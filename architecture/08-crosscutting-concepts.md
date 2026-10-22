---
id: arc42-08
title: Cross-cutting concepts
type: arc42
audience:
  - process-engineer
  - auditor
  - ai
status: outline
relates:
  - adr-0004
  - bb-parametric-yaml
  - bb-vue-spa
---

# 8. Cross-cutting concepts

Ideas that show up in many building blocks.

## Content to write

- **i18n:** Vue-i18n locales `en`, `nl`, `de`; docs remain English.
- **Parametric YAML + equation engine:** input schemas, `if` visibility, AST-evaluated outputs (`amanzi/models/parametric/`).
- **Key figures:** CSV database plus project/scenario overwrites.
- **Project migration:** version field in JSON; toast when upgraded.
- **Analytics:** PostHog in production UI — TBD data classification.
- **Error surface:** Python exceptions often become a generic invalid state in the UI.
- **Stream types:** product, waste, flush — wiring rules (point to user Reference, do not tutorial).
- **Design vs plant walk:** `design()` may run richer physics than `run_quality()` (GAC PFAS gap — [arc42-11](11-risks-and-technical-debt.md)).
