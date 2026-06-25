# Project Context for AI

## Project Summary

InfoLand Dataset Engine is a completed property dataset generator. It processes Kokapet, Mokila, and Shankarpally geography into master properties and generated business/legal/financial datasets.

## Repository Scope

This repository is documentation and dataset generation only. It does not implement MongoDB Atlas ingestion, FastAPI, backend APIs, frontend, risk engine, verification engine, AI reports, environmental intelligence, flood analysis, waterlogging analysis, elevation analysis, recommendation engine, or RAG.

## Folder Structure

| Path | Meaning |
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

## Pipeline

1. `python scripts/run_preprocessing.py` creates cleaned geography, master properties, POI extracts, and preprocessing reports.
2. `python scripts/run_synthesis.py` creates property profiles, synthetic POIs, location scores, and synthesis stats.
3. `python scripts/run_business_dataset_generation.py` creates owners, ownership events, legal documents, loans, taxes, disputes, metadata, timelines, health summaries, and generated reports.

## Datasets

| Dataset | Filename | Records | Primary Key | Foreign Keys | Generation Source |
| --- | --- | --- | --- | --- | --- |
| master_properties | data/master/master_properties.json | 1633 | property_id | None | scripts/run_preprocessing.py |
| property_candidates | data/master/property_candidates.json | 1633 | property_id | property_id -> master_properties.property_id | scripts/run_preprocessing.py |
| property_profiles | data/generated/property_profiles.json | 1633 | property_id | property_id -> master_properties.property_id | scripts/run_synthesis.py |
| synthetic_pois | data/generated/synthetic_pois.json | 95 | poi_id | None | scripts/run_synthesis.py |
| location_scores | data/generated/location_scores.json | 1633 | property_id | property_id -> master_properties.property_id | scripts/run_synthesis.py |
| owners | data/generated/owners.json | 1633 | owner_id | property_id -> master_properties.property_id | scripts/run_business_dataset_generation.py |
| ownership_events | data/generated/ownership_events.json | 3517 | event_id | property_id -> master_properties.property_id; owner ids in transfer fields | scripts/run_business_dataset_generation.py |
| property_registry | data/generated/property_registry.json | 1633 | property_id | property_id -> master_properties.property_id | scripts/run_business_dataset_generation.py |
| property_metadata | data/generated/property_metadata.json | 1633 | property_id | property_id -> master_properties.property_id | scripts/run_business_dataset_generation.py |
| property_timeline | data/generated/property_timeline.json | 1633 | property_id | property_id -> master_properties.property_id | scripts/run_business_dataset_generation.py |
| property_health_summary | data/generated/property_health_summary.json | 1633 | property_id | property_id -> master_properties.property_id | scripts/run_business_dataset_generation.py |
| loans | data/generated/loans.json | 294 | loan_id | property_id -> master_properties.property_id | scripts/run_business_dataset_generation.py |
| tax_records | data/generated/tax_records.json | 1633 | tax_id | property_id -> master_properties.property_id | scripts/run_business_dataset_generation.py |
| court_disputes | data/generated/court_disputes.json | 65 | dispute_id | property_id -> master_properties.property_id | scripts/run_business_dataset_generation.py |
| sale_deed | data/generated/documents/sale_deeds.json | 1633 | document_id | property_id -> master_properties.property_id | scripts/run_business_dataset_generation.py |
| mother_deed | data/generated/documents/mother_deeds.json | 1633 | document_id | property_id -> master_properties.property_id | scripts/run_business_dataset_generation.py |
| encumbrance_certificate | data/generated/documents/encumbrance_certificates.json | 1633 | document_id | property_id -> master_properties.property_id | scripts/run_business_dataset_generation.py |
| property_tax_receipt | data/generated/documents/property_tax_receipts.json | 1633 | document_id | property_id -> master_properties.property_id | scripts/run_business_dataset_generation.py |
| mutation_record | data/generated/documents/mutation_records.json | 1633 | document_id | property_id -> master_properties.property_id | scripts/run_business_dataset_generation.py |
| survey_map | data/generated/documents/survey_maps.json | 1633 | document_id | property_id -> master_properties.property_id | scripts/run_business_dataset_generation.py |
| rtc_record | data/generated/documents/rtc_records.json | 1633 | document_id | property_id -> master_properties.property_id | scripts/run_business_dataset_generation.py |
| khata_certificate | data/generated/documents/khata_certificates.json | 1633 | document_id | property_id -> master_properties.property_id | scripts/run_business_dataset_generation.py |
| khata_extract | data/generated/documents/khata_extracts.json | 1633 | document_id | property_id -> master_properties.property_id | scripts/run_business_dataset_generation.py |
| building_approval_plan | data/generated/documents/building_approval_plans.json | 1633 | document_id | property_id -> master_properties.property_id | scripts/run_business_dataset_generation.py |
| layout_approval | data/generated/documents/layout_approvals.json | 1633 | document_id | property_id -> master_properties.property_id | scripts/run_business_dataset_generation.py |
| land_conversion_certificate | data/generated/documents/land_conversion_certificates.json | 1633 | document_id | property_id -> master_properties.property_id | scripts/run_business_dataset_generation.py |
| occupancy_certificate | data/generated/documents/occupancy_certificates.json | 1633 | document_id | property_id -> master_properties.property_id | scripts/run_business_dataset_generation.py |
| completion_certificate | data/generated/documents/completion_certificates.json | 1633 | document_id | property_id -> master_properties.property_id | scripts/run_business_dataset_generation.py |
| noc | data/generated/documents/nocs.json | 1633 | document_id | property_id -> master_properties.property_id | scripts/run_business_dataset_generation.py |
| identity_proof | data/generated/documents/identity_proofs.json | 1633 | document_id | property_id -> master_properties.property_id; owner_id -> owners.owner_id | scripts/run_business_dataset_generation.py |
| power_of_attorney | data/generated/documents/power_of_attorneys.json | 1633 | document_id | property_id -> master_properties.property_id | scripts/run_business_dataset_generation.py |
| court_dispute_record | data/generated/documents/court_dispute_records.json | 1633 | document_id | property_id -> master_properties.property_id | scripts/run_business_dataset_generation.py |
| documents_all | data/generated/documents/documents_all.json | 29394 | document_id | property_id -> master_properties.property_id | scripts/run_business_dataset_generation.py |

## Relationships

`property_id` is the root key. Geometry is only in `master_properties`. `owner_id`, `document_id`, `loan_id`, `tax_id`, and `dispute_id` identify related domain records.

## Field Overview

Use `docs/FIELD_REFERENCE.md` for every field. Common document fields are: document_id, property_id, document_type, status, issue_date, last_updated, issuing_authority, document_number, remarks.

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

## Validation Results

Consistency status is `passed`; all consistency metrics are zero.

## Architecture Decisions

Master properties are the source of truth; raw GeoJSON is input only; geometry is centralized; documents are generated separately and merged; MongoDB Atlas is documented as the target; app and intelligence layers are future work.

## Future Improvements (Not Implemented)

Add machine-readable schemas, release manifests, and separate future implementation repositories.
