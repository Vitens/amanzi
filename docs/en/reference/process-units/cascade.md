---
lang: en
title: Cascade
type: reference
audience: everyone
status: draft
---

# Cascade

Library name: **Cascade**. A stair of steps. No blower.

## Place it when

Oxygen uptake and some CO₂ removal are enough, and methane removal can stay modest.

## Streams

In: product. Out: product.

## Inputs

| Field | Unit | Default | Range |
|---|---|---|---|
| `units` | — | 1 | Replaces the shared default |
| `number_of_steps` | — | 3 | 1–8 |
| `step_height` | m | 0.5 | 0.1–2 |
| `cascade_length` | m | 3 | 1–10 |

The block is not pressurized. Head loss of the model is the number of steps times the step height.

## What it reports

The design view repeats the gas transfer for 1 to 8 steps: pH, CO₂, oxygen, and methane.

## Science

[Aeration](../../explanation/aeration.md).
