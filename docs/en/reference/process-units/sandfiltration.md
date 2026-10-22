---
lang: en
title: Sand filtration
type: reference
audience: everyone
status: draft
---

# Sand filtration

Library name: **Sand filtration**. Rapid filter. Optional dual media, optional spray, then the oxidation sequence.

## Place it when

Iron, manganese, ammonium, methane, or hydrogen sulfide should come out on a sand bed, with or without an anthracite layer.

## Streams

In: product. Out: product. In: flush. Out: waste.

## Bed

`dual_media` defaults to false. Anthracite fields appear only when it is on.

| Field | Unit | Default | Range |
|---|---|---|---|
| `height_anthracite` | m | 0.5 | 0.1–2 |
| `diameter_anthracite` | mm | 1.3 | 0.1–3 |
| `porosity_anthracite` | — | 0.45 | 0.1–0.6 |
| `porosity_anthracite_clogged` | — | 0.25 | 0.1–0.6 |
| `height_sand` | m | 1.0 | 0.5–3 |
| `diameter_sand` | mm | 1.3 | 0.1–3 |
| `porosity_sand` | — | 0.45 | 0.1–0.6 |
| `porosity_sand_clogged` | — | 0.25 | 0.1–0.6 |

## Filter geometry and backwash

From the shared filtration fields. `spray` defaults to false. Shape is rectangular (length 10 m, width 2.5 m) or circular (diameter 3 m). Fall height to the media is 0.5 m (0.1–2). Filter bottom is 0.5 m (0.1–1). Supernatant level is 0.2 m, up to the fall height.

Backwash pump efficiency 0.6 (0.4–0.8, fraction). Backwash head 5 mH₂O (1–10). Control is `time` (runtime 24 h, range 1–500) or `volume` (run volume 5000 m³, range 10–100000).

Spray nozzle area and the three gas efficiencies are in [Spray aeration](sprayaerator.md). Nozzle pressure loss is 1 mH₂O when spray is on.

## Removal

Each of iron, ammonium, and manganese has a suppress switch, default off. When a switch is on, that removal efficiency is a fraction, default 1, range 0–1. Otherwise removal goes as far as the oxygen allows.

## What it reports

The design view lists the oxidation steps. Clean-bed head loss is Kozeny–Carman. Backwash head loss and expansion use a 15 °C viscosity. The waste stream receives the captured iron.

## Science

[Filtration](../../explanation/filtration.md).
