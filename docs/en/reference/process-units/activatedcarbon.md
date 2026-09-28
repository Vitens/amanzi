---
title: Activated carbon
type: reference
audience: everyone
status: outline
---

# Activated carbon

Library name: **Activated carbon**. GAC contactors for PFAS and organic micropollutants (TOC, colour), including replacement and staggering in **design view**.

## Place it when

You are sizing or comparing GAC for PFAS or organic micropollutant removal.

## Streams

- In: product.
- Out: product; flush if filtration/backwash anchors are used.

## Inputs (UI groups)

- **Filter geometry:** rectangular/circular, length/width or diameter, bed height.
- **Carbon:** packing type (NORIT-Supra options), apparent density, particle diameter, porosity (clean/clogged).
- **PFAS / micropollutants:** Freundlich *K* and *1/n* per compound, competition coefficients, PEQ, design limit, mass-transfer coefficient, removal % from metadata.
- **Replacement / staggering:** interval and number of filters in rotation.
- Optional spray aeration fields when enabled.

## Outputs / design tables

- Breakthrough curves, regeneration interval (days or BV), EBCT, influent/effluent OMV, competition coefficients.
- Energy / chemicals / sustainability for carbon replacement.

## Limitation

Plant-wide `run_quality` does not currently apply PFAS removal; use design view. See [Limitations](../limitations.md).

## Science

[Activated carbon and PFAS](../../explanation/activated-carbon-and-pfas.md).
