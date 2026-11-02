---
id: arc42-10
title: Quality requirements
type: arc42
audience:
  - auditor
  - process-engineer
  - ai
status: draft
relates:
  - arc42-01
  - arc42-11
---

# 10. Quality requirements

Quality scenarios (stimulus and the response the architecture aims for). These are not UI tutorials. **Targets are TBD** until Vitens supplies numbers. Do not treat an empty target as a passed control ([arc42-11](11-risks-and-technical-debt.md)).

The repository has no Python test package: no `tests/` tree and no `test_*.py` modules. A scenario that says “within tolerance” cannot point at a green test today.

| Scenario | Measure | Target | Current | Evidence path |
| --- | --- | --- | --- | --- |
| Calculation correctness | Given a known project JSON, solver outputs match an agreed reference | **TBD** tolerance | No automated comparison | `amanzi/server/api.py` `solve`; absence of a test suite |
| Explainability | An auditor can trace a reported number to a solver step, a parametric equation, or a key figure | **TBD** evidence format | Equations are on output objects; the report returns solver summaries | `amanzi/models/parametric/output.py`; `amanzi/core/scenario.py` `report`; `amanzi/database/key_figures.csv` |
| Reproducibility | Same JSON and same Amanzi build yield the same report | **TBD** (floating point, PHREEQC pin) | PhreeqPython is pinned to 1.6.2. Float policy is not written down | `pyproject.toml`; `.github/workflows/deploy-ui.yml` |
| Pyodide load | Time until the engine reports ready | **TBD** budget | Worker posts progress 0–100 while loading wheels | `ui/src/backend/python.worker.js`; dialog in `ui/src/App.vue` |
| Solve time | Plant-wide solve of the bundled demo project | **TBD** budget | Debounce is 200 ms before the call; solve duration is not budgeted | `ui/src/stores/project.js`; `ui/src/assets/Default-project-EN.json` |
| Scientific validation | Process for accepting a new model or isotherm | **TBD** | PFAS isotherm CSV and a build script exist; no acceptance checklist in-repo | `amanzi/database/pfas_isotherms.csv`; `amanzi/database/pfas_isotherms_README.md` |
| Availability | Hosted demo stays usable | **TBD** RTO/RPO | Demo URL is named; no availability target is in the workflows | `README.md`; `.github/workflows/deploy-ui.yml` |

Literature for process units is in the user documentation (`docs/en/explanation/literature.md`), not restated here.
