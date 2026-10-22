---
lang: de
title: Menge, Energie, Chemikalien, CO₂
type: explanation
audience: everyone
status: outline
---

# Menge, Energie, Chemikalien, CO₂

Was die nicht-qualitätsbezogenen Ergebnisfamilien bedeuten und wie sie von Kennzahlen abhängen.

## Inhalt zum Schreiben

- **Menge:** Gewinnen vs geliefertes Wasser vs Verluste (einschließlich Abfall und nicht wiederverwendeter Spülung).
- **Energie:** kWh/m³ und Jahressummen; Brunnenpumpen, Booster, Gebläse, Vakuum, Hochdruck-Membranpumpen — Wirkungsgrade aus Kennzahlen (`well_efficiency`, `booster_efficiency`, …).
- **Chemikalien:** Massen aus Dosierung, Enthärtung, Kohleaustausch, Membranchemikalien wie implementiert; Einheiten g AS/m³.
- **Nachhaltigkeit:** `electricity_consumption × carbon_intensity_grid` plus Emissionsfaktoren pro Chemikalie plus Methan wo angewendet; gCO₂-eq/m³ und pro Jahr.
- Eine Kennzahl ändern ändert CO₂ ohne die Anlage neu zu zeichnen — das ist der Sinn von Überschreibungen.
- Diese Familien sind Bilanzierung auf der hydraulischen/qualitativen Lösung, keine separate physikalische Simulation.

## Diagramme

- Mermaid: Qualität/Hydraulik lösen → Energie & Chemikalien → mit Kennzahlenfaktoren multiplizieren → CO₂.
