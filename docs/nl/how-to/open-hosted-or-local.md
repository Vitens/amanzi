---
lang: nl
title: Open gehost of lokaal
type: how-to
audience: everyone
status: outline
---

# Open gehost of lokaal

Start Amanzi in de browser vanaf de gehoste demo, of vanaf een gedownloade release.

## Inhoud om te schrijven

- **Gehost:** open [https://demo.amanzi.app](https://demo.amanzi.app).
- **Lokale release:** download de nieuwste zip van [GitHub Releases](https://github.com/Vitens/amanzi/releases), pak uit, serveer de map met een static server, bijv. `python -m http.server 8000`, en ga naar `http://localhost:8000`.
- Wacht tot de engine is geladen (voortgangsdialoog). Pyodide betekent dat je voor dit pad geen Python hoeft te installeren.
- Wanneer de demo genoeg is vs wanneer een lokale zip nodig is (offline, een vaste versie).
- Buiten scope: developer Vite/Flask-setup — dat blijft in de repository-README.
