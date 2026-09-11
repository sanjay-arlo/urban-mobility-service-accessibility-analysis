from __future__ import annotations

import io
import json
import math
import re
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUT_STATIONS = DATA_DIR / "gtfs_station_metrics.csv"
OUT_SEGMENTS = DATA_DIR / "gtfs_metro_segment_travel_times.csv"
OUT_META = DATA_DIR / "gtfs_refresh_metadata.json"

GTFS_URL = "https://github.com/ungalsoththu/ChennaiGTFS/raw/main/data/chennai-unified-gtfs.zip"
REQUIRED = ["stops.txt", "routes.txt", "trips.txt", "stop_times.txt"]


def read_csv(zf: zipfile.ZipFile, name: str, usecols=None) -> pd.DataFrame:
    candidates = [name, f"unified/{name}", f"gtfs/{name}"]
    for candidate in candidates:
        if candidate in zf.namelist():
            return pd.read_csv(zf.open(candidate), usecols=usecols, low_memory=False)
    raise FileNotFoundError(name)


def haversine_m(lat1, lon1, lat2, lon2):
    r = 6371000.0
    p1, p2 = math.radians(float(lat1)), math.radians(float(lat2))
    dlat = math.radians(float(lat2) - float(lat1))
    dlon = math.radians(float(lon2) - float(lon1))
    a = math.sin(dlat / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlon / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def gtfs_seconds(value) -> int | None:
    if pd.isna(value):
        return None
    parts = str(value).strip().split(":")
    if len(parts) != 3:
        return None
    try:
        h, m, s = [int(x) for x in parts]
    except ValueError:
        return None
    if not (0 <= m < 60 and 0 <= s < 60 and h >= 0):
        return None
    return h * 3600 + m * 60 + s


def percentile_rank(series: pd.Series, ascending: bool = True) -> pd.Series:
    clean = pd.to_numeric(series, errors="coerce")
    if clean.dropna().empty:
        return pd.Series(float("nan"), index=series.index)
    lo, hi = float(clean.min()), float(clean.max())
    if math.isclose(lo, hi):
        return pd.Series(1.0, index=series.index)
    return (clean - lo) / (hi - lo) if ascending else (hi - clean) / (hi - lo)


def classify_route_type(value) -> str:
    """Return metro/bus/other using numeric GTFS type plus feed-specific text fallbacks."""
    text = str(value).strip().lower()
    numeric = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
    if pd.notna(numeric):
        if numeric == 1:
            return "metro"
        if numeric == 3:
            return "bus"
    if re.search(r"(metro|subway|mass rapid|rail|cmrl)", text):
        return "metro"
    if re.search(r"(bus|mtc)", text):
        return "bus"
    return "other"


def main():
    DATA_DIR.mkdir(exist_ok=True)
    req = Request(GTFS_URL, headers={"User-Agent": "urban-mobility-portfolio-pipeline/1.2"})
    with urlopen(req, timeout=90) as response:
        payload = response.read()

    with zipfile.ZipFile(io.BytesIO(payload)) as zf:
        names = {Path(x).name for x in zf.namelist()}
        missing = [x for x in REQUIRED if x not in names]
        if missing:
            raise RuntimeError(f"GTFS feed is missing required files: {missing}")

        routes = read_csv(zf, "routes.txt", ["route_id", "route_short_name", "route_long_name", "route_type"])
        trips = read_csv(zf, "trips.txt", ["route_id", "trip_id"])
        stops = read_csv(zf, "stops.txt", ["stop_id", "stop_name", "stop_lat", "stop_lon"])
        stop_times = read_csv(
            zf,
            "stop_times.txt",
            ["trip_id", "arrival_time", "departure_time", "stop_id", "stop_sequence"],
        )

    routes["transport_mode"] = routes["route_type"].map(classify_route_type)
    stops["stop_lat"] = pd.to_numeric(stops["stop_lat"], errors="coerce")
    stops["stop_lon"] = pd.to_numeric(stops["stop_lon"], errors="coerce")
    stop_times["stop_sequence"] = pd.to_numeric(stop_times["stop_sequence"], errors="coerce")

    metro_routes = routes[routes["transport_mode"] == "metro"].copy()
    bus_routes = routes[routes["transport_mode"] == "bus"].copy()
    if metro_routes.empty:
        raise RuntimeError(
            "No metro routes detected in the GTFS feed. "
            "The feed's route_type schema may differ; inspect routes.txt before generating accessibility metrics."
        )

    metro_trip_ids = set(trips.loc[trips["route_id"].isin(metro_routes["route_id"]), "trip_id"])
    bus_trip_ids = set(trips.loc[trips["route_id"].isin(bus_routes["route_id"]), "trip_id"])

    metro_stop_ids = set(stop_times.loc[stop_times["trip_id"].isin(metro_trip_ids), "stop_id"])
    bus_stop_ids = set(stop_times.loc[stop_times["trip_id"].isin(bus_trip_ids), "stop_id"])

    metro_stops = stops[stops["stop_id"].isin(metro_stop_ids)].copy()
    bus_stops = stops[stops["stop_id"].isin(bus_stop_ids)].copy()
    metro_stops = metro_stops.dropna(subset=["stop_lat", "stop_lon"]).drop_duplicates("stop_id")
    bus_stops = bus_stops.dropna(subset=["stop_lat", "stop_lon"]).drop_duplicates("stop_id")

    if metro_stops.empty:
        raise RuntimeError(
            f"Metro routes were detected ({len(metro_routes)}), but no metro stops were mapped through trips/stop_times. "
            "Check route_id/trip_id relationships in the feed."
        )

    metro_st = stop_times[stop_times["trip_id"].isin(metro_trip_ids)][["trip_id", "stop_id"]].merge(
        trips[["trip_id", "route_id"]], on="trip_id", how="left"
    )
    routes_per_stop = metro_st.groupby("stop_id")["route_id"].nunique().rename("metro_route_count")
    trip_count_per_stop = metro_st.groupby("stop_id")["trip_id"].nunique().rename("metro_trip_count")

    mt = stop_times[stop_times["trip_id"].isin(metro_trip_ids)].copy()
    mt = mt.sort_values(["trip_id", "stop_sequence"])
    mt["dep_sec"] = mt["departure_time"].map(gtfs_seconds)
    mt["arr_sec"] = mt["arrival_time"].map(gtfs_seconds)
    mt["next_stop_id"] = mt.groupby("trip_id")["stop_id"].shift(-1)
    mt["next_arr_sec"] = mt.groupby("trip_id")["arr_sec"].shift(-1)
    mt = mt[mt["next_stop_id"].notna()].copy()
    mt["travel_time_min"] = (
        pd.to_numeric(mt["next_arr_sec"], errors="coerce")
        - pd.to_numeric(mt["dep_sec"], errors="coerce")
    ) / 60.0
    mt = mt[mt["travel_time_min"].between(0.1, 60, inclusive="both")]

    seg = mt.groupby(["stop_id", "next_stop_id"], as_index=False).agg(
        median_scheduled_travel_time_min=("travel_time_min", "median"),
        trip_observations=("travel_time_min", "size"),
    )
    seg = seg.rename(columns={"stop_id": "from_stop_id", "next_stop_id": "to_stop_id"})
    seg = seg.merge(
        metro_stops[["stop_id", "stop_name"]].rename(
            columns={"stop_id": "from_stop_id", "stop_name": "from_station"}
        ),
        on="from_stop_id",
        how="left",
    )
    seg = seg.merge(
        metro_stops[["stop_id", "stop_name"]].rename(
            columns={"stop_id": "to_stop_id", "stop_name": "to_station"}
        ),
        on="to_stop_id",
        how="left",
    )
    seg.to_csv(OUT_SEGMENTS, index=False)

    bus_coords = list(
        bus_stops[["stop_id", "stop_name", "stop_lat", "stop_lon"]].itertuples(index=False)
    )
    rows = []
    for row in metro_stops.itertuples(index=False):
        if bus_coords:
            distances = [
                haversine_m(row.stop_lat, row.stop_lon, b.stop_lat, b.stop_lon)
                for b in bus_coords
            ]
            nearest_idx = min(range(len(distances)), key=distances.__getitem__)
            nearest = float(distances[nearest_idx])
            within_500 = int(sum(d <= 500 for d in distances))
            nearest_bus = bus_coords[nearest_idx]
            nearest_name = nearest_bus.stop_name
            nearest_id = nearest_bus.stop_id
        else:
            nearest, within_500, nearest_name, nearest_id = float("nan"), 0, None, None

        rows.append(
            {
                "stop_id": row.stop_id,
                "station_name": row.stop_name,
                "latitude": row.stop_lat,
                "longitude": row.stop_lon,
                "nearest_bus_stop_m": round(nearest, 1) if not math.isnan(nearest) else None,
                "bus_stops_within_500m": within_500,
                "nearest_bus_stop": nearest_name,
                "nearest_bus_stop_id": nearest_id,
            }
        )

    station_metrics = pd.DataFrame(rows)
    station_metrics = station_metrics.set_index("stop_id")
    station_metrics = station_metrics.join(routes_per_stop, how="left").join(trip_count_per_stop, how="left")
    station_metrics["metro_route_count"] = station_metrics["metro_route_count"].fillna(0).astype(int)
    station_metrics["metro_trip_count"] = station_metrics["metro_trip_count"].fillna(0).astype(int)
    station_metrics["interchange_flag"] = (station_metrics["metro_route_count"] > 1).astype(int)

    station_metrics["route_coverage_score"] = percentile_rank(station_metrics["metro_route_count"], ascending=True)
    station_metrics["first_mile_proximity_score"] = percentile_rank(
        station_metrics["nearest_bus_stop_m"], ascending=False
    )
    station_metrics["bus_stop_density_score"] = percentile_rank(
        station_metrics["bus_stops_within_500m"], ascending=True
    )
    station_metrics["network_first_mile_screening_index"] = (
        100
        * (
            station_metrics["route_coverage_score"]
            + station_metrics["first_mile_proximity_score"]
            + station_metrics["bus_stop_density_score"]
        )
        / 3
    ).round(1)
    station_metrics["first_mile_band"] = pd.cut(
        station_metrics["nearest_bus_stop_m"],
        bins=[-float("inf"), 250, 500, float("inf")],
        labels=["Strong (<250m)", "Moderate (250–500m)", "Long (>500m)"],
    ).astype("string")
    station_metrics.reset_index().to_csv(OUT_STATIONS, index=False)

    metadata = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_url": GTFS_URL,
        "source_description": "Chennai unified static GTFS community feed containing MTC + CMRL network data",
        "metro_route_count": int(len(metro_routes)),
        "bus_route_count": int(len(bus_routes)),
        "metro_stop_count": int(len(metro_stops)),
        "bus_stop_count": int(len(bus_stops)),
        "metro_segment_count": int(len(seg)),
        "metrics": {
            "scheduled_travel_time": "Median scheduled minutes between consecutive metro stops derived from GTFS stop_times",
            "first_mile": "Straight-line distance from each metro station to nearest GTFS bus stop",
            "first_mile_500m": "Count of GTFS bus stops within 500m straight-line radius",
            "screening_index": "Equal-weight normalized combination of route coverage, inverse nearest-bus-stop distance, and 500m bus-stop density; screening only",
        },
        "limitations": [
            "Static GTFS represents scheduled service, not observed traffic or real-time delays.",
            "Straight-line first/last-mile distances are proximity proxies, not pedestrian network travel distance.",
            "The community GTFS feed is not presented as an official CMRL/CUMTA feed.",
        ],
    }
    OUT_META.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()
