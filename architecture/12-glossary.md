---
id: arc42-12
title: Glossary
type: arc42
audience:
  - process-engineer
  - auditor
  - ai
status: outline
relates:
  - arch-home
---

# 12. Glossary

Architecture terms only. Water-treatment terms (EBCT, SI, PFAS Sum4, …) live in the **user documentation** file `docs/reference/glossary.md` in this repository (Reference › Glossary on the user site). Do not duplicate them here.

## Content to write

- **Container** — C4 deployable/runnable piece (SPA, worker, Flask, Lambda).
- **Component** — C4 building block inside a container (`AmanziAPI`, solvers).
- **Scenario** — one flowsheet + parameters inside a project JSON (architecture sense: data), not an arc42 quality scenario (those are labelled “quality scenario” in chapter 10).
- **Project JSON** — system of record for a user’s plant designs ([ADR-0001](decisions/0001-json-project-as-system-of-record.md)).
- **Solver** — one of the six sequential calculation stages ([ADR-0003](decisions/0003-sequential-solvers.md)).
- **Parametric model** — YAML-defined inputs/outputs bound to a Python `Model` ([ADR-0004](decisions/0004-yaml-parametric-models.md)).
- **AmanziAPI** — single façade used by all backends (`bb-amanzi-api`).
- **Extraneous composition** — PFAS/VOC/Other/TOC/colour carried beside PHREEQC `Solution`.
- **ADR** — Architecture Decision Record (`adr-NNNN`).
- **`id`** — stable frontmatter identifier for humans and agents.
