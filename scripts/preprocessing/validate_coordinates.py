from __future__ import annotations

import logging
from typing import Any

import geopandas as gpd
from shapely import get_coordinates

from .common import (
    CONFIG_DIR,
    VALIDATION_REPORT_DIR,
    bbox_dict,
    discover_sources,
    ensure_directories,
    load_json,
    read_geojson,
    source_id_for_row,
    write_json,
)

LOGGER = logging.getLogger(__name__)


def _in_range(value: float, limits: list[float]) -> bool:
    return limits[0] <= value <= limits[1]


def validate_coordinate_ranges(gdf: gpd.GeoDataFrame, region: str) -> dict[str, Any]:
    config = load_json(CONFIG_DIR / "region_config.json")
    global_lat = config["global_bounds"]["lat"]
    global_lon = config["global_bounds"]["lon"]
    expected_lat = config["expected_bounds"]["lat"]
    expected_lon = config["expected_bounds"]["lon"]

    invalid = []
    suspicious = []
    for idx, row in gdf.iterrows():
        geometry = row.geometry
        if geometry is None or geometry.is_empty:
            continue
        coords = get_coordinates(geometry)
        has_invalid = any(
            not _in_range(float(lon), global_lon) or not _in_range(float(lat), global_lat)
            for lon, lat in coords[:, :2]
        )
        min_lon, min_lat, max_lon, max_lat = geometry.bounds
        outside_expected = (
            min_lat < expected_lat[0]
            or max_lat > expected_lat[1]
            or min_lon < expected_lon[0]
            or max_lon > expected_lon[1]
        )
        item = {
            "index": int(idx),
            "source_id": source_id_for_row(row, idx),
            "bbox": bbox_dict(geometry),
        }
        if has_invalid:
            invalid.append(item)
        if outside_expected:
            suspicious.append(item)

    return {
        "region": region,
        "total_features": int(len(gdf)),
        "invalid_coordinate_count": int(len(invalid)),
        "suspicious_coordinate_count": int(len(suspicious)),
        "invalid_coordinates": invalid,
        "suspicious_coordinates": suspicious,
        "records_removed": 0,
        "rules": {
            "global_lat": global_lat,
            "global_lon": global_lon,
            "expected_hyderabad_lat": expected_lat,
            "expected_hyderabad_lon": expected_lon,
        },
    }


def run_coordinate_validation() -> dict[str, dict[str, Any]]:
    ensure_directories()
    reports = {}
    for source in discover_sources():
        LOGGER.info("Validating coordinates for %s", source.path.name)
        report = validate_coordinate_ranges(read_geojson(source.path), source.region)
        write_json(VALIDATION_REPORT_DIR / f"{source.region}_coordinate_validation.json", report)
        reports[source.region] = report
    return reports
