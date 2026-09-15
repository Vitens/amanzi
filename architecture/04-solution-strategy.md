---
id: arc42-04
title: Solution strategy
type: arc42
audience:
  - process-engineer
  - auditor
  - ai
status: outline
relates:
  - adr-0001
  - adr-0002
  - adr-0003
  - adr-0004
---

# 4. Solution strategy

The few decisions that shape the rest of the architecture. Detail belongs in ADRs.

## Content to write

- **GUI-first:** Vue 3 SPA is the only supported user path.
- **JSON as system of record:** [ADR-0001](decisions/0001-json-project-as-system-of-record.md).
- **Dual execution:** same `AmanziAPI` in Pyodide worker, Flask, or Lambda — [ADR-0002](decisions/0002-dual-execution-backends.md).
- **Sequential solvers:** quantity → quality → hydraulics → energy → chemicals → sustainability — [ADR-0003](decisions/0003-sequential-solvers.md).
- **YAML parametrics:** UI schemas and design equations from `amanzi/parametric/*.yml` — [ADR-0004](decisions/0004-yaml-parametric-models.md).
- Quality chemistry delegated to PHREEQC; micropollutants (PFAS/VOC) carried as extraneous data, not the PHREEQC database.
- Link building blocks rather than repeating interfaces here.
