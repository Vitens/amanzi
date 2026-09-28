---
title: Vacuum degassing
type: reference
audience: everyone
status: outline
---

# Vacuum degassing

Library name: **Vacuum degassing**. Single-stage vacuum stripper (not a membrane contactor).

## Place it when

You degas by lowering the gas-phase pressure on a vessel, and want pH / SI / gas composition vs vacuum.

## Streams

- In/out: product.

## Inputs (UI groups)

- Vessel / vacuum setpoints (operational).
- Shared capacities and hydraulic line.
- Gas-processing fields when enabled.

## Outputs / design tables

- Design charts: pH, SI, gas composition vs pressure.
- Dry and wet gas composition (v1.0.2+).
- Totals per m³, per unit, and process (v1.0.2+).
- Vacuum energy.

## Science

[Membranes](../../explanation/membranes.md) (comparison with membrane degassing), [How Amanzi calculates](../../explanation/how-amanzi-calculates.md).
