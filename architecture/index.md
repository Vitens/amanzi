---
id: arch-home
title: Amanzi architecture
type: arc42
audience:
  - process-engineer
  - auditor
  - ai
status: outline
relates:
  - arch-conventions
  - arc42-01
---

# Amanzi architecture

This site is the **architecture** documentation for Amanzi (Vitens). It follows [arc42](https://arc42.org/). It is **not** the product user guide.

## Who this is for

- **Process engineers with software knowledge** — how the calculation engine, flowsheet, and deployments are structured; where a process unit lives in code.
- **Auditors** — constraints, decisions, quality requirements, risks, and traceability from a claim to a repository path (when chapters leave `outline`).
- **AI agents** — the same Markdown is the source of truth. Prefer stable `id` values in frontmatter and Mermaid node IDs when citing.

Product usage (how to click the canvas, what PFAS units mean) lives in the **user documentation** (`docs/` in this repository, Diátaxis). Do not copy tutorials here.

## How to read this site

- **arc42 chapters 1–12** — goals, constraints, context, strategy, building blocks, runtime, deployment, concepts, decisions index, quality, risks, glossary.
- **C4** — context, containers, components (Mermaid, stable node IDs).
- **Building blocks** — one page per named block, linked from chapter 5.
- **Decisions** — ADRs. Chapter 9 is only an index.

## Machine conventions

Every page has YAML frontmatter: `id`, `type` (`arc42` | `c4` | `adr` | `building-block`), `audience`, `status`, `relates`. See [Conventions](conventions.md).

## Content to write

- One-paragraph system identity (scenario tool, JSON project, six solvers) without repeating the user landing page.
- Audience doors as above.
- Pointer that all pages in this pass are `status: outline`.
