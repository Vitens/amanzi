---
id: adr-0001
title: JSON project as system of record
type: adr
audience:
  - process-engineer
  - auditor
  - ai
status: outline
relates:
  - adr-0002
  - bb-project-scenario
  - bb-vue-spa
---

# ADR-0001 JSON project as system of record

## Status

outline

## Context

- Users must share and version plant designs without accounts.
- The UI, Pyodide, Flask, and Lambda must see the same payload.
- Cite when filling: `ui/src/stores/project.js` serialize; `amanzi/core/project.py`; default `ui/src/assets/Default-project.json`.

## Decision

- A project is a JSON document (file download/upload and in-memory dict).
- It contains metadata, key-figure overwrites, and `scenarios[]` with models, connections, and scenario metadata.
- The calculation engine is stateless: each `solve` / `design` / `report` receives a complete document.

## Consequences

- Reproducibility is “same JSON + same Amanzi/PHREEQC versions” (quality numbers TBD in [arc42-10](../10-quality-requirements.md)).
- Schema evolution needs migration (`ui/src/lib/projectMigration.js`).
- No server-side project database in the product.
