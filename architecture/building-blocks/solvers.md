---
id: bb-solvers
title: Solvers
type: building-block
audience:
  - process-engineer
  - auditor
  - ai
status: draft
relates:
  - adr-0003
  - bb-process-models
  - arc42-06
---

# Solvers

Six sequential stages per scenario. Decision: [adr-0003](../decisions/0003-sequential-solvers.md). Runtime narrative: [arc42-06](../06-runtime-view.md).

## Repository

`amanzi/components/solvers/`. The package exports `QuantitySolver`, `QualitySolver`, `HydraulicSolver`, `EnergySolver`, `ChemicalSolver`, and `SustainabilitySolver` (`amanzi/components/solvers/__init__.py`). `Scenario` constructs them in that order (`amanzi/core/scenario.py`).

## Order and what each stage writes

`run_scenario` calls `solve(until)` on each solver. `until` is a model uid used by design to stop early (`amanzi/server/api.py`).

| Stage | File | What it sets |
| --- | --- | --- |
| Quantity | `quantitysolver.py` | Flows on connections and model `quantity` inflows and outflows. Linear mass balance. |
| Quality | `qualitysolver.py` | `model.quality` influent and effluent, using `run_quality`. |
| Hydraulics | `hydraulicsolver.py` | `hydraulics.head_in`, `head_out`, booster head and efficiency on connections. |
| Energy | `energysolver.py` | `model.energy` from parametric outputs whose category is `energy` and unit is `kWh/m3`, plus hydraulic loss summed from connection flow, head loss, and efficiency. |
| Chemicals | `chemicalsolver.py` | `model.chemicals` from outputs whose category is `chemicals` and unit is `gAS/m3`. |
| Sustainability | `sustainabilitysolver.py` | `model.sustainability` from outputs whose category is `sustainability` and unit is `gCO2-eq/m3`. |

The namespaces themselves are created on `Model` (`amanzi/models/model.py`): `quantity`, `quality`, `hydraulics`, `energy`, `chemicals`, `sustainability`.

## Quality iteration

`QualitySolver.max_iterations` is 100. `precision` is 0.0001 (`amanzi/components/solvers/qualitysolver.py`). Each pass walks `product`, then `flush`, then `waste`, from emitters, and propagates solutions. If convergence fails after 100 iterations the solver raises `Exception` and includes `self.error` in the message. It does not skip the scenario.

## Owner

**TBD.**
