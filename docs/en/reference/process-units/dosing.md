---
lang: en
title: Chemical dosage
type: reference
audience: everyone
status: draft
---

# Chemical dosage

Library name: **Chemical Dosage**. One chemical, either a fixed dose or a search toward a target.

## Place it when

The water needs an acid, a base, CO₂, oxygen, or a metal salt, and a pellet reactor is the wrong block.

## Streams

In: product. Out: product.

## Inputs

| Field | Default | Choices or range |
|---|---|---|
| `position` | influent | influent, effluent |
| `chemical` | co2 | co2, hcl, h2so4, lye, lime, calcite, oxygen, iron_chloride, manganese_chloride |
| `mode` | constant | constant, setpoint |
| `dosage` | 0.2 mmol/L | 0–5. Shown in constant mode |
| `setpoint_parameter` | pH | pH, SI, AggCO2, CCPP90. Shown in setpoint mode |
| `setpoint` | 7 | 0–14. Shown in setpoint mode |

The constant dose is accepted when Enter is pressed. In setpoint mode the search stays inside 0–5 mmol/L. If it fails, the dose stays 0 and the unit sets a warning.

## What it reports

Formula, formula weight (g AS/mol), dose (mmol/L), and mass dose (g AS/m³). The design view plots pH, oxygen, aggressive CO₂, SI, and TACC₉₀ against dose from 0 to 2 mmol/L.

## Science

[Softening and dosing](../../explanation/softening-and-dosing.md).
