---
title: Transport pipeline
type: reference
audience: everyone
status: outline
---

# Transport pipeline

Library name: **Transport Pipeline**. Pipe for headloss between units. No custom quality change.

## Place it when

You need length, diameter, and roughness between two points on the hydraulic line.

## Streams

- In/out: product (or whichever anchors the block exposes).

## Inputs (UI groups)

- **Transport:** length, diameter, material/roughness as in the form.
- Shared hydraulic-line elevations.

## Outputs / design tables

- Headloss and residual head.
- Pumping energy if a booster is implied by the hydraulic solver.

## Science

[How Amanzi calculates](../../explanation/how-amanzi-calculates.md) (hydraulics / energy).
