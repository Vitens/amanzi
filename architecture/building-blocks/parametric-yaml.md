---
id: bb-parametric-yaml
title: Parametric YAML
type: building-block
audience:
  - process-engineer
  - auditor
  - ai
status: draft
relates:
  - adr-0004
  - bb-process-models
  - bb-vue-spa
---

# Parametric YAML

Declarative inputs, defaults, and output equations shared by the UI and the engine. Decision: [adr-0004](../decisions/0004-yaml-parametric-models.md).

## Repository

- Files: `amanzi/parametric/*.yml` (loaded as package data `amanzi.parametric`).
- Loader: `amanzi/models/parametric/parametric.py` (`ParametricModel`).
- Equation objects: `amanzi/models/parametric/output.py` (`Output`).

`ParametricModel.parse_yaml` opens `amanzi.parametric/<filename>.yml` with `importlib.resources`.

## Interface

**In.** Each model class sets `parametric_model` to a list of YAML stems, for example `['base', 'model', 'activatedcarbon', 'filtration', 'pfas', 'micropollutants']` on `Activatedcarbon` (`amanzi/models/activatedcarbon.py`). Later files merge onto earlier ones when a parameter name collides (`process_parameters`).

**Out.**

- `input_parameters` — ordered map of fields (section, category, namespace, defaults). `AmanziAPI.parameters` serialises these for the SPA (`amanzi/server/api.py`).
- `output_parameters` — `Output` objects. `calculate` evaluates the `equation` string with `ast` (`amanzi/models/parametric/output.py`). `uom` is metadata. `if` hides the output when the expression is false (`Output.hidden`). `validation` is a boolean expression (`Output.validate`).

Missing keys in the project JSON are filled from YAML `default` (`ParametricModel.__init__`).

The SPA does not parse these YAML files itself. Forms use the JSON from `/api/parameters` or the worker equivalent (`ui/src/stores/project.js` `loadParameters`). Changing a YAML file changes both calculated outputs and the form after the Python package is reloaded.

## Owner

**TBD.**
