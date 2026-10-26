---
id: bb-amanzi-api
title: AmanziAPI
type: building-block
audience:
  - process-engineer
  - auditor
  - ai
status: draft
relates:
  - c4-components
  - bb-project-scenario
  - bb-flask-server
  - bb-lambda
  - bb-pyodide-worker
---

# AmanziAPI

Single façade for the Vue SPA, Flask, Lambda, and the Pyodide worker (`amanzi/server/api.py`). The class docstring states it can be called as a Flask application or through a Lambda function. The Pyodide worker imports the same class (`ui/src/backend/python.worker.js`).

## Repository

`amanzi/server/api.py`. HTTP adapters: `amanzi/server/app.py`, `lambda/lambda_function.py`. In-browser adapter: `ui/src/backend/python.worker.js`.

## Interface

**In.** A project dict or JSON string, a scenario index, and for design a model uid. `solve`, `design`, and `report` parse a string with `json.loads` when needed.

**Out.** A JSON string.

| Method | Returns |
| --- | --- |
| `parameters()` | Map of model type → input parameter list. Built by instantiating each exported `ParametricModel` subclass except `Model` (`amanzi/models/__init__.py`). |
| `keyfigures()` | `{rows: ...}` from `Database.rows` (`amanzi/core/database.py`). |
| `solve(data, scenario)` | Connection quantity and hydraulics, model hydraulics, and metric summaries from the quantity, energy, quality, and sustainability solvers. |
| `design(data, scenario, model)` | Hydraulics for the partial run, plus `run_design()` on that model. |
| `report(data)` | `Project.report()`: scenario names and per-scenario solver summaries. |

The class does not contain solver math. `solve` constructs `Project` and calls `Scenario.run_scenario` (`amanzi/core/project.py`, `amanzi/core/scenario.py`).

## Owner

**TBD.**
