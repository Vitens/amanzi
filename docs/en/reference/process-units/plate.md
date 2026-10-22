---
lang: en
title: Plate aeration
type: reference
audience: everyone
status: draft
---

# Plate aeration

Library name: **Plate Aeration**. A perforated plate with a supply fan and an optional recirculated off-gas.

## Place it when

The train needs a first contact with air. The demo uses this block as **Plaatbeluchting**.

## Streams

In: product. Out: product.

## Inputs

| Field | Unit | Default | Range or choices |
|---|---|---|---|
| `type` | — | Metal | Metal, Foil |
| `length` | m | 1 | 0.1–10 |
| `width` | m | 1 | 0.1–10 |
| `hole_diameter` | mm | 1.5 | 0.5–3 |
| `recirculation` | fraction | 0 | 0–0.8 |
| `RQ` | — | 50 | 0–100 |
| `contact_time` | s | 10 | 1–100 |
| Supply, exhaust, and recirculation fan ΔP | Pa | 100 each | 10–2000 |
| Those three fan efficiencies | fraction | 0.75 each | 0.5–1 |
| `efficiency` | — | 0.02 | 0.01–1 |

## Science

[Aeration](../../explanation/aeration.md).
