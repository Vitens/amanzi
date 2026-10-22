---
lang: de
title: Gehostet oder lokal öffnen
type: how-to
audience: everyone
status: outline
---

# Gehostet oder lokal öffnen

Führen Sie Amanzi im Browser aus der gehosteten Demo oder aus einem heruntergeladenen Release aus.

## Inhalt zum Schreiben

- **Gehostet:** öffnen Sie [https://demo.amanzi.app](https://demo.amanzi.app).
- **Lokales Release:** laden Sie die neueste Zip-Datei von [GitHub Releases](https://github.com/Vitens/amanzi/releases) herunter, entpacken Sie sie, stellen Sie den Ordner mit einem statischen Server bereit, z. B. `python -m http.server 8000`, und öffnen Sie dann `http://localhost:8000`.
- Warten Sie, bis die Engine geladen ist (Fortschrittsdialog). Pyodide bedeutet, dass für diesen Weg keine Python-Installation nötig ist.
- Wann die Demo ausreicht und wann eine lokale Zip-Datei nötig ist (offline, eine festgelegte Version).
- Außerhalb des Umfangs: Entwickler-Setup mit Vite/Flask — das bleibt in der README des Repositories.
