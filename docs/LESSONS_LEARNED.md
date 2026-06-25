# Lessons Learned

## Architectural Decisions

- `master_properties.json` became the source of truth for `property_id`, geometry, measurements, and source region.
- Raw GeoJSON is an input, not the application contract.
- Geometry exists only once, in master properties, to avoid drift and duplicate geospatial payloads.
- Every business dataset references `property_id` so future APIs can assemble property packets predictably.
- Risk reports are not generated. `future_risk_tier` is synthetic profile data, not a risk-engine result.
- Verification results are not generated. Document statuses are generated availability states, not verification outcomes.
- Full location intelligence is not generated. `location_scores.json` is a simple proximity artifact, not flood/elevation/waterlogging/environmental analysis.
- MongoDB Atlas is the target database documented in `mongodb_import_summary.json`; Atlas code is not implemented here.
- Datasets are validated through `consistency_report.json`; current status is `passed`.
- Documents are generated separately by type and then merged into `documents_all.json`.

## Important Corrections During Development

- Source geography was normalized into master properties before synthesis.
- Identity was centralized around `property_id`.
- Geometry duplication was avoided.
- Legal documents were split by type and merged for query flexibility.
- Statistics and validation became generated artifacts.

## Future Improvements (Not Implemented)

Add release metadata, formal schema contracts, and separate future risk, verification, environmental, recommendation, AI, and RAG systems.
