---
id: bb-process-models
title: Process models
type: building-block
audience:
  - process-engineer
  - auditor
  - ai
status: outline
relates:
  - bb-parametric-yaml
  - bb-solvers
  - arc42-11
---

# Process models

Unit operations on the flowsheet (`Model` subclasses).

## Content to write

- **Path:** `amanzi/models/` (`__init__.py` export list is the catalog).
- Base: `models/model.py` extending parametric model; hydraulic mixins in `models/submodels/`.
- **In:** parameters from YAML + connections + incoming `Solution`.
- **Out:** `run_quality` / `design` / hydraulic equations.
- Science and literature: user docs Explanation — do not duplicate here.
- Known gap: GAC PFAS in design vs plant walk ([arc42-11](../11-risks-and-technical-debt.md)).
- **Owner:** TBD.
