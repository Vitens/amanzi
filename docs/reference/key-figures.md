---
title: Key figures
type: reference
audience: everyone
status: outline
---

# Key figures

Lookup values shared across calculations. Source of truth: `amanzi/database/key_figures.csv`. The UI can overwrite them per project and per scenario.

## Content to write

- Columns: name, category, type, default, UOM, remarks.
- Categories the UI groups: general (operational and emission), chemicals (emission factors), and the remaining groups as they appear after filling from the CSV (PFAS limits, materials).
- Examples to list when filling: `carbon_intensity_grid` (gCO₂/kWh), well and booster efficiencies (%), chemical emission factors (gCO₂/g AS), methane emission factor, new vs regenerated activated carbon.
- PFAS-related limits stored as key figures: Sum4, Sum20, PEQ (exact keys when filling from CSV).
- Overwrites: project `key_figure_overwrites` and scenario-level overwrites.
- Missing key figure at runtime raises an error.

Fill later from `key_figures.csv`; do not paste the whole CSV into this outline.
