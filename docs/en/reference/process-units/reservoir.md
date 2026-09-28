---
title: Reservoir
type: reference
audience: everyone
status: outline
---

# Reservoir

Library name: **Reservoir**. Storage on the train; can hold flush volume and optional aeration.

## Place it when

You need a tank or clear-well between units, or a place for backwash water to sit before reuse.

## Streams

- In/out: product.
- Flush split via the unit’s hydraulic equations (backwash hold-up).

## Inputs (UI groups)

- Shared capacities and elevations.
- Reservoir geometry / volume (design section of `reservoir` parameters).
- Optional integrated aeration (aeration parametric layer).

## Outputs / design tables

- Hydraulic headloss and flush split.
- Energy if pumping/aeration is enabled.
- Sustainability inherited from base outputs when energy or chemicals apply.

## Science

[Scenarios and flowsheets](../../explanation/scenarios-and-flowsheets.md).
