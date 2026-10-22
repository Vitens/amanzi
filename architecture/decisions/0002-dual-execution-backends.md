---
id: adr-0002
title: Dual execution backends
type: adr
audience:
  - process-engineer
  - auditor
  - ai
status: outline
relates:
  - adr-0001
  - bb-pyodide-worker
  - bb-flask-server
  - bb-lambda
  - bb-amanzi-api
---

# ADR-0002 Dual execution backends

## Status

outline

## Context

- End users should run without installing Python (v1.0.4+).
- Developers need hot reload and easier debugging.
- Hosted services may want a server-side API.
- Cite when filling: `ui/src/main.js` `VITE_BACKEND`; `python.worker.js`; `amanzi/server/app.py`; `lambda/lambda_function.py`.

## Decision

- All backends call the same `AmanziAPI`.
- Production default: Pyodide worker in the browser.
- Development: Flask `amanzi-server` + Vite.
- Optional production API: AWS Lambda with the same methods.

## Consequences

- Behaviour must stay aligned across three hosts (no test suite yet — [arc42-11](../11-risks-and-technical-debt.md)).
- Wheel/Pyodide supply chain is part of deployment ([arc42-07](../07-deployment-view.md)).
- Which backend `demo.amanzi.app` uses is TBD.
