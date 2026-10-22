---
id: arc42-10
title: Quality requirements
type: arc42
audience:
  - auditor
  - process-engineer
  - ai
status: outline
relates:
  - arc42-01
  - arc42-11
---

# 10. Quality requirements

Scenarios and metrics. Numbers are **TBD** until Vitens supplies them.

## Content to write

Quality scenarios (stimulus → response), not UI tutorials:

- **Calculation correctness:** given a known project JSON, solvers produce results within TBD tolerance; cite how that would be tested (there is currently **no** test suite — [arc42-11](11-risks-and-technical-debt.md)).
- **Explainability:** an auditor can trace a reported number to a solver step, a parametric equation, or a key figure (TBD evidence format).
- **Reproducibility:** the same JSON + Amanzi version yields the same report (TBD: floating point, PHREEQC version pin).
- **Pyodide load time:** first paint / engine ready (TBD budget).
- **Solve time:** plant-wide solve on the demo project (TBD budget).
- **Scientific validation:** process for accepting a new model or isotherm (TBD).
- **Availability:** hosted demo (TBD RTO/RPO).

Use a table when filling: scenario | measure | target | current | evidence path.
