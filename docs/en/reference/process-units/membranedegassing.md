---
lang: en
title: Membrane degassing
type: reference
audience: everyone
status: draft
---

# Membrane degassing

Library name: **Membrane degassing**. One or two vacuum contactors with a nitrogen and CO₂ sweep.

## Place it when

Gases should leave without an open aerator loading the water with oxygen.

## Streams

In: product. Out: product.

## Inputs

| Field | Unit | Default | Range or choices |
|---|---|---|---|
| `num_stages` | — | double | single, double |
| `membranes_per_stage` | — | 4 | 1–10 |
| `membrane_type` | — | EXF14x40 | EXF14x40, EXF14x28 |
| `vacuum_type` | — | liquid-ring | liquid-ring, screw |
| `nitrogen_source` | — | cryogenic | cryogenic, PSA |
| `nitrogen_purity` | — | 4 | 4 or 5 |
| `pressure_loss_cartridge_filter` | mH₂O | 2 | 0.01–20 |
| `n2_rq_stage_1` | Nm³/m³ | 0 | 0–1 |
| `co2_rq_stage_1` | Nm³/m³ | 0.02 | 0–1 |
| `vacuum_stage_1` | bara | 0.10 | 0.01–1 |
| Stage 2 sweep and vacuum | same units | 0, 0, 0.10 | Shown when the contactor is double |
| `vent_flare` | — | false | When the vent path applies |

PSA power uses the key figures `psa_purity_4_power_consumption` (0.61 kWh/Nm³) and `psa_purity_5_power_consumption` (0.82 kWh/Nm³), matching purity 4 and 5.

## Science

[Membranes](../../explanation/membranes.md).
