---
lang: nl
title: Stromen
type: reference
audience: everyone
status: outline
---

# Stromen

Verbindingen tussen procesunits. Drie typen; elke unit toont ankers die bedraad moeten worden als ze niet optioneel zijn.

## Inhoud om te schrijven

- **Productstroom** (blauw): behandeld of doorgestuurd water langs de hoofdtrein.
- **Afvalstroom** (rood): concentraat, pekel of afgevoerde stroom naar een afval-sink.
- **Spoeling** (gestippeld blauw): spoelwater / filterwaswater, vaak richting hergebruik of afval.
- Verplichte vs optionele ankers; de melding “not fully connected”.
- Recyclelussen: Spoelwaterhergebruik/Splitsing kan water terugsturen; de kwaliteitssolver itereert tot de massabalans convergeert (alleen feit; waarom staat in [Hoe Amanzi rekent](../explanation/how-amanzi-calculates.md)).
- Een scenario zonder bron of zonder Levering kan niet worden opgelost.

## Diagrammen

- Mermaid: bron → unit (product) → Levering, met afval- en spoelzijranden.
