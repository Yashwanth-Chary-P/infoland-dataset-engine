# MongoDB Collections

This is documentation only. It does not create Atlas code, import scripts, indexes, or APIs.

## Recommended Collections

| Collection | Source JSON | Records | Primary Index | Recommended Secondary Indexes |
| --- | --- | --- | --- | --- |
| property_registry | data/generated/property_registry.json | 1633 | domain id or property_id unique | property_id, status, owner_id, source_region as applicable |
| owners | data/generated/owners.json | 1633 | domain id or property_id unique | property_id, status, owner_id, source_region as applicable |
| ownership_events | data/generated/ownership_events.json | 3517 | domain id or property_id unique | property_id, status, owner_id, source_region as applicable |
| property_metadata | data/generated/property_metadata.json | 1633 | domain id or property_id unique | property_id, status, owner_id, source_region as applicable |
| property_timeline | data/generated/property_timeline.json | 1633 | domain id or property_id unique | property_id, status, owner_id, source_region as applicable |
| property_health_summary | data/generated/property_health_summary.json | 1633 | domain id or property_id unique | property_id, status, owner_id, source_region as applicable |
| loans | data/generated/loans.json | 294 | domain id or property_id unique | property_id, status, owner_id, source_region as applicable |
| tax_records | data/generated/tax_records.json | 1633 | domain id or property_id unique | property_id, status, owner_id, source_region as applicable |
| court_disputes | data/generated/court_disputes.json | 65 | domain id or property_id unique | property_id, status, owner_id, source_region as applicable |
| documents_all | data/generated/documents/documents_all.json | 29394 | domain id or property_id unique | property_id, status, owner_id, source_region as applicable |

## Optional Per-Document Collections

| Collection | Source JSON | Records | Primary Index | Recommended Secondary Indexes |
| --- | --- | --- | --- | --- |
| sale_deed | data/generated/documents/sale_deeds.json | 1633 | document_id unique | property_id, status, issue_date, document_number |
| mother_deed | data/generated/documents/mother_deeds.json | 1633 | document_id unique | property_id, status, issue_date, document_number |
| encumbrance_certificate | data/generated/documents/encumbrance_certificates.json | 1633 | document_id unique | property_id, status, issue_date, document_number |
| property_tax_receipt | data/generated/documents/property_tax_receipts.json | 1633 | document_id unique | property_id, status, issue_date, document_number |
| mutation_record | data/generated/documents/mutation_records.json | 1633 | document_id unique | property_id, status, issue_date, document_number |
| survey_map | data/generated/documents/survey_maps.json | 1633 | document_id unique | property_id, status, issue_date, document_number |
| rtc_record | data/generated/documents/rtc_records.json | 1633 | document_id unique | property_id, status, issue_date, document_number |
| khata_certificate | data/generated/documents/khata_certificates.json | 1633 | document_id unique | property_id, status, issue_date, document_number |
| khata_extract | data/generated/documents/khata_extracts.json | 1633 | document_id unique | property_id, status, issue_date, document_number |
| building_approval_plan | data/generated/documents/building_approval_plans.json | 1633 | document_id unique | property_id, status, issue_date, document_number |
| layout_approval | data/generated/documents/layout_approvals.json | 1633 | document_id unique | property_id, status, issue_date, document_number |
| land_conversion_certificate | data/generated/documents/land_conversion_certificates.json | 1633 | document_id unique | property_id, status, issue_date, document_number |
| occupancy_certificate | data/generated/documents/occupancy_certificates.json | 1633 | document_id unique | property_id, status, issue_date, document_number |
| completion_certificate | data/generated/documents/completion_certificates.json | 1633 | document_id unique | property_id, status, issue_date, document_number |
| noc | data/generated/documents/nocs.json | 1633 | document_id unique | property_id, status, issue_date, document_number |
| identity_proof | data/generated/documents/identity_proofs.json | 1633 | document_id unique | property_id, status, issue_date, document_number |
| power_of_attorney | data/generated/documents/power_of_attorneys.json | 1633 | document_id unique | property_id, status, issue_date, document_number |
| court_dispute_record | data/generated/documents/court_dispute_records.json | 1633 | document_id unique | property_id, status, issue_date, document_number |

## Typical Queries

| Query | Collections | Indexes |
| --- | --- | --- |
| Fetch full property packet | master, profiles, owners, registry, metadata, timeline, health, documents_all, loans, tax, disputes | property_id everywhere |
| Find for-sale properties | property_profiles + master_properties | sale_status, property_class, source_region |
| Find pending tax | tax_records | status, property_id |
| Find active disputes | court_disputes | status, case_type, property_id |
| Find missing documents | documents_all | document_type, status, property_id |
| Fetch ownership chain | ownership_events | property_id, transfer_date |

## Future Improvements (Not Implemented)

Create Atlas ingestion code in a future repository after backend query patterns are known.
