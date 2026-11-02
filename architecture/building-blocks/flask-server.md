---
id: bb-flask-server
title: Flask server
type: building-block
audience:
  - process-engineer
  - ai
status: draft
relates:
  - adr-0002
  - bb-amanzi-api
  - arc42-07
---

# Flask server

Development and self-hosted HTTP front for `AmanziAPI`. Decision: [adr-0002](../decisions/0002-dual-execution-backends.md).

## Repository

`amanzi/server/app.py`. Console script `amanzi-server` → `amanzi.server.app:main` (`pyproject.toml`).

## Interface

One process-wide `AmanziAPI` (`amanzi/server/app.py`).

| Route | Method | API call |
| --- | --- | --- |
| `/api/parameters` | GET | `parameters()` |
| `/api/keyfigures` | GET | `keyfigures()` |
| `/api/solve/<scenario>` | POST | `solve(request.json, scenario)` |
| `/api/design/<scenario>/<model>` | POST | `design(request.json, scenario, model)` |
| `/api/report` | POST | `report(request.json)` |

Other paths serve `ui/dist` (`send_from_directory`), falling back to `index.html`. CORS is enabled (`flask_cors.CORS`).

The SPA talks to this process when `VITE_BACKEND=server`, using `VITE_SERVER_URL` (`ui/src/backend/server.js`). Development sets that URL to `http://localhost:7331/api` (`ui/.env.development`).

## Process flags

`main` is a Click command (`amanzi/server/app.py`):

- `--port` — default 7331
- `--debug` — Flask debug, default off
- `--no-browser` — do not open a browser; the default opens `http://localhost:<port>`

`README.md` shows `amanzi-server --no-browser` for local use.

## Owner

**TBD.**
