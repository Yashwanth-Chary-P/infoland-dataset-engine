from __future__ import annotations

import logging
from typing import Any

import geopandas as gpd
from shapely.validation import explain_validity, make_valid

from .common import (
    VALIDATION_REPORT_DIR,
    discover_sources,
    ensure_directories,
    read_geojson,
    source_id_for_row,
    write_json,
)

LOGGER = logging.getLogger(__name__)


def _repair_geometry(geometry: Any) -> tuple[Any, str]:
    for method in ("make_valid", "buffer(0)"):
        try:
            repaired = make_valid(geometry) if method == "make_valid" else geometry.buffer(0)
            if repaired is not None and not repaired.is_empty and repaired.is_valid:
                return repaired, method
        except Exception:
            LOGGER.debug("%s failed", method, exc_info=True)
    return None, "unrecoverable"


def validate_and_repair_geometries(
    gdf: gpd.GeoDataFrame, region: str
) -> tuple[gpd.GeoDataFrame, dict[str, Any]]:
    cleaned = gdf.copy()
    removed = []
    invalid_features = []
    repaired_count = 0
    null_count = 0
    empty_count = 0

    for idx, row in cleaned.iterrows():
        geometry = row.geometry
        source_id = source_id_for_row(row, idx)
        if geometry is None:
            null_count += 1
            removed.append(idx)
            invalid_features.append({"index": int(idx), "source_id": source_id, "reason": "null"})
            continue
        if geometry.is_empty:
            empty_count += 1
            removed.append(idx)
            invalid_features.append({"index": int(idx), "source_id": source_id, "reason": "empty"})
            continue
        if geometry.is_valid:
            continue
        reason = explain_validity(geometry)
        repaired, method = _repair_geometry(geometry)
        invalid_features.append(
            {"index": int(idx), "source_id": source_id, "reason": reason, "repair_method": method}
        )
        if repaired is None:
            removed.append(idx)
        else:
            cleaned.at[idx, "geometry"] = repaired
            repaired_count += 1

    if removed:
        cleaned = cleaned.drop(index=removed)

    report = {
        "region": region,
        "total_features_before": int(len(gdf)),
        "total_features_after": int(len(cleaned)),
        "null_geometries": int(null_count),
        "empty_geometries": int(empty_count),
        "invalid_geometries_found": int(len(invalid_features)),
        "invalid_geometries_repaired": int(repaired_count),
        "invalid_geometries_removed": int(len(removed)),
        "invalid_features": invalid_features,
    }
    return cleaned, report


def run_geometry_validation() -> dict[str, tuple[gpd.GeoDataFrame, dict[str, Any]]]:
    ensure_directories()
    results = {}
    for source in discover_sources():
        LOGGER.info("Validating geometries for %s", source.path.name)
        cleaned, report = validate_and_repair_geometries(read_geojson(source.path), source.region)
        write_json(VALIDATION_REPORT_DIR / f"{source.region}_geometry_validation.json", report)
        results[source.region] = (cleaned, report)
    return results
