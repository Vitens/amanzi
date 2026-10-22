---
lang: en
title: Units of measure
type: reference
audience: everyone
status: draft
---

# Units of measure

Interpretation of the quantities Amanzi stores. The label in the form is the unit below, except where a field is a fraction.

| Quantity | Unit |
|---|---|
| Capacity, pipe flow | m³/h |
| Yearly production | Mm³ (the quantity panel shows Mm³/y) |
| Head, elevation, bed height | m |
| Head loss | mH₂O. A membrane stage pressure in bar is head divided by 9.81 where the stack does that conversion |
| Temperature | °C. The tower’s ambient-temperature field is stored as `C` |
| Ions and dissolved gases on Abstraction | mg/l |
| pH, saturation index | — |
| Constant dose, pellet base and acid dose | mmol/L |
| Chemical mass | g AS/m³, and g AS/mol for formula weight |
| Energy intensity | kWh/m³ |
| Yearly energy on the panel | MWh/y |
| Grid factor | gCO₂/kWh |
| Chemical emission factor | gCO₂/g AS |
| Methane factor | gCO₂/gCH₄ |
| Specific CO₂ | gCO₂-eq/m³ |
| Yearly CO₂ on the panel | ton CO₂-eq/y |
| Air ratio RQ on a tower or plate | — (m³ air per m³ water) |
| Sweep gas on a membrane contactor | Nm³/m³ |
| Vacuum | bara |
| Blower pressure | Pa |
| Membrane permeability Kw | m³/(m²·bar·h) |
| Conductivity EGV | mS/m |
| Hardness | mmol/l |

## Fractions labelled %

Several fields use the unit label `%` and a range that runs from 0 to 1. The stored number is a fraction. 0.8 is 80%. This applies to splitter split, recycle efficiency, membrane recovery, bypass open, removal efficiencies, spray efficiencies, reservoir aeration efficiencies, blower and fan efficiencies stored on a 0–1 scale, and iron and manganese capture on the pellet reactor.

Well and booster efficiencies in the key figures are different: those defaults are 55 and 75, and the hydraulic solver divides them by 100.
