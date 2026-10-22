---
lang: en
title: Marble filtration
type: reference
audience: everyone
status: draft
---

# Marble filtration

Library name: **Marble filtration**. The sand-filter oxidation sequence, with calcite saturation after each oxidation, on a marble bed. An optional lime layer can sit with it.

## Place it when

The filter should buffer pH while it oxidises iron, manganese, and ammonium.

## Streams

In: product. Out: product. In: flush. Out: waste.

## Bed

`spray` and `lime_pellets` both default to false. Shape is rectangular or circular, with the same length, width, and diameter defaults as sand filtration.

| Field | Unit | Default | Range | When |
|---|---|---|---|---|
| `height_lime` | m | 0.5 | 0.1–10 | Lime pellets on |
| `diameter_lime` | mm | 1 | 0.0001–100 | Lime pellets on |
| `porosity_lime` | — | 0.5 | 0.1–0.6 | Lime pellets on |
| `porosity_lime_clogged` | — | 0.25 | 0.1–0.6 | Lime pellets on |
| `height_marble` | m | 1 | 0.1–10 | |
| `diameter_marble` | mm | 1 | 0.0001–100 | |
| `porosity_marble` | — | 0.5 | 0.1–0.6 | |
| `porosity_marble_clogged` | — | 0.25 | 0.1–0.6 | |

Fall height, filter bottom, supernatant, and backwash match the sand filter, except runtime is capped at 72 h rather than 500 h. Spray fields match [Spray aeration](sprayaerator.md).

## Removal

The same three suppress switches as sand filtration. Efficiencies are fractions, default 1, and they appear only when that suppress switch is on.

## What it reports

The design view lists the same oxidation steps as the sand filter. Each oxidation also saturates calcite. Backwash iron is calculated the same way, and that waste water is saturated to calcite as well.

## Science

[Filtration](../../explanation/filtration.md).
