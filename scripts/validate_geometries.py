from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import geopandas as gpd
from shapely.validation import explain_validity, make_valid

from geo_utils import (
    REPORTS_DIR,
    configure_logging,
    discover_geojson_files,
    ensure_output_dirs,
    normalize_region_name,
    read_geojson,
    source_id_for_row,
    write_json,
)

LOGGER = logging.getLogger(__name__)


def _repair_geometry(geometry: Any) -> tuple[Any, str]:
    try:
        repaired = make_valid(geometry)
        if repaired is not None and not repaired.is_empty and repaired.is_valid:
            return repaired, "make_valid"
    except Exception:
        LOGGER.debug("make_valid failed", exc_info=True)

    try:
        repaired = geometry.buffer(0)
        if repaired is not None and not repaired.is_empty and repaired.is_valid:
            return repaired, "buffer(0)"
    except Exception:
        LOGGER.debug("buffer(0) failed", exc_info=True)

    return None, "unrecoverable"


def validate_and_repair_geometries(
    gdf: gpd.GeoDataFrame, region: str
) -> tuple[gpd.GeoDataFrame, dict[str, Any]]:
    cleaned = gdf.copy()
    removed_indices: list[Any] = []
    invalid_features: list[dict[str, Any]] = []
    repaired_count = 0
    null_count = 0
    empty_count = 0

    for idx, row in cleaned.iterrows():
        geometry = row.geometry
        source_id = source_id_for_row(row, idx)
        if geometry is None:
            null_count += 1
            removed_indices.append(idx)
            invalid_features.append(
                {"index": int(idx), "source_id": source_id, "reason": "null geometry"}
            )
            continue
        if geometry.is_empty:
            empty_count += 1
            removed_indices.append(idx)
            invalid_features.append(
                {"index": int(idx), "source_id": source_id, "reason": "empty geometry"}
            )
            continue
        if geometry.is_valid:
            continue

        reason = explain_validity(geometry)
        repaired, method = _repair_geometry(geometry)
        invalid_features.append(
            {
                "index": int(idx),
                "source_id": source_id,
                "reason": reason,
                "repair_method": method,
            }
        )
        if repaired is None:
            removed_indices.append(idx)
        else:
            cleaned.at[idx, "geometry"] = repaired
            repaired_count += 1

    if removed_indices:
        cleaned = cleaned.drop(index=removed_indices)

    report = {
        "region": region,
        "total_features_before": int(len(gdf)),
        "total_features_after": int(len(cleaned)),
        "null_geometries": int(null_count),
        "empty_geometries": int(empty_count),
        "invalid_geometries_found": int(len(invalid_features)),
        "invalid_geometries_repaired": int(repaired_count),
        "invalid_geometries_removed": int(len(removed_indices)),
        "invalid_features": invalid_features,
    }
    return cleaned, report


def validate_file(path: Path) -> tuple[gpd.GeoDataFrame, dict[str, Any]]:
    region = normalize_region_name(path)
    LOGGER.info("Validating geometries for %s", path.name)
    cleaned, report = validate_and_repair_geometries(read_geojson(path), region)
    write_json(REPORTS_DIR / f"{region}_geometry_validation.json", report)
    return cleaned, report


def main() -> None:
    configure_logging()
    ensure_output_dirs()
    for path in discover_geojson_files():
        validate_file(path)


if __name__ == "__main__":
    main()
