from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import geopandas as gpd
from shapely import get_coordinates

from geo_utils import (
    GLOBAL_LAT_RANGE,
    GLOBAL_LON_RANGE,
    HYDERABAD_LAT_RANGE,
    HYDERABAD_LON_RANGE,
    REPORTS_DIR,
    configure_logging,
    discover_geojson_files,
    ensure_output_dirs,
    get_geometry_bounds,
    normalize_region_name,
    read_geojson,
    source_id_for_row,
    write_json,
)

LOGGER = logging.getLogger(__name__)


def _in_range(value: float, limits: tuple[float, float]) -> bool:
    return limits[0] <= value <= limits[1]


def validate_coordinate_ranges(gdf: gpd.GeoDataFrame, region: str) -> dict[str, Any]:
    global_invalid: list[dict[str, Any]] = []
    outside_expected_bounds: list[dict[str, Any]] = []

    for idx, row in gdf.iterrows():
        geometry = row.geometry
        source_id = source_id_for_row(row, idx)
        if geometry is None or geometry.is_empty:
            continue

        coordinates = get_coordinates(geometry)
        has_global_invalid = any(
            not _in_range(float(lon), GLOBAL_LON_RANGE)
            or not _in_range(float(lat), GLOBAL_LAT_RANGE)
            for lon, lat in coordinates[:, :2]
        )
        min_lon, min_lat, max_lon, max_lat = geometry.bounds
        outside_hyderabad = (
            min_lat < HYDERABAD_LAT_RANGE[0]
            or max_lat > HYDERABAD_LAT_RANGE[1]
            or min_lon < HYDERABAD_LON_RANGE[0]
            or max_lon > HYDERABAD_LON_RANGE[1]
        )

        if has_global_invalid:
            global_invalid.append(
                {"index": int(idx), "source_id": source_id, "bounds": get_geometry_bounds(geometry)}
            )
        if outside_hyderabad:
            outside_expected_bounds.append(
                {"index": int(idx), "source_id": source_id, "bounds": get_geometry_bounds(geometry)}
            )

    return {
        "region": region,
        "total_features": int(len(gdf)),
        "global_coordinate_invalid_count": len(global_invalid),
        "outside_expected_hyderabad_bounds_count": len(outside_expected_bounds),
        "global_coordinate_invalid_features": global_invalid,
        "outside_expected_hyderabad_bounds_features": outside_expected_bounds,
        "rules": {
            "latitude": {"min": GLOBAL_LAT_RANGE[0], "max": GLOBAL_LAT_RANGE[1]},
            "longitude": {"min": GLOBAL_LON_RANGE[0], "max": GLOBAL_LON_RANGE[1]},
            "expected_hyderabad_latitude": {
                "min": HYDERABAD_LAT_RANGE[0],
                "max": HYDERABAD_LAT_RANGE[1],
            },
            "expected_hyderabad_longitude": {
                "min": HYDERABAD_LON_RANGE[0],
                "max": HYDERABAD_LON_RANGE[1],
            },
        },
        "records_removed": 0,
    }


def validate_file(path: Path) -> dict[str, Any]:
    region = normalize_region_name(path)
    LOGGER.info("Validating coordinates for %s", path.name)
    report = validate_coordinate_ranges(read_geojson(path), region)
    write_json(REPORTS_DIR / f"{region}_coordinate_validation.json", report)
    return report


def main() -> None:
    configure_logging()
    ensure_output_dirs()
    for path in discover_geojson_files():
        validate_file(path)


if __name__ == "__main__":
    main()
