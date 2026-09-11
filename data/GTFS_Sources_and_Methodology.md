# GTFS Sources & Methodology

## Primary network source

The analysis is designed around Chennai's static GTFS ecosystem. CUMTA's **Transit Data Chennai** portal is the official open-data backbone for Chennai mobility and provides static GTFS datasets for MTC, Metro and Suburban rail.

For the automated refresh pipeline in this portfolio project, the configured machine-readable feed is the community-maintained **ChennaiGTFS unified feed**, which combines Chennai transit network data and is openly published on GitHub. The project does **not** represent this community feed as an official CUMTA/CMRL publication.

Source feed:
`https://github.com/ungalsoththu/ChennaiGTFS/raw/main/data/chennai-unified-gtfs.zip`

## What the pipeline derives

### Scheduled metro travel time

The pipeline reads `trips.txt` and `stop_times.txt`, keeps metro trips, orders stops by `stop_sequence`, and calculates the scheduled time between consecutive metro stops. The repository stores the **median scheduled travel time** and number of trip observations for each adjacent-station segment.

This is timetable-derived in-vehicle time. It is **not** observed congestion time and does not include real-time delays.

### First/last-mile proximity

The pipeline reads metro and bus stops from the GTFS network and computes:

- straight-line distance to the nearest bus stop;
- count of bus stops within 500 metres.

Distance is calculated with the Haversine formula. This is a spatial proximity measure, not a pedestrian-network walking distance.

### Network + first-mile screening index

A transparent 0–100 screening index is created from three min-max-normalised components:

1. metro route coverage;
2. inverse nearest-bus-stop distance;
3. bus-stop density within 500m.

Each component has equal weight. The index is intended to prioritise stations for deeper study; it is **not** a measure of transport equity, socioeconomic accessibility, service quality or passenger experience.

## Refresh process

GitHub Actions runs the pipeline weekly and can also be started manually. It downloads the latest configured GTFS feed, validates required GTFS files, computes derived metrics, and commits:

- `gtfs_station_metrics.csv`
- `gtfs_metro_segment_travel_times.csv`
- `gtfs_refresh_metadata.json`

The dashboard reads those derived CSV files directly.

## Data quality and limitations

The GTFS standard represents routes, trips, stops and scheduled stop times. The official GTFS specification describes `stops.txt`, `routes.txt`, `trips.txt` and `stop_times.txt` as core schedule data. A static feed cannot by itself establish actual road congestion, observed vehicle travel time or real-time delay.

The current first/last-mile metric should therefore be described as **GTFS bus-stop proximity**. A future upgrade can replace the straight-line distance with OpenStreetMap pedestrian-network routing and can add GTFS-Realtime or vehicle telemetry for observed travel times.
