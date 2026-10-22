---
lang: en
title: Abstraction
type: reference
audience: everyone
status: draft
---

# Abstraction

Library name: **Abstraction**. Calculation type: `groundwater`. The source of raw water and of the analysis the rest of the train starts from.

## Place it when

The scenario needs a wellfield: yearly volume, well hydraulics, and the groundwater analysis.

## Streams

Out: product. This anchor is the emitter. It builds the initial PHREEQC solution.

## Wells and production

This block does not use the shared capacity defaults. Its own are:

| Field | Unit | Default | Range |
|---|---|---|---|
| `yearly_production` | Mm³ | 10 | 0–100 |
| `minimal_capacity` | m³/h | 500 | 1–10000 |
| `nominal_capacity` | m³/h | 1000 | 1–10000 |
| `maximal_capacity` | m³/h | 1500 | 1–10000 |
| `number_of_wells` | — | 4 | 1–40 |
| `average_well_capacity` | m³/h | 100 | 1–500 |
| `average_elevation` | m | 0 | −10–50 |
| `average_groundwater_level` | m | −1 | −10–20 |
| `average_drawdown` | m | 3 | 0.1–10 |
| `minor_losses` | mH₂O | 1 | 0–3 |

The transport pipe on the same block: inner diameter 450 mm (100–2500), length 1000 m (100–50000), material PE, PVC, or Steel.

## Composition

| Group | Fields | Unit | Notes |
|---|---|---|---|
| Common | pH, temperature | —, °C | Defaults 7 and 10 °C |
| Dissolved gases | oxygen, nitrogen, methane, hydrogen sulfide | mg/l | Defaults 0, 15, 1, 0 |
| Cations | iron, manganese, ammonium, calcium, magnesium, sodium, potassium, barium, strontium | mg/l | Iron defaults to 5, calcium to 60 |
| Anions | bicarbonate, chloride, nitrite, nitrate, sulfate, phosphate, fluoride, silicate, boron | mg/l | Bicarbonate defaults to 140 |
| Other | total organic carbon, colour | mg/l | Default 0 |

## What it reports

Installed capacity (wells times average well capacity), production, head at the well, head at treatment, required pump head, and pipe head loss. Well-pump energy uses `well_efficiency`.

## Science

[Reading water quality](../../explanation/reading-water-quality.md).
