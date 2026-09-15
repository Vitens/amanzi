---
id: bb-flask-server
title: Flask server
type: building-block
audience:
  - process-engineer
  - ai
status: outline
relates:
  - adr-0002
  - bb-amanzi-api
  - arc42-07
---

# Flask server

Development and self-hosted HTTP front for `AmanziAPI`.

## Content to write

- **Path:** `amanzi/server/app.py`; entry `amanzi-server`.
- **In:** HTTP `/api/parameters`, `/api/keyfigures`, `/api/solve/<scenario>`, `/api/design/<scenario>/<model>`, `/api/report`.
- **Out:** JSON; also serves `ui/dist` static SPA.
- Default port 7331; `--debug`, `--no-browser`.
- **Owner:** TBD.
