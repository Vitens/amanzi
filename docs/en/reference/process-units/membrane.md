---
lang: en
title: Membrane filtration
type: reference
audience: everyone
status: draft
---

# Membrane filtration

Library name: **Membrane filtration**. An RO or NF stack. Permeate continues. Concentrate leaves as waste.

## Place it when

Dissolved solids have to be held back. Recovery is the share of feed that becomes permeate.

## Streams

In: product. Out: product (permeate). Out: waste (concentrate).

## Inputs

| Field | Unit | Default | Range or choices |
|---|---|---|---|
| `inlet_elevation` | m | 1 | −10–12. Replaces the shared default |
| `pressure_loss_cartridge_filter` | mH₂O | 2 | 0.01–20 |
| `pressure_loss_between_stages` | mH₂O | 2 | 0.01–20 |
| `membrane_type` | — | ESPA2-LD | ESPA2-LD, ESPA2-LD-MAX, ESPA4-LD, ESPA4-MAX, AK-400H, AK-440H |
| `number_of_stages` | — | 3 | 1–3 |
| `modules_per_vessel` | — | 6 | 1–10 |
| `optiflux` | — | false | When on, vessels double and modules per vessel halve |
| `stage1_vessels` | — | 12 | 1–20 |
| `stage2_vessels` | — | 6 | 1–20. Shown from 2 stages |
| `stage3_vessels` | — | 3 | 1–20. Shown at 3 stages |
| `recovery` | fraction | 0.8 | 0.5–0.95 |

Minimum and maximum capacity on this block are hidden sentinels (−1), not fields you set. Nominal capacity stays the shared field.

## What it reports

Feed pressure, flux per stage, permeate and concentrate TDS, and supersaturation of the concentrate. Salt passage uses the element rejection from the manufacturer row. Kw is in m³/(m²·bar·h).

## Science

[Membranes](../../explanation/membranes.md).
