---
id: bb-process-models
title: Process models
type: building-block
audience:
  - process-engineer
  - auditor
  - ai
status: draft
relates:
  - bb-parametric-yaml
  - bb-solvers
  - arc42-11
---

# Process models

Unit operations on the flowsheet. Each is a `Model` subclass (`amanzi/models/model.py`), and `Model` extends `ParametricModel` (`amanzi/models/parametric/parametric.py`).

## Repository

`amanzi/models/`. The catalog the engine can construct is the import list in `amanzi/models/__init__.py`:

sand filtration, membrane, groundwater, reservoir, output, waste, softening, plate, recycle, splitter, vacuum, cascade, dosing, membrane degassing, tower aeration, activated carbon, marble filtration, sand trap, pipeline.

Ion exchange is implemented in `amanzi/models/ionexchange.py` and commented out of that list. See [arc42-11](../11-risks-and-technical-debt.md).

Shared equation helpers live in `amanzi/models/submodels/` (`Loss`, `Balance`, `Splitter`). An unused alternative marble-filtration module sits in `amanzi/models/alternative_models/` and is not imported by `amanzi/models/__init__.py`.

## Interface

**In.**

- Parameters from the model’s YAML layers (`parametric_model = [...]` on the class) merged with `configuration.parameters` in the JSON (`amanzi/models/parametric/parametric.py`).
- Connections attached by `Scenario.load_connections` (`amanzi/core/scenario.py`).
- An incoming PHREEQC `Solution` (plus extraneous composition) when a solver calls `run_quality`.

**Out.**

- `run_quality(type, total_inflow, solution)` — plant-walk water quality. The base class logs a warning and returns the solution unchanged (`amanzi/models/model.py`).
- `design()` — extra payload for the design view. The base class returns `{}`. `run_design` adds parameters, tables, evaluated outputs, and quality summaries (`amanzi/models/model.py`).
- Hydraulic equations via properties such as `equations` on units that participate in the quantity matrix (for example `amanzi/models/groundwater.py`, `amanzi/models/submodels/loss.py`).

Science and literature stay in `docs/en/explanation/`. Do not copy isotherm or mass-transfer derivations onto this page.

## Known gap

Activated-carbon PFAS breakthrough runs in `design`, not in `run_quality` (`amanzi/models/activatedcarbon.py`). Detail: [arc42-11](../11-risks-and-technical-debt.md).

## Owner

**TBD.**
