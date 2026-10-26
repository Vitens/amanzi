---
id: adr-0001
title: JSON project as system of record
type: adr
audience:
  - process-engineer
  - auditor
  - ai
status: draft
relates:
  - adr-0002
  - bb-project-scenario
  - bb-vue-spa
---

# ADR-0001 JSON project as system of record

## Status

draft

## Context

- Users share and version plant designs without accounts. The SPA writes the document to `localStorage` and to a downloaded file (`ui/src/stores/project.js`, `ui/src/components/MenuBar.vue`). There is no project table in `amanzi/server/`.
- The UI, the Pyodide worker, Flask, and Lambda must see the same payload. Each of `solve`, `design`, and `report` receives that payload and constructs `Project` (`amanzi/server/api.py`).
- The shape the SPA writes is `metadata`, `key_figure_overwrites`, and `scenarios[]` (`ui/src/stores/project.js`). Defaults shipped with the app are `ui/src/assets/Default-project-EN.json`, `Default-project-NL.json`, and `Default-project-DE.json` (`ui/src/App.vue`).

## Decision

- A project is a JSON document (file download or upload, and an in-memory dict). It is not a row in a server database.
- It contains metadata, key-figure overwrites, and `scenarios[]` with models, connections, and scenario metadata (`ui/src/stores/scenario.js` `serialize`).
- The calculation engine is stateless across requests: each `solve`, `design`, or `report` builds a new `Project` from the complete document (`amanzi/server/api.py`). `Project.load_file` also accepts a dict, so the server does not need a path (`amanzi/core/project.py`).

## Consequences

- Reproducibility means the same JSON and the same Amanzi and PHREEQC versions. Numeric tolerances are **TBD** in [arc42-10](../10-quality-requirements.md). PhreeqPython is pinned in `pyproject.toml`.
- Schema changes need a forward migration (`ui/src/lib/projectMigration.js`, log in `ui/src/lib/migrationConfig.js`).
- No server-side project database is part of the product. Confidentiality of a design is the handling of the JSON file ([arc42-11](../11-risks-and-technical-debt.md)).
- Block page: [bb-project-scenario](../building-blocks/project-scenario.md).
