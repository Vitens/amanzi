---
id: arc42-11
title: Risks and technical debt
type: arc42
audience:
  - auditor
  - process-engineer
  - ai
status: outline
relates:
  - arc42-10
  - bb-process-models
---

# 11. Risks and technical debt

Known gaps. Do not present a stub as a completed control.

## Content to write

- **No automated test suite** — no regression net for solvers or JSON schema.
- **GAC PFAS:** breakthrough runs in `design()`; plant-wide `run_quality()` does not currently apply PFAS removal (cite `amanzi/models/activatedcarbon.py`).
- **Ion exchange** exists in code but is not exported / hidden in the library.
- **Thin error UX** — engine failures can look like generic invalid.
- **Scientific validation process unknown** (TBD).
- **Spray aerator** Sauter diameter may be unset at runtime (verify when filling).
- **Documentation split:** user Diátaxis vs this arc42 site; leftover MyST `_build` must not be treated as source.
- **Supply chain:** Pyodide + PhreeqPython wheels in the UI zip (TBD review).
- **Analytics / privacy:** PostHog (TBD).
- **No login** — project files in browser storage or email; confidentiality is a process control, not an app control.

## Content not to write

- Mitigations that do not exist yet.
