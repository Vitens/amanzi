---
id: arc42-01
title: Introduction and goals
type: arc42
audience:
  - process-engineer
  - auditor
  - ai
status: draft
relates:
  - arc42-10
  - arc42-11
  - c4-context
---

# 1. Introduction and goals

Amanzi is a **design and scenario tool** for drinking-water treatment plants (`README.md`). Users draw a flowsheet in the SPA (`ui/`), persist it as JSON (`ui/src/stores/project.js`), and the engine calculates quantity, quality, energy, chemicals, and sustainability (`amanzi/core/scenario.py`). It is **not** a live plant controller.

## Purpose

The product lets a designer compare treatment scenarios: a graph of process units, a water composition, and the numbers that follow from that graph. The calculation entry point used by every backend is `AmanziAPI` (`amanzi/server/api.py`). See [bb-amanzi-api](building-blocks/amanzi-api.md).

## Non-goals

These are absent from the product as built:

- **No time-series control or SCADA.** The engine runs a scenario document once per `solve`, `design`, or `report` (`amanzi/server/api.py`). It does not subscribe to plant tags.
- **No GIS plant layout.** The canvas stores block positions in project metadata (`ui/src/stores/project.js`, field `metadata.canvas`). That is a diagram, not a map.
- **No user accounts in the SPA.** The project is kept in `localStorage` and in downloaded JSON (`ui/src/stores/project.js`). There is no login module under `ui/src/`.

## Stakeholders

- **Process engineers with software knowledge** read building blocks and runtime to find where a unit is calculated.
- **Auditors** read constraints, ADRs, quality scenarios, and risks. Evidence is a repository path, not a slide.
- **AI agents** read this Markdown. Cite `id` values ([arch-conventions](conventions.md)).

Authors recorded in the package metadata are Abel Heinsbroek, Nils Zickermann, and Christiaan Slippens (`pyproject.toml`, `README.md`). The public repository is `https://github.com/Vitens/amanzi` (`pyproject.toml`).

## Overlap with user documentation

Science, units, and how to operate the canvas stay in the user site (`docs/en/explanation/`, `docs/en/reference/`, with `docs/nl/`, `docs/de/`, and `docs/fr/` in parallel). This site explains structure and decisions. Parameter tables are not generated here ([adr-0004](decisions/0004-yaml-parametric-models.md)).

## Quality goals

Names only. Numeric targets are **TBD** in [arc42-10](10-quality-requirements.md).

- **Calculation integrity** — a known project JSON produces a defined result.
- **Explainability** — a reported number can be traced to a solver, a parametric equation, or a key figure.
- **Reproducibility** — the same JSON and the same Amanzi build produce the same report.
- **Operable browser deployment** — a user can run the released UI without installing Python ([adr-0002](decisions/0002-dual-execution-backends.md)).

## Open questions (TBD — do not invent)

- Who may accept ADRs? Who operates `https://demo.amanzi.app`? The URL is named in `README.md` and `docs/en/index.md`. The operator is not named in this repository.
- What must an auditor verify (reproducibility, literature traceability, GPL compliance, security, or all)?
- Quality numbers: Pyodide load budget, solve time, numerical tolerances, model validation or peer review.
- Data classification of project JSON; which PostHog events are in scope; whether the hosted demo stores scenarios.
- Which backend `demo.amanzi.app` runs today (Pyodide zip vs Lambda). The GitHub release UI is built with `VITE_BACKEND=pyodide` (`.github/workflows/deploy-ui.yml`). That does not by itself identify the demo host.
- Threat model with no login; supply-chain review of the wheels in the UI zip.
- May AI agents treat this site as the **only** architecture source of truth, or must they also read the code when a draft and a path disagree?
