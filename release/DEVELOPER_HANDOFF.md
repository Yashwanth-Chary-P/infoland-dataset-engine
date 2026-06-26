# Developer Handoff

## Current State

Dataset generation is feature complete. Current consistency status is `passed` and all metrics are zero.

## How Datasets Are Generated

Run only when intentional regeneration is required:

```powershell
python scripts/run_preprocessing.py
python scripts/run_synthesis.py
python scripts/run_business_dataset_generation.py
```

## Where Outputs Are Stored

| Output Area | Contents |
| --- | --- |
| data/raw/ | Current raw GeoJSON inputs. |
| data/geojson/ | Legacy GeoJSON inputs. |
| data/cleaned/ | Cleaned GeoJSON outputs. |
| data/master/ | Canonical master property datasets. |
| data/poi/ | Extracted source POIs. |
| data/generated/ | Generated synthetic and business datasets. |
| data/generated/documents/ | 18 legal document datasets plus documents_all. |
| data/generated/reports/ | Generated coverage, consistency, statistics, schema, import, and sample reports. |
| data/reports/ | Preprocessing inspection, validation, and statistics reports. |

## How Validation Works

Preprocessing validates coordinates, geometries, and deduplication. Business validation checks orphan references, ownership chains, registry integrity, duplicate IDs, document merge counts, dispute/loan/tax consistency, health summaries, and timelines.

## What Should Not Be Changed

Do not change Python source, JSON datasets, generated reports, schemas, naming conventions, folder structure, or generation behavior unless the dataset phase is reopened.

## Future Repository Consumption

Use `master_properties.json` as the canonical property and geometry source, join by `property_id`, load `documents_all.json` for unified document queries, and use `mongodb_import_summary.json` as collection guidance only.

## Future Improvements (Not Implemented)

Add release checklists, checksums, and downstream contract tests in future repositories.
