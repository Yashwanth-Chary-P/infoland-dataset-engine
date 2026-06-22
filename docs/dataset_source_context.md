# Dataset Source Context

InfoLand source geography currently comes from OpenStreetMap / Overpass Turbo GeoJSON exports for Kokapet, Mokila, and Shankarpally.

This preprocessing phase keeps only real source features. It does not synthesize owners, documents, verification cases, sale status, or risk reports.

The pipeline normalizes raw GeoJSON into cleaned features, property candidates, POI datasets, and a master property dataset keyed by `property_id`.
