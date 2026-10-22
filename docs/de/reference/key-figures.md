---
lang: de
title: Kennzahlen
type: reference
audience: everyone
status: outline
---

# Kennzahlen

Nachschlagewerte, die über Berechnungen hinweg geteilt werden. Quelle der Wahrheit: `amanzi/database/key_figures.csv`. Die UI kann sie pro Projekt und pro Szenario überschreiben.

## Inhalt zum Schreiben

- Spalten: Name, Kategorie, Typ, Standard, UOM, Bemerkungen.
- Kategorien, die die UI gruppiert: allgemein (Betrieb und Emission), Chemikalien (Emissionsfaktoren) und die übrigen Gruppen, wie sie nach dem Füllen aus der CSV erscheinen (PFAS-Grenzwerte, Materialien).
- Beispiele zum Auflisten beim Füllen: `carbon_intensity_grid` (gCO₂/kWh), Brunnen- und Booster-Wirkungsgrade (%), chemische Emissionsfaktoren (gCO₂/g AS), Methan-Emissionsfaktor, neue vs regenerierte Aktivkohle.
- PFAS-bezogene Grenzwerte als Kennzahlen gespeichert: Sum4, Sum20, PEQ (genaue Schlüssel beim Füllen aus der CSV).
- Überschreibungen: Projekt-`key_figure_overwrites` und Überschreibungen auf Szenarioebene.
- Fehlende Kennzahl zur Laufzeit wirft einen Fehler.

Später aus `key_figures.csv` füllen; nicht die ganze CSV in dieses Outline einfügen.
