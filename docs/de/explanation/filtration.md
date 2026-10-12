---
lang: de
title: Filtration
type: explanation
audience: keyuser
status: outline
---

# Filtration

Schnellfiltration vs Marmorkontaktfiltration: Oxidationssequenz, Calcit, Rückspülung.

## Inhalt zum Schreiben

- Gemeinsame Idee: sauerstoffbegrenzte Oxidation auf einem körnigen Bett, dann Fällung.
- Im Code genutzte Sequenz: CH₄ → Fe²⁺ → H₂S → NH₄ → NO₂ → Mn; `desaturate` Fe(OH)₃, Manganit.
- **Sand:** optionale Unterdrückungswirkungsgrade; Dualmedien (Anthrazit + Sand); Spritz-Polynom (TU Delft / Dresden-Fit), wenn Spray an ist.
- **Marmor:** `saturate("Calcite", 0)` nach Schritten — pH-Pufferung; Produktionsmodell vs unveröffentlichte GJ-Variante (GJ nicht als Bibliothekseinheit dokumentieren).
- Rückspülung: Eisenmasse in der Spülung; Kozeny–Carman-Druckverlust; Expansion; 15 °C-Viskositätsannahme wo verwendet.
- Entwurfsansicht mit schrittweiser Speziationstabelle vs dem einfacheren Anlagen-`run_quality`-Pfad.
- Druckverlust-Mixin (`Loss`) vs Menge an Filtrat vs Spülung.

## Diagramme

- Mermaid: Oxidationskette; Sand vs Marmor-Zweig bei Calcitsättigung.
