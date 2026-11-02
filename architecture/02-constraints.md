---
id: arc42-02
title: Constraints
type: arc42
audience:
  - process-engineer
  - auditor
  - ai
status: draft
relates:
  - adr-0002
  - arc42-07
---

# 2. Constraints

Technical, organisational, and political constraints that architecture must obey.

## License

The repository is licensed under the GNU General Public License v3.0 (`LICENSE`, `pyproject.toml` `license.file`). GPL-3.0 is a copyleft license: distributing a modified Amanzi, or a combined work that includes the program, must follow that license. Whether a particular closed system counts as a combined work is a legal question. This site does not decide it. **TBD** if Vitens publishes an additional combining policy.

## Execution

Three hosts call the same `AmanziAPI` ([adr-0002](decisions/0002-dual-execution-backends.md)):

- **Browser.** `ui/src/main.js` selects the Pyodide worker unless `VITE_BACKEND` is `server`. The release build sets `VITE_BACKEND=pyodide` (`.github/workflows/deploy-ui.yml`).
- **Development server.** `amanzi-server` is the console script for Flask (`pyproject.toml`, `amanzi/server/app.py`).
- **Optional hosted API.** AWS Lambda (`lambda/lambda_function.py`) maps API Gateway paths onto the same methods.

## Chemistry engine

Quality uses PHREEQC through PhreeqPython. `Scenario` constructs `phreeqpython.PhreeqPython()` (`amanzi/core/scenario.py`). The dependency is pinned: `phreeqpython==1.6.2` (`pyproject.toml`). The UI zip downloads that wheel (`.github/workflows/deploy-ui.yml`). Quality chemistry is not optional for a scenario solve: `QualitySolver` calls `model.run_quality` (`amanzi/components/solvers/qualitysolver.py`).

## Identity and persistence

The SPA has no account model. `projectStore.save` writes the serialized project to `localStorage` under the key `project` (`ui/src/stores/project.js`). Opening a project reads that key, or a bundled default JSON (`ui/src/App.vue`).

The production UI installs PostHog only when Vite `MODE` is not `development` (`ui/src/main.js`). The plugin calls `https://eu.i.posthog.com` and, if `/userinfo` returns JSON, identifies that email (`ui/src/plugins/posthog.js`). Data classification of those events is **TBD** ([arc42-08](08-crosscutting-concepts.md)).

## Documentation and UI languages

- User documentation is four parallel trees: `docs/en/`, `docs/nl/`, `docs/de/`, and `docs/fr/` (`zensical.toml`, `zensical.nl.toml`, `zensical.de.toml`, `zensical.fr.toml`).
- This architecture site is English only (`zensical.architecture.toml`).
- The SPA locales are `en`, `nl`, `de`, and `fr` (`ui/src/main.js`, `ui/src/locales/`).

## GUI-first

The only documented end-user path is the Vue SPA (`ui/`, `README.md`). `pyproject.toml` exposes one script, `amanzi-server`. There is no scenario CLI. `Project` in `amanzi/core/project.py` is the object the backends construct. It is not documented as an end-user API.

## Organisation

Authors are Vitens staff listed in `pyproject.toml` and `README.md`. The public Git remote is `https://github.com/Vitens/amanzi`.

## TBD

Internal hosting, network, and data-residency constraints for `demo.amanzi.app` are not stated in this repository. The URL is named in `README.md`. The operator, TLS, and residency rules are **TBD** ([arc42-07](07-deployment-view.md)).
