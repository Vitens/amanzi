---
lang: nl
title: Kengetallen
type: reference
audience: everyone
status: outline
---

# Kengetallen

Opzoekwaarden die berekeningen delen. Bron van waarheid: `amanzi/database/key_figures.csv`. De UI kan ze per project en per scenario overschrijven.

## Inhoud om te schrijven

- Kolommen: name, category, type, default, UOM, remarks.
- Categorieën die de UI groepeert: algemeen (operationeel en emissie), chemicaliën (emissiefactoren), en de overige groepen zoals ze verschijnen na vullen uit de CSV (PFAS-limieten, materialen).
- Voorbeelden bij het vullen: `carbon_intensity_grid` (gCO₂/kWh), put- en boosterrendementen (%), chemische emissiefactoren (gCO₂/g AS), methaanemissiefactor, nieuw vs geregenereerd aktiefkool.
- PFAS-gerelateerde limieten als kengetallen: Sum4, Sum20, PEQ (exacte sleutels bij vullen uit CSV).
- Overschrijvingen: project `key_figure_overwrites` en scenario-overschrijvingen.
- Ontbrekend kengetal bij runtime geeft een fout.

Vul later uit `key_figures.csv`; plak niet de hele CSV in deze outline.
