---
lang: en
title: Output
type: reference
audience: everyone
status: draft
---

# Output

Library name: **Output**. The sink of the product stream. The scenario’s delivered water is the product flow into this block. The demo often names the block **Levering**.

## Place it when

Every scenario that should solve needs one. Without it the quantity balance has no distribution.

## Streams

In: product. Nothing leaves.

## Inputs

| Field | Unit | Default | Range |
|---|---|---|---|
| `integrated_booster` | — | true | |
| `inlet_elevation` | m | 0 | −10–100 |
| `required_pressure` | mH₂O | 35 | 10–100 |

Distribution energy on the results panel is the share that belongs to this block, including the booster when it is on. Booster efficiency is the key figure `booster_efficiency` (default 75%).
