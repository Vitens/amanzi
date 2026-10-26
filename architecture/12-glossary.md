---
id: arc42-12
title: Glossary
type: arc42
audience:
  - process-engineer
  - auditor
  - ai
status: draft
relates:
  - arch-home
---

# 12. Glossary

Architecture terms only. Water-treatment terms (EBCT, SI, PFAS Sum4, and the rest) live in `docs/en/reference/glossary.md` (Reference › Glossary on the user site; same path under `docs/nl/`, `docs/de/`, and `docs/fr/`). Do not duplicate them here.

- **Container** — a C4 deployable or runnable piece: the SPA, the Pyodide worker, Flask, or Lambda ([c4-containers](c4/containers.md)).
- **Component** — a C4 building block inside a container, such as `AmanziAPI` or the solvers ([c4-components](c4/components.md)).
- **Scenario** — one flowsheet plus parameters inside a project JSON (`scenarios[]` in `ui/src/stores/project.js` and `amanzi/core/scenario.py`). This is data. An arc42 quality scenario is labelled “quality scenario” in [arc42-10](10-quality-requirements.md).
- **Project JSON** — the system of record for a user’s plant designs ([adr-0001](decisions/0001-json-project-as-system-of-record.md)).
- **Solver** — one of the six sequential calculation stages ([adr-0003](decisions/0003-sequential-solvers.md), `amanzi/components/solvers/`).
- **Parametric model** — YAML-defined inputs and outputs bound to a Python `Model` ([adr-0004](decisions/0004-yaml-parametric-models.md), `amanzi/models/parametric/parametric.py`).
- **AmanziAPI** — the single façade used by all backends (`amanzi/server/api.py`, [bb-amanzi-api](building-blocks/amanzi-api.md)).
- **Extraneous composition** — `Color`, `TOC`, `PFAS`, `VOC`, and `Other` carried beside the PHREEQC solution. Groundwater attaches that dict in `PhreeqPython.add_solution` (`amanzi/models/groundwater.py`).
- **ADR** — Architecture Decision Record, file `architecture/decisions/NNNN-….md`, id `adr-NNNN`.
- **`id`** — stable frontmatter identifier for humans and agents ([arch-conventions](conventions.md)).
