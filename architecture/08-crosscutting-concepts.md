---
id: arc42-08
title: Cross-cutting concepts
type: arc42
audience:
  - process-engineer
  - auditor
  - ai
status: draft
relates:
  - adr-0004
  - bb-parametric-yaml
  - bb-vue-spa
---

# 8. Cross-cutting concepts

Ideas that show up in many building blocks.

## Internationalisation

The SPA uses vue-i18n with message catalogs `en`, `nl`, `de`, and `fr` (`ui/src/main.js`, `ui/src/locales/`). The locale starts from `navigator.language`, falling back to `en`. User documentation is four Markdown trees (`docs/en/`, `docs/nl/`, `docs/de/`, `docs/fr/`). This architecture site stays English (`zensical.architecture.toml`).

## Parametric YAML and the equation engine

Models declare YAML layers. `ParametricModel` loads each `amanzi/parametric/<name>.yml` (`amanzi/models/parametric/parametric.py`). Output equations are evaluated with Python `ast` against a small set of builtins and `math` (`amanzi/models/parametric/output.py`). An output may carry `uom`, `if` (hidden when the expression is false; see `Output.hidden`), and `validation` (`Output.validate`). Example conditions live in `amanzi/parametric/base.yml`. Decision: [adr-0004](decisions/0004-yaml-parametric-models.md). Block: [bb-parametric-yaml](building-blocks/parametric-yaml.md).

## Key figures

`Database` reads `amanzi/database/key_figures.csv` (semicolon-separated) (`amanzi/core/database.py`). `Scenario` applies project-level overwrites, then stores scenario-level overwrites on the same object (`amanzi/core/scenario.py`). `AmanziAPI.keyfigures` returns the CSV rows (`amanzi/server/api.py`). The SPA loads them through `projectStore.getKeyFigures` (`ui/src/stores/project.js`).

## Project migration

The on-disk version is `metadata.amanzi_version`, written by `projectStore.serialize` (`ui/src/stores/project.js`). `migrateProject` applies `MIGRATION_LOG` forward only (`ui/src/lib/migrationConfig.js`, `ui/src/lib/projectMigration.js`). A successful migration raises a toast (`ui/src/lib/migrationToast.js`, called from `ui/src/App.vue`).

## Analytics

PostHog is installed only when the Vite mode is not `development` (`ui/src/main.js`). The plugin initialises `posthog-js` against `https://eu.i.posthog.com` and attempts `fetch('/userinfo')` to call `identify` (`ui/src/plugins/posthog.js`). Which events are sent, and the data class of project contents versus UI events, is **TBD**.

## Error surface

Python exceptions from the worker or from axios become a rejected promise. `solveDebounced` sets `interfaceStore.invalid` without storing `error.message` (`ui/src/stores/project.js`). The banner in `ui/src/App.vue` renders the translation of `invalid_message`. Validation failures do set that message (for example `ui.general.messages.missing_source`). Calculation failures do not. See [arc42-11](11-risks-and-technical-debt.md).

## Stream types

Connections are one of `product`, `waste`, or `flush`. Quality walks them in that order (`amanzi/components/solvers/qualitysolver.py`). Block specs declare anchors with a `type` and whether the anchor is `optional` (`ui/src/models/*/block.vue`). Wiring rules for people are in `docs/en/reference/streams.md` (and the same path under `docs/nl/`, `docs/de/`, and `docs/fr/`). This site does not repeat that how-to.

## Design versus the plant walk

`AmanziAPI.design` stops the scenario at the edited model and then calls `run_design` (`amanzi/server/api.py`, `amanzi/models/model.py`). `run_quality` on the plant walk can do less physics than `design`. Activated carbon is the documented case: `design` runs breakthrough; `run_quality` for product water returns the influent after optional spray aeration and does not call breakthrough (`amanzi/models/activatedcarbon.py`). See [arc42-11](11-risks-and-technical-debt.md).
