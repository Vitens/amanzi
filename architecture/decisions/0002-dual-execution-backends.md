---
id: adr-0002
title: Dual execution backends
type: adr
audience:
  - process-engineer
  - auditor
  - ai
status: draft
relates:
  - adr-0001
  - bb-pyodide-worker
  - bb-flask-server
  - bb-lambda
  - bb-amanzi-api
---

# ADR-0002 Dual execution backends

## Status

draft

## Context

- End users should run without installing Python. `changelog.md` records that, from 1.0.4, scenarios run in the browser with Pyodide and a Python server is no longer required.
- Developers need a local server. `amanzi-server` is the Flask entry (`pyproject.toml`, `amanzi/server/app.py`). Vite dev points at it when `VITE_BACKEND` is `server` (`ui/src/main.js`, `ui/.env.development`).
- A hosted HTTP API is still possible. `lambda/lambda_function.py` maps API Gateway events onto the same class.
- The switch is `VITE_BACKEND` in `ui/src/main.js`. The worker is `ui/src/backend/python.worker.js`.

## Decision

- All backends call the same `AmanziAPI` (`amanzi/server/api.py`).
- Default for the released UI: Pyodide worker. `.github/workflows/deploy-ui.yml` sets `VITE_BACKEND=pyodide`. `ui/src/main.js` uses the worker unless `VITE_BACKEND` is `server`.
- Development: Flask `amanzi-server` plus Vite, with `VITE_BACKEND=server`.
- Optional production API: AWS Lambda (`lambda/lambda_function.py`, `lambda/Dockerfile`) with the same methods, plus a `version` read of the `VERSION` file copied into the image.

## Consequences

- Behaviour must stay aligned across three hosts. There is no test suite that checks that alignment ([arc42-11](../11-risks-and-technical-debt.md)).
- The wheel and Pyodide supply chain is part of deployment ([arc42-07](../07-deployment-view.md), `.github/workflows/deploy-ui.yml`).
- Which backend `demo.amanzi.app` uses is **TBD**. The URL is named in `README.md`. The release zip is the Pyodide build; that does not prove what the demo host serves.
- Blocks: [bb-pyodide-worker](../building-blocks/pyodide-worker.md), [bb-flask-server](../building-blocks/flask-server.md), [bb-lambda](../building-blocks/lambda.md), [bb-amanzi-api](../building-blocks/amanzi-api.md).
