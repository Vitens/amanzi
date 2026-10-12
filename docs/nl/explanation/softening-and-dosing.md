---
lang: nl
title: Ontharding en dosering
type: explanation
audience: keyuser
status: outline
---

# Ontharding en dosering

Pelletontharding (calciet-SI-doel, bypass, zuur) en het generieke doseringsblok.

## Inhoud om te schrijven

- Pelletreactor: doseer base → optionele Fe/Mn-carbonaatvangst → `desaturate('Calcite', to_si=…)` → optioneel zuur → meng met bypass.
- Bypass als hydraulische/kwaliteitsblend, geen aparte bibliotheek-Splitsing.
- Seed- / fluidisatie-porositeitshulp.
- Doseringschemicaliën en modi: constant mmol/L vs setpoint (pH, SI, AggCO₂, CCPP90); influent- vs effluentpositie.
- Sustainability: chemische emissiefactoren uit kengetallen (natronloog, lime, CO₂, …).
- Ontwerpgrafieken: doseringssweeps, stapprofielen (pH, hardheid, CCPP, sc).
- Eerlijkheid: sommige ontwerp-massabalans-placeholders kunnen nog hardcoded zijn — verifieer tegen de code bij het schrijven van proza.

## Diagrammen

- Mermaid: influent → (reactor vs bypass) → zuur? → blend → product.
