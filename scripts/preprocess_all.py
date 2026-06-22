from __future__ import annotations

import logging
from typing import Any

from classify_features import classify_gdf
from deduplicate_features import deduplicate_gdf
from geo_utils import (
    CLEANED_DIR,
    configure_logging,
    discover_geojson_files,
    ensure_output_dirs,
    make_stats_payload,
    normalize_region_name,
    prepare_output_columns,
    read_geojson,
    value_counts,
    write_geojson,
    write_json,
)
from inspect_geojson import inspect_gdf
from validate_coordinates import validate_coordinate_ranges
from validate_geometries import validate_and_repair_geometries

LOGGER = logging.getLogger(__name__)


def _merge_category_counts(target: dict[str, int], source: dict[str, int]) -> None:
    for key, value in source.items():
        target[key] = target.get(key, 0) + int(value)


def process_all() -> dict[str, Any]:
    ensure_output_dirs()
    per_region_stats: list[dict[str, Any]] = []
    overall_category_distribution: dict[str, int] = {}

    for path in discover_geojson_files():
        region = normalize_region_name(path)
        LOGGER.info("Processing region %s", region)
        raw_gdf = read_geojson(path)
        before_count = len(raw_gdf)

        write_json(
            CLEANED_DIR.parent / "reports" / f"{region}_inspection.json",
            inspect_gdf(raw_gdf, region),
        )
        write_json(
            CLEANED_DIR.parent / "reports" / f"{region}_coordinate_validation.json",
            validate_coordinate_ranges(raw_gdf, region),
        )

        geometry_cleaned, geometry_report = validate_and_repair_geometries(raw_gdf, region)
        write_json(
            CLEANED_DIR.parent / "reports" / f"{region}_geometry_validation.json",
            geometry_report,
        )

        deduped, dedupe_report = deduplicate_gdf(geometry_cleaned, region)
        write_json(
            CLEANED_DIR.parent / "reports" / f"{region}_deduplication.json",
            dedupe_report,
        )

        classified, classification_report = classify_gdf(deduped, region)
        write_json(
            CLEANED_DIR.parent / "reports" / f"{region}_classification.json",
            classification_report,
        )

        output_gdf = prepare_output_columns(classified, region)
        write_geojson(output_gdf, CLEANED_DIR / f"{region}_clean.geojson")

        stats = make_stats_payload(
            region=region,
            before_count=before_count,
            gdf=output_gdf,
            invalid_removed=geometry_report["invalid_geometries_removed"],
            duplicates_removed=dedupe_report["duplicates_removed"],
        )
        write_json(CLEANED_DIR.parent / "reports" / f"{region}_stats.json", stats)
        per_region_stats.append(stats)
        _merge_category_counts(overall_category_distribution, value_counts(output_gdf, "feature_category"))

    overall_stats = {
        "regions_processed": int(len(per_region_stats)),
        "total_features_before": int(
            sum(item["total_features_before"] for item in per_region_stats)
        ),
        "total_features_after": int(sum(item["total_features_after"] for item in per_region_stats)),
        "invalid_removed": int(
            sum(item["invalid_geometries_removed"] for item in per_region_stats)
        ),
        "duplicates_removed": int(sum(item["duplicates_removed"] for item in per_region_stats)),
        "category_distribution": dict(sorted(overall_category_distribution.items())),
    }
    write_json(CLEANED_DIR.parent / "reports" / "overall_stats.json", overall_stats)
    return overall_stats


def main() -> None:
    configure_logging()
    overall_stats = process_all()
    LOGGER.info("Completed preprocessing: %s", overall_stats)


if __name__ == "__main__":
    main()
