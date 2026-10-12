---
lang: nl
title: Filtratie
type: explanation
audience: keyuser
status: outline
---

# Filtratie

Snelle zandfiltratie vs marblecontactfiltratie: oxidatievolgorde, calciet, spoeling.

## Inhoud om te schrijven

- Gedeeld idee: zuurstofbegrensde oxidatie op een granulair bed, daarna precipitatie.
- Volgorde in de code: CH₄ → Fe²⁺ → H₂S → NH₄ → NO₂ → Mn; `desaturate` Fe(OH)₃, Manganite.
- **Zand:** optionele onderdrukkingsefficiënties; dual media (antraciet + zand); sproeipolynoom (TU Delft / Dresden-fit) als sproei aan staat.
- **Marble:** `saturate("Calcite", 0)` na stappen — pH-buffering; productiemodel vs ongepubliceerde GJ-variant (documenteer GJ niet als bibliotheekunit).
- Spoeling: ijzermassa in spoelwater; Kozeny–Carman headloss; expansie; viscositeitsaanname 15 °C waar gebruikt.
- Ontwerpweergave stapsgewijze speciatietabel vs het eenvoudigere plant-`run_quality`-pad.
- Headloss-mixin (`Loss`) vs hoeveelheid filtraat vs spoeling.

## Diagrammen

- Mermaid: oxidatieketen; zand vs marble-tak bij calcietverzadiging.
