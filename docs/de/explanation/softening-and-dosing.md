---
lang: de
title: Enthärtung und Dosierung
type: explanation
audience: keyuser
status: outline
---

# Enthärtung und Dosierung

Pelletontharding (Calcit-SI-Ziel, Bypass, Säure) und der generische Dosierungsblock.

## Inhalt zum Schreiben

- Pelletreaktor: Base dosieren → optionale Fe/Mn-Carbonatbindung → `desaturate('Calcite', to_si=…)` → optionale Säure → mit Bypass mischen.
- Bypass als hydraulische/qualitative Mischung, kein separater Bibliotheks-Teilen.
- Saatgut- / Fluidisierungs-Porositäts-Hilfsfunktion.
- Dosierchemikalien und Modi: konstant mmol/L vs Sollwert (pH, SI, AggCO₂, CCPP90); Zulauf- vs Ablaufposition.
- Nachhaltigkeit: chemische Emissionsfaktoren aus Kennzahlen (Lauge, Kalk, CO₂, …).
- Entwurfsdiagramme: Dosiersweep, Schrittprofile (pH, Härte, CCPP, sc).
- Ehrlichkeit: einige Entwurfs-Stoffbilanz-Platzhalter können noch hartcodiert sein — beim Schreiben der Prosa gegen den Code prüfen.

## Diagramme

- Mermaid: Zulauf → (Reaktor vs Bypass) → Säure? → Mischung → Produkt.
