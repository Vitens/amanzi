---
lang: de
title: Einschränkungen
type: reference
audience: everyone
status: outline
---

# Einschränkungen

Fakten darüber, was das aktuelle Produkt nicht tut. Keine Workarounds außer dem Verweis auf die UI, die *existiert*.

## Inhalt zum Schreiben

- **Ionenaustausch** ist nicht in der Prozessbibliothek und wird im Berechnungspaket nicht exportiert.
- **Aktivkohlefiltration:** PFAS- / Durchbruchsberechnungen laufen in der **Entwurfsansicht**. Der anlagenweite Qualitätslauf wendet derzeit **keine** PFAS-Entfernung auf dem Produktstrom an (optionale Spritzbelüftung an diesem Block kann weiterhin wirken).
- Kein Excel-, CSV- oder GIS-Import von Wasseranalysen; die Zusammensetzung wird bei Gewinnen (und ähnlichen Formularen) eingegeben.
- Keine Benutzerkonten; Persistenz ist Browser-Speicher plus heruntergeladene JSON.
- Engine-Fehler können als generischer ungültiger Zustand mit wenig Solver-Detail erscheinen.
- Spritzbelüftung als eigenständiger Bibliotheksblock kann fehlschlagen, wenn der Sauter-Durchmesser nicht gesetzt ist (nur notieren, falls beim Schreiben noch wahr).
- Stationäre Modelle: keine Zeitreihen-Anlagensteuerung, kein SCADA.
- Zeichenflächen-Koordinaten sind keine Landkarte.
- Die Nutzerdokumentation ist Englisch, Niederländisch, Deutsch und Französisch. Die Architekturdokumentation ist nur Englisch.
