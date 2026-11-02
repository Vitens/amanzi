---
id: arc42-04
title: Solution strategy
type: arc42
audience:
  - process-engineer
  - auditor
  - ai
status: draft
relates:
  - adr-0001
  - adr-0002
  - adr-0003
  - adr-0004
---

# 4. Solution strategy

The few decisions that shape the rest of the architecture. Detail belongs in the ADRs. This chapter only records the strategy and the path that implements it.

## GUI-first

The supported user path is the Vue 3 SPA in `ui/` (`ui/package.json`, `ui/src/main.js`). There is no scenario command-line interface (`pyproject.toml` scripts). See [bb-vue-spa](building-blocks/vue-spa.md).

## JSON as system of record

A project is a JSON document the user keeps, not a row in a server database. The SPA serializes it (`ui/src/stores/project.js`). Every `solve`, `design`, and `report` builds a new `Project` from that document (`amanzi/server/api.py`). Decision: [adr-0001](decisions/0001-json-project-as-system-of-record.md). Block: [bb-project-scenario](building-blocks/project-scenario.md).

## Dual execution

Pyodide, Flask, and Lambda all call `AmanziAPI`. The SPA picks Pyodide unless `VITE_BACKEND` is `server` (`ui/src/main.js`). Decision: [adr-0002](decisions/0002-dual-execution-backends.md). Blocks: [bb-pyodide-worker](building-blocks/pyodide-worker.md), [bb-flask-server](building-blocks/flask-server.md), [bb-lambda](building-blocks/lambda.md).

## Sequential solvers

Each scenario runs quantity, then quality, then hydraulics, then energy, then chemicals, then sustainability (`amanzi/core/scenario.py`). Decision: [adr-0003](decisions/0003-sequential-solvers.md). Block: [bb-solvers](building-blocks/solvers.md).

## YAML parametrics

Input schemas and many output equations live in `amanzi/parametric/*.yml`. A model lists the layers it loads (`parametric_model` on classes in `amanzi/models/`). The SPA receives schemas from `AmanziAPI.parameters()` rather than hard-coding every field. Decision: [adr-0004](decisions/0004-yaml-parametric-models.md). Block: [bb-parametric-yaml](building-blocks/parametric-yaml.md).

## Chemistry split

PHREEQC tracks the inorganic solution (`amanzi/core/scenario.py`, `amanzi/components/solution.py`). Micropollutants travel beside that solution. Groundwater attaches an extraneous dict — `Color`, `TOC`, `PFAS`, `VOC`, `Other` — as the second argument to `PhreeqPython.add_solution` (`amanzi/models/groundwater.py`). Those keys are not PHREEQC database species. Science of the isotherms and mass-transfer correlations stays in `docs/en/explanation/`.
