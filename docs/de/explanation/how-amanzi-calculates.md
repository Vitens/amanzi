---
lang: de
title: Wie Amanzi berechnet
type: explanation
audience: keyuser
status: outline
---

# Wie Amanzi berechnet

Die Engine hinter der Zeichenfläche. Reihenfolge der Solver, PHREEQC, Rückführungen und Entwurf vs Anlagenlauf.

## Inhalt zum Schreiben

- JSON-Projekt → `Project` / `Scenario` → Modelle instanziiert nach Typnamen → Verbindungen.
- Solver-Reihenfolge: **Menge → Qualität → Hydraulik → Energie → Chemikalien → Nachhaltigkeit**.
- Menge: Stoffbilanz auf Produkt/Abfall/Spülung; Teilen und Rückführungen.
- Qualität: PHREEQC (`phreeqpython.Solution`) wandert den Graphen ab; extraneous-Dict für PFAS, VOC, Sonstige, TOC, Farbe (nicht in der PHREEQC-Datenbank).
- Rückführungs- / Emitter-Iteration: bis zu 100 Durchläufe, Genauigkeit 0.0001; Fehler ist eine Stoffbilanz-Ausnahme.
- Hydraulik: Druckhöhen, Booster, Druckverlust-Mixins (Balance, Loss, Splitter).
- Energie, Chemikalien, dann CO₂ aus Energie + chemischen Emissionsfaktoren + Prozessemissionen (Kennzahlen).
- **`design()` vs `run_quality()`:** die Entwurfsansicht kann reichhaltigere Physik ausführen (GAC-Durchbruch, Turm-Flutungsdiagramme) als der anlagenweite Qualitätslauf. Die GAC-Lücke explizit nennen.
- Parametrisches YAML: Eingaben, Gleichungsergebnisse, `if`-Sichtbarkeit, Validierungsausdrücke — nur Konzept, keine Schema-Spezifikation.

## Diagramme

- Mermaid-Sequenz der sechs Solver, dann eine Qualitätsschleife über Rückführungen.
