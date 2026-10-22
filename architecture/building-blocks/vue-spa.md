---
id: bb-vue-spa
title: Vue SPA
type: building-block
audience:
  - process-engineer
  - ai
status: outline
relates:
  - c4-containers
  - bb-pyodide-worker
  - bb-flask-server
---

# Vue SPA

The only end-user interface.

## Content to write

- **Path:** `ui/` — Vue 3, Vite, Pinia, Element Plus, Chart.js, vue-i18n.
- **In:** user gestures; project JSON; API/worker results.
- **Out:** serialized project; `solve` / `design` / `report` calls (`ui/src/stores/project.js`).
- Backend switch: `VITE_BACKEND` in `ui/src/main.js`.
- Does not import Python model classes.
- **Owner:** TBD.
