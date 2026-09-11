from __future__ import annotations

import io
import json
import math
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

# Use the publisher's separate feeds instead of the unified feed. This avoids
# ambiguity in route_type/agency mappings and keeps the metro-vs-bus logic explicit.
CMRL_GTFS_URL = "https://github.com/ungalsoththu/ChennaiGTFS/raw/main/data/cmrl-gtfs.zip"
MTC_GTFS_URL = "https://github.com/ungalsoththu/ChennaiGTFS/raw/main/data/mtc-gtfs.zip"


def download_zip(url: str) -> zipfile.ZipFile:
    req = Request(url, headers={"User-Agent": "urban-mobility-portfolio-pipeline/2.0"})
    with urlopen(req, timeout=90) as response:
        payload = response.read()
    return zipfile.ZipFile(io.BytesIO(payload))


def read_csv(zf: zipfile.ZipFile, name: str, usecols=None) -> pd.DataFrame:
    candidates = [name, f"cmrl/{name}", f"mtc/{name}", f"unified/{name}", f"gtfs/{name}"]
    names = set(zf.namelist())
    for candidate in candidates:
        if candidate in names:
            return pd.read_csv(zf.open(candidate), usecols=usecols, low_memory=False)
    raise FileNotFoundError(f"{name} not found in feed. Available files: {sorted(names)[:20]}")


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
    if not (h >= 0 and 0 <= m < 60 and 0 <= s < 60):
        return None
    return h * 3600 + m * 60 + s


def percentile_rank(series: pd.Series, ascending: bool = True) -> pd.Series:
    clean = pd.to_numeric(series, errors="coerce")
    if clean.dropna().empty:
        return pd.Series(float("nan"), index=series.index)
    lo, hi = float(clean.min()), float(clean.max())
    if math.isclose(lo, hi):
        return pd.Series(1.0, index=series.index)
    if ascending:
        return (clean - lo) / (hi - lo)
    return (hi - clean) / (hi - lo)


