---
id: adr-0003
title: Sequential solvers
type: adr
audience:
  - process-engineer
  - auditor
  - ai
status: outline
relates:
  - bb-solvers
  - bb-process-models
  - arc42-06
---

# ADR-0003 Sequential solvers

## Status

outline

## Context

- A plant model needs consistent flows before chemistry, heads before energy, and masses before CO₂.
- Recycle loops need iteration on quality.
- Cite when filling: `amanzi/core/scenario.py` run order; `amanzi/components/solvers/`.

## Decision

- Run exactly this order per scenario: **quantity → quality → hydraulics → energy → chemicals → sustainability**.
- Quality walks the graph with PHREEQC `Solution` plus extraneous micropollutants; iterate emitters/recycles until convergence or fail.
- Design view may invoke extra per-unit physics (`design()`) after a (partial) solve.

## Consequences

- Downstream numbers are accounting on top of hydraulic/quality results (key figures).
- Divergence is an error, not a silent skip.
- Design vs `run_quality` can differ (GAC PFAS — [arc42-11](../11-risks-and-technical-debt.md)).
