---
id: arch-home
title: Amanzi architecture
type: arc42
audience:
  - process-engineer
  - auditor
  - ai
status: draft
relates:
  - arch-conventions
  - arc42-01
---

# Amanzi architecture

This site is the **architecture** documentation for Amanzi (Vitens). It follows [arc42](https://arc42.org/). It is **not** the product user guide.

Amanzi is a design and scenario tool for drinking-water treatment plants (`README.md`, `pyproject.toml`). A user draws a flowsheet in the Vue SPA (`ui/`). The project is a JSON document (`ui/src/stores/project.js`). The engine runs six solvers in order — quantity, quality, hydraulics, energy, chemicals, sustainability (`amanzi/core/scenario.py`). It is not a live plant controller.

## Who this is for

- **Process engineers with software knowledge** — how the calculation engine, flowsheet, and deployments are structured, and where a process unit lives in code.
- **Auditors** — constraints, decisions, quality requirements, risks, and a path from a claim to a repository file.
- **AI agents** — the same Markdown is the source of truth for this site. Cite frontmatter `id` values and Mermaid node IDs. See [arch-conventions](conventions.md).

Product usage (how to use the canvas, what a PFAS sum means) lives in the user documentation (`docs/en/`, `docs/nl/`, `docs/de/`, `docs/fr/`, Diátaxis). Do not copy tutorials here. Water-treatment science stays in `docs/en/explanation/`.

## How to read this site

- **arc42 chapters 1–12** — goals, constraints, context, strategy, building blocks, runtime, deployment, concepts, decisions index, quality, risks, glossary.
- **C4** — context, containers, components (Mermaid, stable node IDs).
- **Building blocks** — one page per named block, linked from [arc42-05](05-building-block-view.md).
- **Decisions** — ADRs. [arc42-09](09-architecture-decisions.md) is only an index.

Pages on this site are `status: draft`. An owner has not accepted them. Who may move a page to `accepted` is **TBD** ([arc42-01](01-introduction-and-goals.md)).

## Machine conventions

Every page has YAML frontmatter: `id`, `type` (`arc42` | `c4` | `adr` | `building-block`), `audience`, `status`, `relates`. See [arch-conventions](conventions.md).