def main():
    DATA_DIR.mkdir(exist_ok=True)

    with download_zip(CMRL_GTFS_URL) as cmrl_zip, download_zip(MTC_GTFS_URL) as mtc_zip:
        cmrl_trips = read_csv(cmrl_zip, "trips.txt", ["route_id", "trip_id"])
        cmrl_stops = read_csv(cmrl_zip, "stops.txt", ["stop_id", "stop_name", "stop_lat", "stop_lon"])
        cmrl_stop_times = read_csv(
            cmrl_zip,
            "stop_times.txt",
            ["trip_id", "arrival_time", "departure_time", "stop_id", "stop_sequence"],
        )

        cmrl_routes = read_csv(cmrl_zip, "routes.txt", ["route_id", "route_short_name", "route_long_name", "route_type"])

        mtc_trips = read_csv(mtc_zip, "trips.txt", ["route_id", "trip_id"])
        mtc_stops = read_csv(mtc_zip, "stops.txt", ["stop_id", "stop_name", "stop_lat", "stop_lon"])
        mtc_stop_times = read_csv(mtc_zip, "stop_times.txt", ["trip_id", "stop_id"])
        mtc_routes = read_csv(mtc_zip, "routes.txt", ["route_id", "route_short_name", "route_long_name", "route_type"])

    for frame in (cmrl_stops, mtc_stops):
        frame["stop_lat"] = pd.to_numeric(frame["stop_lat"], errors="coerce")
        frame["stop_lon"] = pd.to_numeric(frame["stop_lon"], errors="coerce")

    # Every stop in the dedicated CMRL feed is a metro-network stop.
    cmrl_stop_ids = set(cmrl_stop_times["stop_id"].dropna().astype(str))
    mtc_stop_ids = set(mtc_stop_times["stop_id"].dropna().astype(str))
    cmrl_stops["stop_id"] = cmrl_stops["stop_id"].astype(str)
    mtc_stops["stop_id"] = mtc_stops["stop_id"].astype(str)
    cmrl_stops = cmrl_stops[cmrl_stops["stop_id"].isin(cmrl_stop_ids)].dropna(subset=["stop_lat", "stop_lon"]).drop_duplicates("stop_id")
    mtc_stops = mtc_stops[mtc_stops["stop_id"].isin(mtc_stop_ids)].dropna(subset=["stop_lat", "stop_lon"]).drop_duplicates("stop_id")

    if cmrl_stops.empty:
        raise RuntimeError("CMRL feed returned no usable metro stops.")
    if mtc_stops.empty:
        raise RuntimeError("MTC feed returned no usable bus stops.")

    cmrl_st = cmrl_stop_times[["trip_id", "stop_id"]].merge(cmrl_trips[["trip_id", "route_id"]], on="trip_id", how="left")
    routes_per_stop = cmrl_st.groupby("stop_id")["route_id"].nunique().rename("metro_route_count")
    trip_count_per_stop = cmrl_st.groupby("stop_id")["trip_id"].nunique().rename("metro_trip_count")

    # Scheduled CMRL segment travel time from the dedicated CMRL stop_times file.
    mt = cmrl_stop_times.copy()
    mt["stop_id"] = mt["stop_id"].astype(str)
    mt["stop_sequence"] = pd.to_numeric(mt["stop_sequence"], errors="coerce")
    mt = mt.sort_values(["trip_id", "stop_sequence"])
    mt["dep_sec"] = mt["departure_time"].map(gtfs_seconds)
    mt["arr_sec"] = mt["arrival_time"].map(gtfs_seconds)
    mt["dep_sec"] = mt["dep_sec"].fillna(mt["arr_sec"])
    mt["arr_sec"] = mt["arr_sec"].fillna(mt["dep_sec"])
    mt["next_stop_id"] = mt.groupby("trip_id")["stop_id"].shift(-1)
    mt["next_arr_sec"] = mt.groupby("trip_id")["arr_sec"].shift(-1)
    mt = mt[mt["next_stop_id"].notna()].copy()
    mt["travel_time_min"] = (pd.to_numeric(mt["next_arr_sec"], errors="coerce") - pd.to_numeric(mt["dep_sec"], errors="coerce")) / 60.0
    mt = mt[mt["travel_time_min"].between(0.1, 60, inclusive="both")]

    seg = mt.groupby(["stop_id", "next_stop_id"], as_index=False).agg(
        median_scheduled_travel_time_min=("travel_time_min", "median"),
        trip_observations=("travel_time_min", "size"),
    )
    seg = seg.rename(columns={"stop_id": "from_stop_id", "next_stop_id": "to_stop_id"})
    seg = seg.merge(
        cmrl_stops[["stop_id", "stop_name"]].rename(columns={"stop_id": "from_stop_id", "stop_name": "from_station"}),
        on="from_stop_id", how="left",
    )
    seg = seg.merge(
        cmrl_stops[["stop_id", "stop_name"]].rename(columns={"stop_id": "to_stop_id", "stop_name": "to_station"}),
        on="to_stop_id", how="left",
    )
    if seg.empty:
        raise RuntimeError("No consecutive CMRL metro segments with usable schedule times were derived.")
    seg.to_csv(OUT_SEGMENTS, index=False)

    # First/last-mile screening: nearest MTC stop and bus-stop density around each metro station.
    bus_coords = list(mtc_stops[["stop_id", "stop_name", "stop_lat", "stop_lon"]].itertuples(index=False))
    rows = []
    for row in cmrl_stops.itertuples(index=False):
        distances = [haversine_m(row.stop_lat, row.stop_lon, b.stop_lat, b.stop_lon) for b in bus_coords]
        nearest_idx = min(range(len(distances)), key=distances.__getitem__)
        nearest = float(distances[nearest_idx])
        within_500 = int(sum(d <= 500 for d in distances))
        nearest_bus = bus_coords[nearest_idx]
        rows.append(
            {
                "stop_id": row.stop_id,
                "station_name": row.stop_name,
                "latitude": row.stop_lat,
                "longitude": row.stop_lon,
                "nearest_bus_stop_m": round(nearest, 1),
                "bus_stops_within_500m": within_500,
                "nearest_bus_stop": nearest_bus.stop_name,
                "nearest_bus_stop_id": nearest_bus.stop_id,
            }
        )

    station_metrics = pd.DataFrame(rows)
    if station_metrics.empty:
        raise RuntimeError("No station-level GTFS accessibility rows were generated.")
    station_metrics = station_metrics.set_index("stop_id")
    station_metrics = station_metrics.join(routes_per_stop, how="left").join(trip_count_per_stop, how="left")
    station_metrics["metro_route_count"] = station_metrics["metro_route_count"].fillna(0).astype(int)
    station_metrics["metro_trip_count"] = station_metrics["metro_trip_count"].fillna(0).astype(int)
    station_metrics["interchange_flag"] = (station_metrics["metro_route_count"] > 1).astype(int)
    station_metrics["route_coverage_score"] = percentile_rank(station_metrics["metro_route_count"], ascending=True)
    station_metrics["first_mile_proximity_score"] = percentile_rank(station_metrics["nearest_bus_stop_m"], ascending=False)
    station_metrics["bus_stop_density_score"] = percentile_rank(station_metrics["bus_stops_within_500m"], ascending=True)
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
        "cmrl_source_url": CMRL_GTFS_URL,
        "mtc_source_url": MTC_GTFS_URL,
        "source_description": "Separate Chennai CMRL metro and MTC bus static GTFS feeds maintained by UngalSoththu.",
        "cmrl_route_count": int(len(cmrl_routes)),
        "mtc_route_count": int(len(mtc_routes)),
        "metro_stop_count": int(len(cmrl_stops)),
        "bus_stop_count": int(len(mtc_stops)),
        "metro_segment_count": int(len(seg)),
        "metrics": {
            "scheduled_travel_time": "Median scheduled minutes between consecutive CMRL stops derived from stop_times",
            "first_mile": "Straight-line distance from each CMRL station to nearest MTC bus stop",
            "first_mile_500m": "Count of MTC bus stops within 500m straight-line radius",
            "screening_index": "Equal-weight normalized combination of route coverage, inverse nearest-bus-stop distance and 500m bus-stop density; screening only",
        },
        "limitations": [
            "Static GTFS represents scheduled service, not observed traffic or real-time delays.",
            "Straight-line first/last-mile distances are proximity proxies, not pedestrian network travel distance.",
            "The source feeds are community-maintained and are not presented as official CMRL/CUMTA open-data feeds.",
        ],
    }
    OUT_META.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()
