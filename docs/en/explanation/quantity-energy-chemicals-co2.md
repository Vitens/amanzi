---
title: Quantity, energy, chemicals, CO₂
type: explanation
audience: everyone
status: outline
---

# Quantity, energy, chemicals, CO₂

What the non-quality result families mean and how they depend on key figures.

## Content to write

- **Quantity:** abstraction vs delivered water vs losses (including waste and unrecycled flush).
- **Energy:** kWh/m³ and yearly totals; well pumps, boosters, blowers, vacuum, high-pressure membrane pumps — efficiencies from key figures (`well_efficiency`, `booster_efficiency`, …).
- **Chemicals:** masses from dosing, softening, carbon replacement, membrane chemicals as implemented; units g AS/m³.
- **Sustainability:** `electricity_consumption × carbon_intensity_grid` plus per-chemical emission factors plus methane where applied; gCO₂-eq/m³ and per year.
- Changing a key figure changes CO₂ without redrawing the plant — that is the point of overwrites.
- These families are accounting on top of the hydraulic/quality solution, not a separate physical simulation.

## Diagrams

- Mermaid: solve quality/hydraulics → energy & chemicals → multiply by key-figure factors → CO₂.
