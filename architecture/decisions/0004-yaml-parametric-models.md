---
id: adr-0004
title: YAML parametric models
type: adr
audience:
  - process-engineer
  - auditor
  - ai
status: outline
relates:
  - bb-parametric-yaml
  - bb-process-models
  - bb-vue-spa
---

# ADR-0004 YAML parametric models

## Status

outline

## Context

- Process units share capacities, elevations, and sustainability outputs.
- The UI needs schemas (defaults, ranges, conditional fields) without duplicating Python.
- Cite when filling: `amanzi/parametric/*.yml`; `amanzi/models/parametric/parametric.py`; `output.py`.

## Decision

- Each model declares YAML layers (`parametric_model = ['base', 'model', …]`).
- YAML defines input parameters and output equations (`uom`, `if`, `validation`).
- The SPA loads schemas through `AmanziAPI.parameters()` rather than hard-coding every field.

## Consequences

- Changing a YAML file changes both calculation outputs and the form (after rebuild/reload).
- Equation engine is a cross-cutting concept ([arc42-08](../08-crosscutting-concepts.md)).
- Auto-generated user-doc parameter tables were a MyST plugin; not used on this architecture site.
