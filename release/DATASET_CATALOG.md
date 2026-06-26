# Dataset Catalog

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

## Document Datasets

Each of the 18 legal document datasets contains 1633 records, one per property. `documents_all.json` contains 29394 merged records.

| Document Type | Filename | Records | Additional Fields |
| --- | --- | --- | --- |
| sale_deed | data/generated/documents/sale_deeds.json | 1633 | seller_name, buyer_name, registration_number, registration_date, market_value |
| mother_deed | data/generated/documents/mother_deeds.json | 1633 | parent_document_number, ownership_chain_length, origin_year |
| encumbrance_certificate | data/generated/documents/encumbrance_certificates.json | 1633 | ec_period_from, ec_period_to, encumbrance_count, active_encumbrance |
| property_tax_receipt | data/generated/documents/property_tax_receipts.json | 1633 | financial_year, tax_amount, paid_amount, pending_amount |
| mutation_record | data/generated/documents/mutation_records.json | 1633 | mutation_number, mutation_date, reason |
| survey_map | data/generated/documents/survey_maps.json | 1633 | survey_number, plot_area_sqyd, survey_date |
| rtc_record | data/generated/documents/rtc_records.json | 1633 | survey_number, land_type, cultivation_status |
| khata_certificate | data/generated/documents/khata_certificates.json | 1633 | khata_number, owner_name |
| khata_extract | data/generated/documents/khata_extracts.json | 1633 | khata_number, assessment_value |
| building_approval_plan | data/generated/documents/building_approval_plans.json | 1633 | approval_number, approved_floors, approval_date |
| layout_approval | data/generated/documents/layout_approvals.json | 1633 | layout_number, approved_by, approval_date |
| land_conversion_certificate | data/generated/documents/land_conversion_certificates.json | 1633 | conversion_type, conversion_date |
| occupancy_certificate | data/generated/documents/occupancy_certificates.json | 1633 | building_type, occupancy_date |
| completion_certificate | data/generated/documents/completion_certificates.json | 1633 | completion_date, approved_structure |
| noc | data/generated/documents/nocs.json | 1633 | issuing_department, valid_until |
| identity_proof | data/generated/documents/identity_proofs.json | 1633 | owner_id, proof_type, proof_last4 |
| power_of_attorney | data/generated/documents/power_of_attorneys.json | 1633 | principal_name, agent_name, valid_until |
| court_dispute_record | data/generated/documents/court_dispute_records.json | 1633 | case_number, court_name, case_type, case_status |

## Relationship Notes

`property_id` connects the property ecosystem. `owner_id` links owners, registry, and identity proofs. `document_id` identifies document records. Geometry is only in `master_properties`.

## Future Improvements (Not Implemented)

Publish this catalog as a machine-readable manifest for downstream repositories.
