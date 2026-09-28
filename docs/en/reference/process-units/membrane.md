---
title: Membrane filtration
type: reference
audience: everyone
status: outline
---

# Membrane filtration

Library name: **Membrane filtration**. Multi-stage RO/NF stack; permeate is product, concentrate is waste.

## Place it when

You split the stream into permeate and concentrate with a membrane stack (recovery, staging, element type).

## Streams

- In: product.
- Out: product (permeate); waste (concentrate).

## Inputs (UI groups)

- **Stack:** membrane type (ESPA2-LD, ESPA4, AK-400H, …), number of stages (1–3), modules per vessel, vessels, recovery, optiflux flag.
- **Hydraulic line:** cartridge-filter loss, inter-stage loss, inlet elevation.
- Pressurised by default.

## Outputs / design tables

- Element-level table: flows, pressures, *Kw*.
- Stage pressures and recoveries.
- Energy of high-pressure pumps.

## Science

[Membranes](../../explanation/membranes.md).
