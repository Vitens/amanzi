---
title: Tower aeration
type: reference
audience: everyone
status: outline
---

# Tower aeration

Library name: **Tower Aeration**. Counter-current packed tower for CO₂, CH₄, O₂ transfer and VOC stripping.

## Place it when

You need packed-tower gas transfer (degassing methane/CO₂, adding oxygen, stripping VOC).

## Streams

- In/out: product (no waste stream).

## Inputs (UI groups)

- **Tower:** diameter, bed height, packing (Raflux25 / 50 / 90), blower efficiency.
- **Hydraulic line:** nozzle pressure loss, fall height.
- **Operational:** RQ, ambient temperature, min/nom/max as inherited.
- VOC list comes from upstream extraneous composition.

## Outputs / design tables

- Removal fractions and O₂ addition on the product stream.
- Design: flooding / operating charts, pressure drop, VOC curves.
- Blower energy (isentropic compression).

## Science

[Aeration](../../explanation/aeration.md).
