# Data Model

## Core Principle

`property_id` is the spine of the system. `master_properties.json` owns identity and geometry.

```text
master_properties -> property_profiles -> owners -> ownership_events -> documents -> loans -> tax_records -> court_disputes -> property_metadata -> property_timeline -> property_health_summary
```

## Relationships

| Entity | Key | Cardinality / Role |
| --- | --- | --- |
| master_properties | property_id | Root entity and geometry owner |
| property_profiles | property_id | 1:1 |
| owners | owner_id | 1 current owner per property |
| ownership_events | event_id | 1:many per property |
| property_registry | property_id + owner_id | 1:1 current owner bridge |
| documents_all | document_id | 18 records per property |
| loans | loan_id | Optional selected properties |
| tax_records | tax_id | 1:1 |
| court_disputes | dispute_id | Optional selected properties |
| property_metadata | property_id | 1:1 |
| property_timeline | property_id | 1:1 with nested events |
| property_health_summary | property_id | 1:1 summary |

## Geometry Policy

Geometry remains only in `data/master/master_properties.json`. Downstream datasets join back by `property_id`.

## Future Improvements (Not Implemented)

Add formal ER diagrams and schema artifacts for future API repositories.
