---
title: Units of measure
type: reference
audience: everyone
status: outline
---

# Units of measure

Internal conventions. The UI labels should match these; where they differ, this page wins for interpretation.

## Content to write

- Flow and capacity: m³/h; yearly production often Mm³.
- Hydraulic head: m, mH₂O; some conversions to bar via /9.81.
- Temperature: °C.
- Major ions and dissolved gases (PHREEQC): mg/L (mg/l in forms).
- Dosing: mmol/L for constant dosage.
- PFAS concentrations: **ng/L** inside the engine; other prefixes converted on input.
- VOC in packed tower: **mg/L** (ng/L and µg/L converted).
- TOC / colour: as in scenario metadata.
- GAC Freundlich *K*: `(µg/g)·(L/µg)^(1/n)`; exponent is **1/n**, not *n*.
- Langmuir (isotherm DB): qmax µg/g, KL L/µg.
- Membrane water permeability *Kw*: m³/(m²·bar·h).
- Energy: kWh/m³, kWh/year.
- Emissions: gCO₂-eq/m³, gCO₂-eq/year, gCO₂/kWh, gCO₂/g AS.
- Air/gas: RQ dimensionless; some blower figures kWh/Nm³.

## Diagrams

- None required; a compact table when written.
