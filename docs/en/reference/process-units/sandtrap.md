---
lang: en
title: Sand trap
type: reference
audience: everyone
status: draft
---

# Sand trap

Library name: **Sand trap**. A settling channel on the waste line.

## Place it when

A waste stream carries grains that should drop out before the water goes on.

## Streams

In: waste. Out: waste. It does not sit on the product train.

## Inputs

| Field | Unit | Default | Range or choices |
|---|---|---|---|
| `nominal_capacity` | m³/h | 1000 | 10–5000 |
| `length` | m | 5 | 1–20 |
| `width` | m | 2 | 0.1–10 |
| `height_at_inlet` | m | 1 | 0.1–10 |
| `height_at_outlet` | m | 1.5 | 0.1–10 |
| `temperature` | °C | 10 | 0–40 |
| `particle_material` | — | quartz-sand | quartz-sand, anthracite, hydro-anthracite, garnet, pellets, basalt, marble, gravel, other |
| `other_particle_density` | kg/m³ | 2650 | 1000–5000, when the material is other |
| `particle_size` | mm | 0.8 | 0.1–5 |

Viscosity for this block cites the Viswanath and Natarajan data book. The citation is on [Literature](../../explanation/literature.md).
