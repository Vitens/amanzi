---
lang: en
title: Pellet softening
type: reference
audience: everyone
status: draft
---

# Pellet softening

Library name: **Pelletontharding**. A calcite pellet reactor with a bypass and an optional acid.

## Place it when

Hardness should fall by dosing a base and precipitating calcite, while part of the flow can pass around the reactor.

## Streams

In: product. Out: product. The bypass is a fraction inside the block, not a second anchor.

## Reactor and flows

| Field | Unit | Default | Range or choices |
|---|---|---|---|
| `nominal_capacity` | m³/h | 300 | 0–1000. Replaces the shared default |
| `bypass_capacity` | m³/h | 100 | 0–1000 |
| `inlet_elevation` | m | 1 | −10–20 |
| `reactor_shape` | — | funnel | cylindrical, funnel |
| `height_cylindrical` | m | 5 | 1–10 |
| `diameter_cylindrical` | m | 2 | 0.1–10 |
| `height_funnel` | m | 2 | 1–10, funnel only |
| `diameter_funnel` | m | 3 | From the cylindrical diameter up to 10, funnel only |
| `bypass_open` | fraction | 0.2 | 0–1 |
| `base_dosage` | mmol/L | 1 | 0–5 |
| `acid_dosage` | mmol/L | 0.1 | 0–5 |
| `soften_to_si` | — | 0.6 | 0–2 |
| `fe_capture` | fraction | 0.9 | 0–0.99 |
| `mn_capture` | fraction | 0.9 | 0–0.99 |

## Chemicals and seed

| Field | Default | Choices |
|---|---|---|
| `seed_material` | quartz_sand | quartz_sand, garnet_sand, calcite |
| `base_chemical` | NaOH | NaOH, Ca(OH)2 |
| `acid_chemical` | CO2 | CO2, HCl |
| `acid_position` | reactor-outlet | reactor-outlet, bypass, after-bypass |
| `lime_type` | quicklime | quicklime, hydrated_lime, milk_of_lime, when the base is lime |

Pellet bed: static height 3 m (0.1–10), static porosity 0.4 (0.1–0.9), seed diameter 0.1 mm, pellet diameter 0.5 mm. Each diameter stays on the legal side of the other.

## What it reports

The design view sweeps the base dose and draws pH, hardness, HCO₃, and conductivity. The plant result is the blend of reactor and bypass.

## Science

[Softening and dosing](../../explanation/softening-and-dosing.md).
