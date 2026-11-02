---
id: arch-conventions
title: Conventions
type: arc42
audience:
  - process-engineer
  - auditor
  - ai
status: draft
relates:
  - arch-home
  - arc42-09
---

# Conventions

Rules for writing and reading this architecture site. Not a product tutorial.

## Docs-as-code

- Source of truth for this site is Markdown in `architecture/` in this Git repository.
- Humans read it via Zensical: `zensical serve -f zensical.architecture.toml` (port 8001, `zensical.architecture.toml`).
- CI builds the HTML with the same file (`.github/workflows/build-docs.yml`) and uploads `architecture-html.zip`. Publishing to a public URL is not wired in that workflow.
- Agents parse frontmatter `id` / `relates` and Mermaid node IDs. Cite those IDs in generated answers. Whether this site is the **only** architecture source an agent may use is **TBD** ([arc42-01](01-introduction-and-goals.md)). When a draft and the code disagree, the cited path is the evidence to re-check; a draft is not an accepted decision.

## Frontmatter

Required keys:

- `id` — stable slug (`arc42-01`, `c4-context`, `adr-0001`, `bb-amanzi-api`)
- `type` — `arc42` | `c4` | `adr` | `building-block`
- `audience` — subset of `process-engineer`, `auditor`, `ai`
- `status` — `outline` | `draft` | `accepted`. This pass uses `draft`. `accepted` needs an owner ([arc42-09](09-architecture-decisions.md)).
- `relates` — list of other `id` values

## Cross-references

Cite a stable `id`, then the file. A bare nickname is not a citation.

- Good: the façade is [bb-amanzi-api](building-blocks/amanzi-api.md) (`amanzi/server/api.py`).
- Weak: “the API does solve.” That name is not an `id`, and it does not name a path.

Mermaid node IDs are cited the same way: `AmanziAPI` in [c4-components](c4/components.md), not “the box in the middle.”

## Diagrams

- Mermaid fenced blocks only (rendered in the page).
- Node IDs: camelCase or PascalCase, **no spaces**.
- Do not commit duplicate `.svg` exports of the same diagram.
- C4 views use nested `flowchart` subgraphs, not a second diagram language.

## Claims

- Every factual claim in a `draft` or `accepted` page cites a **repository path** (file or directory).
- Do not invent quality numbers, owners, or audit criteria. Put them under **TBD** until Vitens supplies them.
- Do not rewrite user-facing science (Freundlich, Onda, units). Link to user documentation under `docs/en/explanation/` and `docs/en/reference/` instead. Dutch, German, and French copies use the same paths under `docs/nl/`, `docs/de/`, and `docs/fr/`.
- No click-by-click UI steps.

## How to add an ADR

1. Copy [adr-0000](decisions/0000-template.md) to `architecture/decisions/NNNN-short-kebab-title.md`.
2. Set `id: adr-NNNN` and `status: draft`. One decision per file.
3. Add a row to [adr-index](decisions/index.md) and a link in [arc42-09](09-architecture-decisions.md).
4. Add the page to the `Decisions` list in `zensical.architecture.toml`. The template itself stays out of that nav.
5. Link the new `id` from the chapter the decision shapes (usually [arc42-04](04-solution-strategy.md)).
