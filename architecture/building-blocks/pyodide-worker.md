---
id: bb-pyodide-worker
title: Pyodide worker
type: building-block
audience:
  - process-engineer
  - auditor
  - ai
status: draft
relates:
  - adr-0002
  - bb-amanzi-api
  - bb-vue-spa
  - arc42-07
---

# Pyodide worker

In-browser Python runtime that hosts `AmanziAPI` and PhreeqPython. Decision: [adr-0002](../decisions/0002-dual-execution-backends.md). Deployment: [arc42-07](../07-deployment-view.md).

## Repository

- Worker: `ui/src/backend/python.worker.js`
- Page-side client: `ui/src/backend/python.js` (creates the worker and `postMessage`s method calls)

## Interface

**In.** Messages `{id, method, args}` from the SPA. Methods: `initialize`, `parameters`, `keyfigures`, `report`, `design`, `solve`. `solve` and `design` and `report` pass the serialized project on `args`.

**Out.** `{id, result}` with the JSON already parsed, or `{id, error}`. During `initialize`, progress messages (`value`, `message`) drive the startup dialog (`ui/src/App.vue`).

Results are the same `AmanziAPI` methods Flask returns. There is no network server in this mode.

## Wheels

`initialize` loads Pyodide from `https://cdn.jsdelivr.net/pyodide/v<version>/full/`, then `micropip.install`s:

- `phreeqpython-1.6.2-py3-none-any.whl`
- the Amanzi wheel named by `VITE_AMANZI_WHEEL_FILENAME`, defaulting in source to `amanzi-1.0.5-py2.py3-none-any.whl` (`ui/src/backend/python.worker.js`)

Both files are fetched from `dist/` under the app base URL. CI places them there (`.github/workflows/deploy-ui.yml`). The worker then does `pyimport('amanzi.server.api')` and constructs `AmanziAPI`.

`ui/src/main.js` selects this backend unless `VITE_BACKEND` is `server`. The tagged UI release sets `VITE_BACKEND=pyodide`. Package version in `pyproject.toml` is `1.0.5`. The worker file’s comment history is not a release note; the workflow is the build that ships.

## Owner

**TBD.**
