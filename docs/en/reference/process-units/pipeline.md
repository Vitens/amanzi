---
lang: en
title: Transport pipeline
type: reference
audience: everyone
status: draft
---

# Transport pipeline

Library name: **Transport Pipeline**. A pipe on the product line. Head loss is Darcy friction. It does not change the water’s chemistry.

## Streams

In: product. Out: product.

## Inputs

| Field | Unit | Default | Range or choices |
|---|---|---|---|
| `pipe_inner_diameter` | mm | 450 | 100–2500 |
| `pipe_length` | m | 1000 | 100–50000 |
| `pipe_material` | — | PE | PE, PVC, Steel |

Roughness used in the friction factor is 0.003 mm for PE, 0.0015 mm for PVC, and 0.045 mm for steel. Kinematic viscosity in this calculation is the constant 1.308 mm²/s. The head-loss result carries a check that loss per metre stays under 0.005.

Abstraction has its own copy of these pipe fields. This block is the one you place between other units.
