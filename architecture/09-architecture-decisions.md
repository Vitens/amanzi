---
id: arc42-09
title: Architecture decisions
type: arc42
audience:
  - process-engineer
  - auditor
  - ai
status: draft
relates:
  - adr-0001
  - adr-0002
  - adr-0003
  - adr-0004
---

# 9. Architecture decisions

This chapter is an **index only**. Decision prose lives in ADR files.

## ADRs

- [adr-index](decisions/index.md)
- [adr-0001](decisions/0001-json-project-as-system-of-record.md) — JSON project as system of record
- [adr-0002](decisions/0002-dual-execution-backends.md) — dual execution backends
- [adr-0003](decisions/0003-sequential-solvers.md) — sequential solvers
- [adr-0004](decisions/0004-yaml-parametric-models.md) — YAML parametric models

Template for new records: `architecture/decisions/0000-template.md` (not in the site nav). Steps: [arch-conventions](conventions.md).

## Status legend

| Status | Meaning |
| --- | --- |
| `outline` | Headings and a list of claims still to write. |
| `draft` | Claims are written and cite a repository path. Not yet accepted. |
| `accepted` | An owner has accepted the record. |
| `deprecated` | No longer followed. Say what replaced it. |
| `superseded` | Replaced by another ADR. Link that ADR’s `id`. |

Every ADR on this site is `draft`. Who may change status to `accepted` is **TBD** ([arc42-01](01-introduction-and-goals.md)).
