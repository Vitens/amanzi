---
id: bb-solvers
title: Solvers
type: building-block
audience:
  - process-engineer
  - auditor
  - ai
status: outline
relates:
  - adr-0003
  - bb-process-models
  - arc42-06
---

# Solvers

Six sequential stages per scenario.

## Content to write

- **Path:** `amanzi/components/solvers/`.
- **Order:** Quantity → Quality → Hydraulics → Energy → Chemicals → Sustainability.
- Quality iterates emitters/recycles (up to 100, precision 0.0001) — confirm numbers when filling from `qualitysolver.py`.
- **In:** wired `Scenario` with models and connections.
- **Out:** namespaces on each model (`quantity`, `quality`, `hydraulics`, `energy`, `chemicals`, `sustainability`).
- **Owner:** TBD.
