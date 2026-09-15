---
id: bb-parametric-yaml
title: Parametric YAML
type: building-block
audience:
  - process-engineer
  - auditor
  - ai
status: outline
relates:
  - adr-0004
  - bb-process-models
  - bb-vue-spa
---

# Parametric YAML

Declarative inputs, defaults, ranges, and output equations shared by UI and engine.

## Content to write

- **Path:** `amanzi/parametric/*.yml`; loader `amanzi/models/parametric/`.
- **In:** YAML layers listed on each model (`parametric_model = [...]`).
- **Out:** `input_parameters`, evaluated `output_parameters` (uom, `if`, validation).
- UI parameter forms are generated from the same schemas (via `/api/parameters`).
- **Owner:** TBD.
