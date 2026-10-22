---
lang: en
title: Spray aeration
type: reference
audience: everyone
status: draft
---

# Spray aeration

Library name: **Spray aeration**. The block is hidden. It is not in the library. The same fields appear on [sand filtration](sandfiltration.md) and [marble filtration](marblefiltration.md) when `spray` is on.

## Inputs

All of these apply only when spray is on.

| Field | Unit | Default | Range |
|---|---|---|---|
| `area_per_nozzle` | m² | 1 | 0.1–10 |
| `co2_removal_efficiency` | fraction | 0.50 | 0.01–1 |
| `ch4_removal_efficiency` | fraction | 0.30 | 0.01–1 |
| `o2_saturation` | fraction | 0.80 | 0.01–1 |

Nozzle pressure loss and fall height to the media are on the filter, not on this hidden block. Fall height to the media defaults to 0.5 m (0.1–2).

## Science

[Aeration](../../explanation/aeration.md). The calculation that runs is the fall-height polynomial, not a Sauter diameter.
