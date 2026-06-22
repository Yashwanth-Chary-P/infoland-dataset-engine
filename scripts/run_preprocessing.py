from __future__ import annotations

import logging
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from scripts.preprocessing.classify_features import classify_gdf
from scripts.preprocessing.common import (
    CLEANED_DIR,
    INSPECTION_REPORT_DIR,
    REQUIRED_CLEAN_COLUMNS,
    STATISTICS_REPORT_DIR,
    VALIDATION_REPORT_DIR,
    clean_text,
    configure_logging,
    discover_sources,
    ensure_directories,
    source_id_for_row,
    write_geojson,
    write_json,
)
from scripts.preprocessing.create_master_dataset import create_master_dataset
from scripts.preprocessing.deduplicate_features import deduplicate_gdf
from scripts.preprocessing.enrich_properties import enrich_properties, enrichment_report
from scripts.preprocessing.extract_poi import extract_pois
from scripts.preprocessing.generate_statistics import generate_statistics
from scripts.preprocessing.inspect_geojson import inspect_gdf
from scripts.preprocessing.validate_coordinates import validate_coordinate_ranges
from scripts.preprocessing.validate_geometries import validate_and_repair_geometries

LOGGER = logging.getLogger(__name__)


def _prepare_clean_output(gdf, region: str):
    output = gdf.copy()
    output["source_id"] = [source_id_for_row(row, idx) for idx, row in output.iterrows()]
    output["source_region"] = region
    for column in ["feature_category", "building", "amenity", "landuse"]:
        if column not in output.columns:
            output[column] = ""
        output[column] = output[column].apply(clean_text)
    return output[REQUIRED_CLEAN_COLUMNS]


def run_pipeline() -> dict:
    ensure_directories()
    enriched_by_region = {}
    processing_reports = {}

    for source in discover_sources():
        LOGGER.info("Processing %s", source.region)
        raw = __import__("scripts.preprocessing.common", fromlist=["read_geojson"]).read_geojson(source.path)

        inspection = inspect_gdf(raw, source.region)
        write_json(INSPECTION_REPORT_DIR / f"{source.region}_inspection.json", inspection)

        coordinate_validation = validate_coordinate_ranges(raw, source.region)
        write_json(
            VALIDATION_REPORT_DIR / f"{source.region}_coordinate_validation.json",
            coordinate_validation,
        )

        geometry_cleaned, geometry_validation = validate_and_repair_geometries(raw, source.region)
        write_json(
            VALIDATION_REPORT_DIR / f"{source.region}_geometry_validation.json",
            geometry_validation,
        )

        deduped, deduplication = deduplicate_gdf(geometry_cleaned, source.region)
        classified, classification = classify_gdf(deduped, source.region)
        enriched = enrich_properties(classified)
        enriched["source_region"] = source.region

        clean_output = _prepare_clean_output(enriched, source.region)
        write_geojson(clean_output, CLEANED_DIR / f"{source.region}_clean.geojson")

        enriched_by_region[source.region] = clean_output
        processing_reports[source.region] = {
            "inspection": inspection,
            "coordinate_validation": coordinate_validation,
            "geometry_validation": geometry_validation,
            "deduplication": deduplication,
            "classification": classification,
            "enrichment": enrichment_report(clean_output, source.region),
        }
        write_json(
            STATISTICS_REPORT_DIR / f"{source.region}_processing_summary.json",
            processing_reports[source.region],
        )

    poi_counts = extract_pois(enriched_by_region)
    master_records = create_master_dataset(enriched_by_region)
    overall_stats = generate_statistics(
        enriched_by_region=enriched_by_region,
        master_records=master_records,
        poi_counts=poi_counts,
        processing_reports=processing_reports,
    )
    return overall_stats


def main() -> None:
    configure_logging()
    stats = run_pipeline()
    LOGGER.info("Preprocessing complete: %s", stats)


if __name__ == "__main__":
    main()
