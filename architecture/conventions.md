---
id: arch-conventions
title: Conventions
type: arc42
audience:
  - process-engineer
  - auditor
  - ai
status: outline
relates:
  - arch-home
---

# Conventions

Rules for writing and reading this architecture site. Not a product tutorial.

## Docs-as-code

- Source of truth is Markdown in `architecture/` in this Git repository.
- Humans read it via Zensical (`zensical serve -f zensical.architecture.toml`).
- Agents parse frontmatter `id` / `relates` and Mermaid node IDs. Cite those IDs in generated answers (TBD whether that is mandatory — [arc42-01](01-introduction-and-goals.md)).

## Frontmatter

Required keys:

- `id` — stable slug (`arc42-01`, `c4-context`, `adr-0001`, `bb-amanzi-api`)
- `type` — `arc42` | `c4` | `adr` | `building-block`
- `audience` — subset of `process-engineer`, `auditor`, `ai`
- `status` — `outline` now; later `draft` or `accepted`
- `relates` — list of other `id` values

## Diagrams

- Mermaid fenced blocks only (rendered as SVG in the page).
- Node IDs: camelCase or PascalCase, **no spaces**.
- Do not commit duplicate `.svg` exports of the same diagram.
- C4 views use nested `flowchart` subgraphs, not a second diagram language.

## Claims

- When a chapter leaves `outline`, every factual claim must cite a **repository path** (file or directory).
- Do not invent quality numbers, owners, or audit criteria. Put them under **TBD** until Vitens supplies them.
- Do not rewrite user-facing science (Freundlich, Onda, units). Link to user documentation Explanation / Reference instead.
- No click-by-click UI steps.

## Content to write

- Short examples of a good vs bad cross-reference (ID vs “the API”).
- How to add an ADR from [0000-template](decisions/0000-template.md).
