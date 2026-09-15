---
id: arc42-01
title: Introduction and goals
type: arc42
audience:
  - process-engineer
  - auditor
  - ai
status: outline
relates:
  - arc42-10
  - arc42-11
  - c4-context
---

# 1. Introduction and goals

Amanzi is a **design and scenario tool** for drinking-water treatment plants. Users draw a flowsheet, persist it as JSON, and the engine calculates quantity, quality, energy, chemicals, and sustainability. It is **not** a live plant controller (not SCADA).

## Content to write

- System purpose and non-goals (no time-series control, no GIS plant layout, no user accounts).
- Stakeholders: process engineers with software knowledge; auditors; AI agents consuming this site.
- Overlap with user documentation: science and units stay there; this site explains structure and decisions.
- Quality goals (names only until numbers exist): calculation integrity, explainability, reproducibility of a project file, operable browser deployment.

## Open questions (TBD — do not invent)

- Who may accept ADRs? Who operates `https://demo.amanzi.app`?
- What must an auditor verify (reproducibility, literature traceability, GPL/compliance, security, or all)?
- Quality numbers: Pyodide load budget, solve-time, numerical tolerances, model validation / peer review.
- Data classification of project JSON; PostHog events; whether the hosted demo stores scenarios.
- Production backend today (Pyodide vs Lambda); RTO/RPO if any.
- Threat model with no login; supply chain for wheels in the Pyodide zip.
- May AI agents treat this site as the **only** architecture source of truth? Must they cite `id` values?
