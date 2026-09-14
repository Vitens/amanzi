---
title: Abstraction
type: reference
audience: everyone
status: outline
---

# Abstraction

Library name: **Abstraction**. Calculation type: groundwater. The source of raw water and its composition.

## Place it when

You need a starting point for the plant: wells, flow, and the analysis of the groundwater.

## Streams

- Out: product (raw water into the train).
- Emitter: defines the initial PHREEQC solution for downstream units.

## Inputs (UI groups)

- **General:** yearly production (Mm³), min/nominal/max capacity (m³/h).
- **Well design:** number of wells, average well capacity, elevation, groundwater level, drawdown, minor losses.
- **Composition:** pH, temperature; dissolved gases (O₂, N₂, CH₄, H₂S); cations/anions (Fe, Mn, NH₄, Ca, Mg, Na, Cl, HCO₃, NO₃, …) in mg/L.
- **Micropollutants:** PFAS, VOC, Other concentrations (see [Work with micropollutants](../../how-to/work-with-micropollutants.md)).

## Outputs / design tables

- Installed capacity and production.
- Hydraulic: head at well, head at treatment, required pump head, total headloss.
- Design checks: charge balance, oxygen demand, SI(Calcite), sc20.
- Energy of well pumps.

## Science

[Reading water quality](../../explanation/reading-water-quality.md), [How Amanzi calculates](../../explanation/how-amanzi-calculates.md).
