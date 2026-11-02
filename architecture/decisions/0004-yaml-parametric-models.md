---
id: adr-0004
title: YAML parametric models
type: adr
audience:
  - process-engineer
  - auditor
  - ai
status: draft
relates:
  - bb-parametric-yaml
  - bb-process-models
  - bb-vue-spa
---

# ADR-0004 YAML parametric models

## Status

draft

## Context

- Process units share capacities, elevations, and sustainability outputs. Those shared fields live in `amanzi/parametric/base.yml` and `amanzi/parametric/model.yml`, and unit files add their own.
- The UI needs defaults, units, and conditional fields without a second copy of every number in Vue. `AmanziAPI.parameters` walks the exported model classes and returns `input_parameters` (`amanzi/server/api.py`).
- Output equations, `uom`, `if`, and `validation` are parsed in `amanzi/models/parametric/parametric.py` and evaluated in `amanzi/models/parametric/output.py`.

## Decision

- Each model declares YAML layers on the class: `parametric_model = ['base', 'model', …]` (example: `amanzi/models/activatedcarbon.py`).
- YAML defines input parameters and output equations. Visibility uses `if`. Checks use `validation`. Units use `uom` (`amanzi/parametric/base.yml`, `amanzi/models/parametric/output.py`).
- The SPA loads schemas through `AmanziAPI.parameters()` (`ui/src/stores/project.js` `loadParameters`). It does not hard-code the engineering fields that YAML already defines. Vue files under `ui/src/models/` are layout and charts, not a second parameter database.

## Consequences

- Changing a YAML file changes both calculation outputs and the form, after the Python package is reloaded (worker wheels or the Flask process).
- The equation engine is a cross-cutting concept ([arc42-08](../08-crosscutting-concepts.md), [bb-parametric-yaml](../building-blocks/parametric-yaml.md)).
- User-doc parameter tables are not generated on this architecture site. Science stays in `docs/en/explanation/` and `docs/en/reference/`.
