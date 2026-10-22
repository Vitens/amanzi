---
lang: en
title: Key figures
type: reference
audience: everyone
status: draft
---

# Key figures

Shared lookup values. The file is `amanzi/database/key_figures.csv`. Columns: name (the tag), category, type, default, UOM, remarks.

The dialog groups them as **General** and **Chemical**. Under General the types are operational, **Sustainability & Emissions**, and **Quality standards**. Under Chemical the rows are emission factors.

| Tag | Default | Unit | Role |
|---|---|---|---|
| `max_hour` | 1.2 | — | Day peak factor |
| `well_efficiency` | 55 | % | Well pumps |
| `booster_efficiency` | 75 | % | Booster pumps |
| `carbon_intensity_grid` | 250 | gCO₂/kWh | Electricity |
| `methane_emission_factor` | 28 | gCO₂/gCH₄ | Methane |
| `ph_lower_limit` | 7 | — | Quality standard, one of a lower/upper limit and threshold pair |
| `hardness_upper_limit` | 2 | mmol/l | Quality standard |
| `lye_emission` | 1.27 | gCO₂/g AS | Chemical factor |

The same pattern covers the other quality rows (pH, conductivity, SI, oxygen, hardness, aggressive CO₂, TACC₉₀, iron, manganese, ammonium, sodium, chloride) and the other chemical factors (lime, CO₂, acids, oxygen, filter sand, seed materials, and the rest of the chemical block).

A project overwrite replaces the default for every scenario. A scenario overwrite replaces it for that scenario only. An empty cell means the column is not an override. A missing tag at calculation time is an error.

The CSV in the repository also contains `sum4PFAS_limit` (20 ng/l), `sum20PFAS_limit` (100 ng/l), and `PEQ_limit` (4.4 ng/l). The public app’s key-figure list does not show those three rows. How to edit a figure that is on the list is in [Set key figures](../how-to/set-key-figures.md).
