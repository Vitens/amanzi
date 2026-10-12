---
lang: nl
title: Hoe Amanzi rekent
type: explanation
audience: keyuser
status: outline
---

# Hoe Amanzi rekent

De engine achter het canvas. Volgorde van solvers, PHREEQC, recycles, en ontwerp vs plantwandeling.

## Inhoud om te schrijven

- JSON-project → `Project` / `Scenario` → modellen geïnstantieerd op typenaam → verbindingen.
- Solvervolgorde: **hoeveelheid → kwaliteit → hydraulica → energie → chemicaliën → sustainability**.
- Hoeveelheid: massabalans op product/afval/spoeling; Splitsing en recycles.
- Kwaliteit: PHREEQC (`phreeqpython.Solution`) loopt over de graaf; extraneous-dict voor PFAS, VOC, Overig, TOC, kleur (niet in de PHREEQC-database).
- Recycle- / emitter-iteratie: tot 100 passen, precisie 0.0001; falen is een massabalans-exception.
- Hydraulica: drukhoogtes, boosters, headloss-mixins (Balance, Loss, Splitter).
- Energie, chemicaliën, daarna CO₂ uit energie + chemische emissiefactoren + procesemissies (kengetallen).
- **`design()` vs `run_quality()`:** ontwerpweergave kan rijkere fysica draaien (GAC-doorbraak, overstromingsgrafieken van torens) dan de plantbrede kwaliteitswandeling. Noem de GAC-kloof expliciet.
- Parametrisch YAML: inputs, vergelijkingsoutputs, `if`-zichtbaarheid, validatie-expressies — alleen concept, geen schemaspecificatie.

## Diagrammen

- Mermaid-sequentie van de zes solvers, daarna een kwaliteitslus over recycles.
