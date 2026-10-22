---
lang: en
title: Tower aeration
type: reference
audience: everyone
status: draft
---

# Tower aeration

Library name: **Tower Aeration**. Packed column with a blower.

## Place it when

Methane or another volatile gas has to be stripped, and a cascade is not enough.

## Streams

In: product. Out: product.

## Inputs

| Field | Unit | Default | Range or choices |
|---|---|---|---|
| `pressure_loss_nozzles` | mH₂O | 1 | 0.01–10 |
| `fall_height` | m | 1 | 0.1–10 |
| `diameter` | m | 1 | 0.1–10 |
| `bed_height` | m | 2 | 0.1–10 |
| `packingmaterial` | — | Raflux50 | Raflux25, Raflux50, Raflux90 |
| `blowereficiency` | fraction | 0.75 | 0.01–1 |
| `rq` | — | 50 | 0.01–100 |
| `ambient_temperature` | °C | 20 | −30–40 |
| `air_system_pressure_loss` | Pa | 25 | 0–2000 |

Gas handling on the off-gas, from the shared gas-processing fields: flare (default on), power generation (default on), generator efficiency 0.35 (0.1–0.6, fraction), generator availability 0.9 (0.1–1, fraction). The generator fields apply when power generation is on.

## What it reports

Removal by compound, packing pressure drop, flooding factor, and blower power. The design view draws the operating point against the flooding line.

## Science

[Aeration](../../explanation/aeration.md).
