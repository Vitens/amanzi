---
lang: de
title: Aktivkohlefiltration
type: reference
audience: everyone
status: outline
---

# Aktivkohlefiltration

Bibliotheksname: **Aktivkohlefiltration**. GAC-Kontaktoren für PFAS und organische Mikroschadstoffe (TOC, Farbe), einschließlich Austausch und Staffelung in der **Entwurfsansicht**.

## Wann platzieren

Sie dimensionieren oder vergleichen GAC für PFAS- oder organische Mikroschadstoffentfernung.

## Ströme

- Ein: Produkt.
- Aus: Produkt; Spülung, wenn Filtrations-/Rückspülanker genutzt werden.

## Eingaben (UI-Gruppen)

- **Filtergeometrie:** rechteckig/rund, Länge/Breite oder Durchmesser, Betthöhe.
- **Kohle:** Packungstyp (NORIT-Supra-Optionen), scheinbare Dichte, Partikeldurchmesser, Porosität (sauber/verstopft).
- **PFAS / Mikroschadstoffe:** Freundlich *K* und *1/n* pro Verbindung, Konkurrenzkoeffizienten, PEQ, Entwurfsgrenzwert, Stoffübergangskoeffizient, Entfernungs-% aus Metadaten.
- **Austausch / Staffelung:** Intervall und Anzahl Filter in Rotation.
- Optionale Spritzbelüftungsfelder wenn aktiviert.

## Ausgaben / Entwurfstabellen

- Durchbruchskurven, Regenerationsintervall (Tage oder BV), EBCT, Zulauf-/Ablauf-OMV, Konkurrenzkoeffizienten.
- Energie / Chemikalien / Nachhaltigkeit für den Kohleaustausch.

## Einschränkung

Anlagenweites `run_quality` wendet derzeit keine PFAS-Entfernung an; nutzen Sie die Entwurfsansicht. Siehe [Einschränkungen](../limitations.md).

## Wissenschaft

[Aktivkohle und PFAS](../../explanation/activated-carbon-and-pfas.md).
