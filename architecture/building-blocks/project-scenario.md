---
id: bb-project-scenario
title: Project and Scenario
type: building-block
audience:
  - process-engineer
  - auditor
  - ai
status: draft
relates:
  - adr-0001
  - bb-amanzi-api
  - bb-solvers
  - bb-process-models
---

# Project and Scenario

Domain objects for a JSON project and one flowsheet run. Decision: [adr-0001](../decisions/0001-json-project-as-system-of-record.md).

## Repository

- `amanzi/core/project.py` — `Project`
- `amanzi/core/scenario.py` — `Scenario`
- `amanzi/core/database.py` — `Database` (key figures)

The SPA mirror of the same document is `ui/src/stores/project.js` and `ui/src/stores/scenario.js`.

## Interface

**In.** `Project` accepts a dict or a filesystem path (`Project.load_file`). The backends pass the dict from the request (`amanzi/server/api.py`). The dict written by `projectStore.serialize` has:

- `metadata` — `version`, `amanzi_version`, `project_name`, `canvas` (`ui/src/stores/project.js`)
- `key_figure_overwrites`
- `scenarios[]` — each from `scenarioStore.serialize`: `name`, `notes`, `scenario_version`, `models`, `connections`, `metaData`, `key_figure_overwrites` (`ui/src/stores/scenario.js`)

**Out.** `Project.load_scenarios` builds one `Scenario` per entry. `Scenario` instantiates models and connections, applies key-figure overwrites, and holds the solver map. `Scenario.report` runs the solvers and returns summaries plus a model order. `Project.report` collects that for every scenario.

## Model lookup

`Scenario.load_models` takes `model['type']`, applies `str.capitalize`, and `getattr` on the `amanzi.models` module (`amanzi/core/scenario.py`). The catalog of classes is the import list in `amanzi/models/__init__.py`. A type that is not exported (ion exchange today) cannot be constructed. See [arc42-11](../11-risks-and-technical-debt.md).

Connections are `amanzi.components.connection.Connection`, assigned back onto the models (`Scenario.load_connections`).

## Owner

**TBD.**
