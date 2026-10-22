---
lang: en
title: Reservoir
type: reference
audience: everyone
status: draft
---

# Reservoir

Library name: **Reservoir**. A storage volume on the product line, with an optional gas exchange.

## Place it when

The train needs a clear-water volume between treatment and delivery.

## Streams

In: product. Out: product. Out: flush, and that anchor is optional.

## Inputs

Shared unit count is repeated here (default 1, range 1–40). Shape is `rectangular` or `cylindrical`.

| Field | Unit | Default | When |
|---|---|---|---|
| `reservoir_width` | m | 10 | Rectangular. Range 1–100 |
| `reservoir_length` | m | 20 | Rectangular. Range 1–100 |
| `reservoir_diameter` | m | 10 | Cylindrical. Range 1–50 |
| `reservoir_height` | m | 5 | Range 1–20 |
| `inlet_elevation` | m | 2 | Range 0–80. Replaces the shared default |
| `influent_pressure_loss` | mH₂O | 0 | Range 0–10 |
| `mean_water_level` | m | 3 | Up to the reservoir height |
| `integrated_aeration` | — | false | |
| `co2_removal` | fraction | 0.5 | Only if aeration is on. Range 0–1 |
| `o2_saturation` | fraction | 0.8 | Only if aeration is on. Range 0–1 |

## Science

[Aeration](../../explanation/aeration.md) for the optional gas exchange. The reservoir itself is storage, not a treatment reaction.
