---
id: bb-vue-spa
title: Vue SPA
type: building-block
audience:
  - process-engineer
  - ai
status: draft
relates:
  - c4-containers
  - bb-pyodide-worker
  - bb-flask-server
---

# Vue SPA

The only end-user interface (`README.md`, `ui/`).

## Repository

`ui/`. Runtime libraries in `ui/package.json`: Vue 3, Vite, Pinia, Element Plus, Chart.js, vue-i18n. Entry: `ui/src/main.js`.

## Interface

**In.** User edits on the canvas; a project JSON from `localStorage` or from `ui/src/assets/Default-project-EN.json` (and the NL and DE files); results from the backend.

**Out.** `projectStore.serialize()` (`ui/src/stores/project.js`) and one of `backend.solve`, `backend.design`, or `backend.report`. The choice is in `solveDebounced` in that same file. See [arc42-06](../06-runtime-view.md).

## Backend switch

`ui/src/main.js`: if `import.meta.env.VITE_BACKEND == 'server'`, the global backend is `ui/src/backend/server.js`. Otherwise it is `ui/src/backend/python.js` (the Pyodide worker). The release workflow sets `VITE_BACKEND=pyodide` (`.github/workflows/deploy-ui.yml`).

## What it does not do

It does not import Python model classes. `loadModels` in `ui/src/main.js` registers Vue single-file components from `ui/src/models/*/*.vue`. Parameter schemas come from `backend.parameters()`.

Locales `en`, `nl`, `de`, and `fr` are loaded in `ui/src/main.js`. PostHog is installed only outside Vite development mode.

## Owner

**TBD.**
