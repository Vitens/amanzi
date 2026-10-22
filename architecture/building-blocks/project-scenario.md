---
id: bb-project-scenario
title: Project and Scenario
type: building-block
audience:
  - process-engineer
  - auditor
  - ai
status: outline
relates:
  - adr-0001
  - bb-amanzi-api
  - bb-solvers
  - bb-process-models
---

# Project and Scenario

Domain objects for a JSON project and one flowsheet run.

## Content to write

- **Paths:** `amanzi/core/project.py`, `amanzi/core/scenario.py`, `amanzi/core/database.py`.
- **In:** JSON/dict with `metadata`, `scenarios[]`, `key_figure_overwrites`.
- **Out:** instantiated models, connections, solver summaries, report structure.
- Model type → class via `type.capitalize()` and `amanzi.models` exports.
- **Owner:** TBD.
