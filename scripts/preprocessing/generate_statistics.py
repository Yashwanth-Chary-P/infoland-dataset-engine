from __future__ import annotations

from typing import Any

import geopandas as gpd
import pandas as pd

from .common import STATISTICS_REPORT_DIR, coordinate_bounds, value_counts, write_json


def generate_statistics(
    enriched_by_region: dict[str, gpd.GeoDataFrame],
    master_records: list[dict[str, Any]],
    poi_counts: dict[str, int],
    processing_reports: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    master_df = pd.DataFrame(master_records)
    total_properties = int(len(master_df))
    area = master_df["area_sq_m"] if "area_sq_m" in master_df else pd.Series(dtype=float)

    all_features = pd.concat(enriched_by_region.values(), ignore_index=True)
    all_gdf = gpd.GeoDataFrame(all_features, geometry="geometry", crs="EPSG:4326")

    master_stats = {
        "total_properties": total_properties,
        "properties_per_region": (
            master_df["source_region"].value_counts().sort_index().to_dict()
            if total_properties
            else {}
        ),
        "average_area_sq_m": round(float(area.mean()), 2) if total_properties else 0,
        "median_area_sq_m": round(float(area.median()), 2) if total_properties else 0,
        "min_area_sq_m": round(float(area.min()), 2) if total_properties else 0,
        "max_area_sq_m": round(float(area.max()), 2) if total_properties else 0,
        "category_distribution": (
            master_df["feature_category"].value_counts().sort_index().to_dict()
            if total_properties
            else {}
        ),
        "building_type_distribution": (
            master_df["building"].fillna("").value_counts().sort_index().to_dict()
            if total_properties
            else {}
        ),
        "coordinate_bounds": coordinate_bounds(all_gdf),
    }
    overall_stats = {
        **master_stats,
        "poi_counts": poi_counts,
        "regions_processed": int(len(enriched_by_region)),
        "total_features_before": int(
            sum(report["inspection"]["total_feature_count"] for report in processing_reports.values())
        ),
        "total_features_after_cleaning": int(sum(len(gdf) for gdf in enriched_by_region.values())),
        "invalid_geometries_removed": int(
            sum(
                report["geometry_validation"]["invalid_geometries_removed"]
                for report in processing_reports.values()
            )
        ),
        "duplicates_removed": int(
            sum(report["deduplication"]["duplicates_removed"] for report in processing_reports.values())
        ),
        "all_feature_category_distribution": value_counts(all_gdf, "feature_category"),
    }

    write_json(STATISTICS_REPORT_DIR / "master_dataset_stats.json", master_stats)
    write_json(STATISTICS_REPORT_DIR / "overall_stats.json", overall_stats)
    return overall_stats
