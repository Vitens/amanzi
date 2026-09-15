---
id: arc42-02
title: Constraints
type: arc42
audience:
  - process-engineer
  - auditor
  - ai
status: outline
relates:
  - adr-0002
  - arc42-07
---

# 2. Constraints

Technical, organisational, and political constraints that architecture must obey.

## Content to write

- **License:** GNU GPL-3.0 (`LICENSE`); implications for combining with closed systems.
- **Execution:** production UI can run entirely in the browser via Pyodide; development uses Flask (`amanzi-server`); hosted API may use AWS Lambda. Cite `ui/src/main.js`, `amanzi/server/app.py`, `lambda/`.
- **Chemistry engine:** PHREEQC via PhreeqPython — not optional for quality.
- **Identity:** no user accounts; persistence is browser storage plus downloaded JSON.
- **Documentation language:** architecture and user docs English; UI en/nl/de.
- **GUI-first:** no user-facing scenario CLI; Python `Project` is not a documented end-user API.
- **Organisational:** Vitens N.V. authors; public GitHub `Vitens/amanzi`.
- TBD: internal hosting, network, and data-residency constraints for `demo.amanzi.app`.
