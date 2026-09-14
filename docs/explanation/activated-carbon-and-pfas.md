---
title: Activated carbon and PFAS
type: explanation
audience: keyuser
status: outline
---

# Activated carbon and PFAS

GAC as implemented in Amanzi: competitive isotherms, simplified breakthrough, staggering, regulatory sums, and the design-vs-runtime gap.

## Content to write

- PFAS live in the **extraneous** stream (ng/L), not in PHREEQC.
- **SRS (Sheindorf–Rebhun–Sheintuch)** competitive Freundlich; *K* in `(µg/g)·(L/µg)^(1/n)`, exponent **1/n**.
- DOC competition via TOC → DOC; competition coefficients.
- Simplified breakthrough (stationary flow, no dispersion): *C/C₀ = 1 / (1 + exp(k · EBCT · (1 − BV · C_in / q)))*.
- PEQ-weighted Sum4 / Sum20 vs key-figure limits.
- Staggered replacement: blending peak pre-replacement concentrations across filters.
- Isotherm database: 21 compounds, original vs Amanzi-converted columns; unit conversion rules (Polanyi, EPA WQTC, Cantoni, Chen, Hückstädt, Langmuir).
- Defaults in parametric PFAS YAML (Polanyi predicted) vs literature rows.
- **Gap:** `design()` runs this physics; `run_quality()` does not apply PFAS removal (optional spray only).
- Micropollutant % removal from scenario metadata for OMV-style organics.

## Diagrams

- Mermaid: influent PFAS → SRS capacity → breakthrough → staggering blend → design tables (not plant walk).
