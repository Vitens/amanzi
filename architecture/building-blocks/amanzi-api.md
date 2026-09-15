---
id: bb-amanzi-api
title: AmanziAPI
type: building-block
audience:
  - process-engineer
  - auditor
  - ai
status: outline
relates:
  - c4-components
  - bb-project-scenario
  - bb-flask-server
  - bb-lambda
  - bb-pyodide-worker
---

# AmanziAPI

Single façade for UI, Flask, Lambda, and the Pyodide worker.

## Content to write

- **Path:** `amanzi/server/api.py`.
- **In:** project dict/JSON; scenario index; optional model uid for design.
- **Out:** parameter schemas, key figures, solve results, design payload, multi-scenario report.
- **Methods:** `parameters()`, `keyfigures()`, `solve()`, `design()`, `report()`.
- **Owner:** TBD.
- Does not contain solver math; delegates to `Project` / `Scenario`.
