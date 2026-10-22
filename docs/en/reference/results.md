---
lang: en
title: Results
type: reference
audience: everyone
status: draft
---

# Results

The right-hand panel is the scenario that is open, after the last successful solve. **Calculate project** opens the report for that scenario. **Comparison** in the report draws every scenario. Quantity appears in the report only in that comparison. The comparison headings stay Dutch: **Kwantiteit**, **Waterkwaliteit**, **Energie**, **Duurzaamheid**.

An unsolved or disconnected scenario leaves the panel without a fresh result. The message for a missing connection is described in [Streams](streams.md) and [Limitations](limitations.md).

## Quantity

| Row | Meaning | Unit |
|---|---|---|
| Abstraction | Product flow leaving units with nothing upstream | Mm³/y |
| Distribution | Product flow entering units with nothing downstream | Mm³/y |
| Loss | Abstraction minus distribution, also as a percentage | Mm³/y and % |

## Quality

The plant effluent. Labels on the panel: pH, EGV, O₂, HCO₃, TAC, Hardness, TDS, TACC₉₀, AggCO₂, SI, Fe, Mn, NH₄, Na, Cl. Concentrations are mg/l except hardness (mmol/l), EGV (mS/m), and the indexes, which have no unit. What the words mean is in [Reading water quality](../explanation/reading-water-quality.md).

## Energy

| Row | Meaning | Unit on the panel |
|---|---|---|
| Treatment | Specific consumption of the treatment units | kWh/m³ |
| Distribution | Specific consumption of the outlet | kWh/m³ |
| Total | Those two together, and the yearly sum | kWh/m³ and MWh/y |

## Sustainability

| Row | Meaning | Unit on the panel |
|---|---|---|
| Specific emissions | CO₂-equivalent per cubic metre delivered | gCO₂-eq/m³ |
| Total emissions | The same account over the year | ton CO₂-eq/y |

## Chemicals

There is no chemicals heading on the panel. Chemical masses are g AS/m³ on the unit that doses them, and they enter sustainability through the key-figure factors. See [Quantity, energy, chemicals, CO₂](../explanation/quantity-energy-chemicals-co2.md).
