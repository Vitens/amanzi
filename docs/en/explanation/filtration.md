---
title: Filtration
type: explanation
audience: keyuser
status: outline
---

# Filtration

Rapid sand vs marble contact filtration: oxidation sequence, calcite, backwash.

## Content to write

- Shared idea: oxygen-limited oxidation on a granular bed, then precipitation.
- Sequence used in code: CH₄ → Fe²⁺ → H₂S → NH₄ → NO₂ → Mn; `desaturate` Fe(OH)₃, Manganite.
- **Sand:** optional suppression efficiencies; dual media (anthracite + sand); spray polynomial (TU Delft / Dresden fit) when spray is on.
- **Marble:** `saturate("Calcite", 0)` after steps — pH buffering; production model vs unpublished GJ variant (do not document GJ as a library unit).
- Backwash: mass of iron in flush; Kozeny–Carman headloss; expansion; 15 °C viscosity assumption where used.
- Design view stepwise speciation table vs the simpler plant `run_quality` path.
- Headloss mixin (`Loss`) vs quantity of filtrate vs flush.

## Diagrams

- Mermaid: oxidation chain; sand vs marble branch at calcite saturation.
