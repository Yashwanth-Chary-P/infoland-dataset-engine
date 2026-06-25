# InfoLand Dataset Engine

InfoLand Dataset Engine is the completed dataset-generation repository for InfoLand property intelligence. It converts Kokapet, Mokila, and Shankarpally geography into canonical master properties, synthetic profiles, POIs, ownership records, legal documents, loans, taxes, disputes, timelines, health summaries, and validation/statistics reports.

This repository is documentation and dataset generation only. It does not implement MongoDB Atlas ingestion, FastAPI, backend APIs, frontend, risk engine, verification engine, AI reports, environmental intelligence, flood analysis, waterlogging analysis, elevation analysis, recommendation engine, or RAG.

## Current Status

Dataset generation is feature complete. `data/generated/reports/consistency_report.json` reports `passed` and every consistency metric is zero.

## Folder Structure

| Path | Purpose |
| --- | --- |
| config/ | Region config and classification rules. |
| data/raw/ | Current raw GeoJSON inputs. |
| data/geojson/ | Legacy GeoJSON inputs. |
| data/cleaned/ | Cleaned GeoJSON outputs. |
| data/master/ | Canonical master property datasets. |
| data/poi/ | Extracted source POIs. |
| data/generated/ | Generated synthetic and business datasets. |
| data/generated/documents/ | 18 legal document datasets plus documents_all. |
| data/generated/reports/ | Generated coverage, consistency, statistics, schema, import, and sample reports. |
| data/reports/ | Preprocessing inspection, validation, and statistics reports. |
| scripts/ | Generation scripts. |
| docs/ | Documentation knowledge base. |

## Pipeline Overview

1. Geographic preprocessing: inspect, validate, repair, deduplicate, classify, enrich, extract POIs, and create master properties.
2. Property synthesis: assign property classes, sale status, synthetic POIs, location scores, and profiles.
3. Business generation: create owners, ownership events, registry, metadata, timeline, health, loans, taxes, disputes, documents, and reports.
4. Validation/statistics: write coverage, consistency, schema, import, and statistics reports.

## Dataset Summary

| Dataset | Records |
| --- | --- |
| properties | 1633 |
| property_profiles | 1633 |
| pois | 95 |
| owners | 1633 |
| ownership_events | 3517 |
| property_registry | 1633 |
| property_metadata | 1633 |
| property_timeline | 1633 |
| property_health_summary | 1633 |
| documents_all | 29394 |
| loans | 294 |
| tax_records | 1633 |
| court_disputes | 65 |

Discovered additional generated artifact: `data/generated/location_scores.json` has 1633 records and feeds `property_profiles.json`; it is not a future environmental or risk engine.

## Current Statistics

| Metric | Value |
| --- | --- |
| Master properties | 1633 |
| Kokapet | 806 |
| Mokila | 592 |
| Shankarpally | 235 |
| Property profiles | 1633 |
| Synthetic POIs | 95 |
| Owners | 1633 |
| Ownership events | 3517 |
| Documents all | 29394 |
| Loans | 294 |
| Tax records | 1633 |
| Court disputes | 65 |
| Consistency status | passed |

## Validation Summary

| Metric | Value |
| --- | --- |
| orphan_owners | 0 |
| orphan_documents | 0 |
| orphan_loans | 0 |
| orphan_tax_records | 0 |
| orphan_disputes | 0 |
| invalid_property_references | 0 |
| ownership_chain_errors | 0 |
| registry_errors | 0 |
| duplicate_current_owners | 0 |
| missing_current_owners | 0 |
| document_merge_count_mismatch | 0 |
| duplicate_owner_ids | 0 |
| duplicate_event_ids | 0 |
| duplicate_loan_ids | 0 |
| duplicate_tax_ids | 0 |
| duplicate_dispute_ids | 0 |
| duplicate_document_ids | 0 |
| court_dispute_document_errors | 0 |
| active_loan_ec_errors | 0 |
| pending_tax_receipt_errors | 0 |
| health_summary_errors | 0 |
| timeline_errors | 0 |

## How to Run

These commands regenerate outputs and should only be run when dataset-generation work intentionally resumes.

```powershell
pip install -r requirements.txt
python scripts/run_preprocessing.py
python scripts/run_synthesis.py
python scripts/run_business_dataset_generation.py
```

## Generated Outputs

Primary outputs live in `data/master/`, `data/generated/`, `data/generated/documents/`, `data/generated/reports/`, and `data/reports/`.

## Future Roadmap

Future repositories/phases should cover Atlas ingestion, APIs, frontend, risk, verification, AI reports, environmental analysis, recommendation, and RAG.

## License

No license file is currently present.
