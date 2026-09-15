---
id: bb-pyodide-worker
title: Pyodide worker
type: building-block
audience:
  - process-engineer
  - auditor
  - ai
status: outline
relates:
  - adr-0002
  - bb-amanzi-api
  - bb-vue-spa
  - arc42-07
---

# Pyodide worker

In-browser Python runtime that hosts `AmanziAPI` and PhreeqPython.

## Content to write

- **Path:** `ui/src/backend/python.worker.js`.
- **In:** serialized project messages from the SPA.
- **Out:** same API results as Flask, without a network server.
- Wheels bundled in the UI release (cite deploy workflow when filling).
- Default production path since v1.0.4.
- **Owner:** TBD.
