---
id: arc42-11
title: Risks and technical debt
type: arc42
audience:
  - auditor
  - process-engineer
  - ai
status: draft
relates:
  - arc42-10
  - bb-process-models
---

# 11. Risks and technical debt

Known gaps. A row here is not a completed control. Mitigations that do not exist in the repository are not listed.

## No automated test suite

There is no `tests/` tree and no `test_*.py` module in this repository. Solver results and the JSON schema have no regression net. Quality targets in [arc42-10](10-quality-requirements.md) cannot be checked by CI today. `.github/workflows/build-docs.yml` builds documentation only.

## GAC PFAS on the plant walk

`Activatedcarbon.design` calls `breakthrough_calculation` and `advancedExtraneousRemoval` (`amanzi/models/activatedcarbon.py`). `Activatedcarbon.run_quality` for `product` optionally runs spray aeration and then returns that solution. The calls to `advancedExtraneousRemoval` and `simpleExtraneousRemoval` inside `run_quality` are comments. A plant-wide `solve` therefore does not apply the PFAS breakthrough that the design view calculates.

## Ion exchange is hidden

`amanzi/models/ionexchange.py` exists. `amanzi/models/__init__.py` comments out `from .ionexchange import Ionexchange`, so `Scenario.load_models` cannot resolve the class (`amanzi/core/scenario.py` uses `getattr` on `amanzi.models`). The canvas block sets `hidden: true` (`ui/src/models/ionexchange/block.vue`). Vue files for the unit remain under `ui/src/models/ionexchange/`.

## Thin error UX

`solveDebounced` catches backend errors and sets `invalid` without `invalid_message` (`ui/src/stores/project.js`). The banner in `ui/src/App.vue` translates that message. A quality non-convergence (`amanzi/components/solvers/qualitysolver.py`) or a missing key figure (`amanzi/core/database.py`) can look like a generic invalid scenario.

## Scientific validation process

`amanzi/database/pfas_isotherms.csv` and `amanzi/database/pfas_isotherms_README.md` record isotherm data. Who may accept a new model or a new isotherm is **TBD**. No checklist file exists in the repository.

## Spray-aerator Sauter diameter

`Sprayaerator.__init__` leaves `self.sauter = float(self.parameters['sauter_diameter'])` commented out (`amanzi/models/sprayaerator.py`). `run_quality` still passes `self.sauter` into `calculate_efficiency`. The default `d_sauter=0.00025` on that function applies only when the argument is omitted, so this path depends on an attribute `__init__` does not set.

Other units do not use that attribute for spray aeration. `spray_aeration` on sand filtration, marble filtration, and activated carbon reads `co2_removal_efficiency` and `ch4_removal_efficiency` (`amanzi/models/sandfiltration.py`, `amanzi/models/marblefiltration.py`, `amanzi/models/activatedcarbon.py`). `changelog.md` for 1.0.5 says the spray aeration model was changed to a user-defined efficiency. That matches those helpers. It does not match `Sprayaerator.run_quality`, which still calls `calculate_efficiency`. `marblefiltration.py` also keeps the commented `self.sauter` line, and its live spray path uses the efficiency parameters instead.

## Documentation split

User behaviour is Diátaxis under `docs/`. Architecture is arc42 under `architecture/`. A generated MyST `_build` directory, if present on a machine, is not a source. Sources are the Markdown trees and `zensical.toml`, `zensical.nl.toml`, `zensical.de.toml`, `zensical.fr.toml`, and `zensical.architecture.toml`.

## Supply chain

The UI zip contains an Amanzi wheel built in CI and a PhreeqPython wheel downloaded from `https://github.com/Vitens/phreeqpython/releases/download/v1.6.2/` (`.github/workflows/deploy-ui.yml`). The worker also loads the Pyodide runtime from `https://cdn.jsdelivr.net` (`ui/src/backend/python.worker.js`). A recorded review of those artifacts is **TBD**.

## Analytics and privacy

Production bundles initialise PostHog (`ui/src/main.js`, `ui/src/plugins/posthog.js`). Classification of events and of `/userinfo` is **TBD**.

## No login

Projects live in browser `localStorage` or in a file the user downloads (`ui/src/stores/project.js`). Confidentiality of a scenario is a process around that file. The application does not authenticate the designer.
