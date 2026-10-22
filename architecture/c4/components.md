---
id: c4-components
title: C4 components
type: c4
audience:
  - process-engineer
  - auditor
  - ai
status: outline
relates:
  - c4-containers
  - bb-amanzi-api
  - bb-solvers
---

# C4 components

Inside the calculation container and the SPA. Each node maps to a building-block page or a data file.

## Diagram

```mermaid
flowchart TB
  subgraph spa [VueSPA]
    canvas[Canvas]
    stores[PiniaStores]
  end
  subgraph calc [CalculationContainer]
    api[AmanziAPI]
    project[ProjectScenario]
    solvers[Solvers]
    models[ProcessModels]
    parametric[ParametricYAML]
    phreeqc[PHREEQC]
    csvDb[CsvDatabases]
  end
  canvas --> stores
  stores --> api
  api --> project
  project --> solvers
  solvers --> models
  models --> parametric
  models --> phreeqc
  solvers --> csvDb
```

## Legend

- `Canvas` / `PiniaStores` — `ui/src/components`, `ui/src/stores/`.
- `AmanziAPI` — `amanzi/server/api.py` (`bb-amanzi-api`).
- `ProjectScenario` — `amanzi/core/` (`bb-project-scenario`).
- `Solvers` — `amanzi/components/solvers/` (`bb-solvers`).
- `ProcessModels` — `amanzi/models/` (`bb-process-models`).
- `ParametricYAML` — `amanzi/parametric/` (`bb-parametric-yaml`).
- `PHREEQC` — PhreeqPython `Solution`.
- `CsvDatabases` — `amanzi/database/`, `membranestack/membrane_database.csv`.

## Content to write

- HTTP methods on `AmanziAPI` (`parameters`, `keyfigures`, `solve`, `design`, `report`).
- That the SPA never imports model classes directly.
