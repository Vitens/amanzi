---
title: Pellet softening
type: reference
audience: everyone
status: outline
---

# Pellet softening

Library name: **Pelletontharding** (pellet softening). Lime/soda pellet reactor with bypass and optional acid.

## Place it when

You are reducing hardness by crystallising calcite in a pellet reactor, with optional bypass blending.

## Streams

- In/out: product (bypass is internal).

## Inputs (UI groups)

- **Capacities:** nominal and bypass flow (m³/h).
- **Reactor:** funnel vs cylindrical; heights and diameters.
- **Chemicals:** base and acid species and dosages; acid injection point.
- **Operational / model:** `soften_to_si`, Fe/Mn capture rates, seed material.

## Outputs / design tables

- Step profiles: pH, hardness, CCPP, sc.
- Dosage sweep charts.
- Chemical consumption and CO₂ from chemicals.
- Fluidization / porosity helper.

## Science

[Softening and dosing](../../explanation/softening-and-dosing.md).
