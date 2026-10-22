---
lang: en
title: Vacuum degassing
type: reference
audience: everyone
status: draft
---

# Vacuum degassing

Library name: **Vacuum degassing**. A vessel under vacuum. The gas phase includes hydrogen sulfide as `H2Sg`.

## Place it when

Methane or hydrogen sulfide has to be pulled out by lowering the pressure, rather than by blowing air through a tower.

## Streams

In: product. Out: product.

## Inputs

| Field | Unit | Default | Range or choices |
|---|---|---|---|
| `diameter` | m | 2 | 0.1–10 |
| `spray_height` | m | 1 | 0–5 |
| `bed_height` | m | 3 | 0–10 |
| `pressure_loss_nozzles` | mH₂O | 2 | 0.01–10 |
| `vacuum_pump` | — | liquid_ring | liquid_ring, screw |
| `vacuum_pressure` | bara | 0.2 | 0.05–0.5 |

The same gas-processing switches as the tower (flare, power generation, generator efficiency and availability) apply to the off-gas.

## What it reports

The design view sweeps vacuum and plots pH, saturation index, and the gases.

## Science

[Membranes](../../explanation/membranes.md).
