---
id: adr-0003
title: Sequential solvers
type: adr
audience:
  - process-engineer
  - auditor
  - ai
status: draft
relates:
  - bb-solvers
  - bb-process-models
  - arc42-06
---

# ADR-0003 Sequential solvers

## Status

draft

## Context

- Flows have to exist before chemistry can mix them, heads before pump energy, and masses before CO₂ factors. Energy reads quantity and hydraulics (`amanzi/components/solvers/energysolver.py`). Sustainability reads quantity (`amanzi/components/solvers/sustainabilitysolver.py`). Chemicals read parametric outputs that themselves sit on the solved model (`amanzi/components/solvers/chemicalsolver.py`).
- Recycle loops need iteration on quality. `QualitySolver` repeats the graph until mass balance is within `precision` or it raises (`amanzi/components/solvers/qualitysolver.py`).
- The order is fixed in one place: the `OrderedDict` on `Scenario` (`amanzi/core/scenario.py`). Implementations are `amanzi/components/solvers/`.

## Decision

- Run exactly this order per scenario: **quantity → quality → hydraulics → energy → chemicals → sustainability** (`amanzi/core/scenario.py`).
- Quality walks `product`, then `flush`, then `waste`, carrying a PHREEQC `Solution` plus the extraneous micropollutant dict created with the groundwater solution (`amanzi/components/solvers/qualitysolver.py`, `amanzi/models/groundwater.py`). It iterates until convergence or fails after 100 passes at precision 0.0001.
- Design may stop the chain at one model (`run_scenario(until=model)`) and then call `run_design` (`amanzi/server/api.py`). That path can run extra per-unit physics. It is not a seventh solver.

## Consequences

- Downstream numbers are accounting on top of quantity, quality, and hydraulics, using key figures and YAML outputs (`amanzi/core/database.py`, `amanzi/models/parametric/output.py`).
- Divergence is an error. `QualitySolver.solve` raises `Exception` rather than returning a partial plant (`amanzi/components/solvers/qualitysolver.py`).
- `design()` and `run_quality()` can disagree. Activated-carbon PFAS breakthrough is the current case ([arc42-11](../11-risks-and-technical-debt.md), `amanzi/models/activatedcarbon.py`).
- Block: [bb-solvers](../building-blocks/solvers.md). Runtime: [arc42-06](../06-runtime-view.md).
