---
id: c4-containers
title: C4 containers
type: c4
audience:
  - process-engineer
  - auditor
  - ai
status: outline
relates:
  - c4-context
  - c4-components
  - arc42-05
---

# C4 containers

Runnable / deployable pieces. Only one calculation container is active per session (Pyodide **or** Flask **or** Lambda).

## Diagram

```mermaid
flowchart TB
  designer[Designer]
  spa[VueSPA]
  pyodide[PyodideWorker]
  flask[FlaskServer]
  lambda[Lambda]
  jsonFile[ProjectJSON]
  yamlDb[ParametricYAML]
  csvDb[CsvDatabases]
  phreeqc[PHREEQC]
  designer --> spa
  spa --> jsonFile
  spa --> pyodide
  spa --> flask
  spa --> lambda
  pyodide --> phreeqc
  flask --> phreeqc
  lambda --> phreeqc
  pyodide --> yamlDb
  flask --> yamlDb
  lambda --> yamlDb
  pyodide --> csvDb
  flask --> csvDb
  lambda --> csvDb
```

## Legend

- `VueSPA` — `ui/` (Vite, Vue 3, Pinia, Element Plus).
- `PyodideWorker` — `ui/src/backend/python.worker.js`.
- `FlaskServer` — `amanzi/server/app.py` (`amanzi-server`).
- `Lambda` — `lambda/lambda_function.py`.
- `ProjectJSON` — user file / localStorage.
- `ParametricYAML` — `amanzi/parametric/`.
- `CsvDatabases` — key figures, PFAS isotherms, membrane database.

## Content to write

- Protocol on each edge (in-process worker vs HTTP `/api/*`).
- Which container holds PHREEQC in each deployment.
