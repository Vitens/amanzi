---
title: Open hosted or local
type: how-to
audience: everyone
status: outline
---

# Open hosted or local

Run Amanzi in the browser from the hosted demo, or from a downloaded release.

## Content to write

- **Hosted:** open [https://demo.amanzi.app](https://demo.amanzi.app).
- **Local release:** download the latest zip from [GitHub Releases](https://github.com/Vitens/amanzi/releases), unpack, serve the folder with a static server, e.g. `python -m http.server 8000`, then browse to `http://localhost:8000`.
- Wait until the engine has loaded (progress dialog). Pyodide means no Python install for this path.
- When the demo is enough vs when a local zip is needed (offline, a pinned version).
- Out of scope: developer Vite/Flask setup — that stays in the repository README.
