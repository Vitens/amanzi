---
title: Softening and dosing
type: explanation
audience: keyuser
status: outline
---

# Softening and dosing

Pellet softening (calcite SI target, bypass, acid) and the generic dosing block.

## Content to write

- Pellet reactor: dose base → optional Fe/Mn carbonate capture → `desaturate('Calcite', to_si=…)` → optional acid → mix with bypass.
- Bypass as a hydraulic/quality blend, not a separate library splitter.
- Seed / fluidization porosity helper.
- Dosing chemicals and modes: constant mmol/L vs setpoint (pH, SI, AggCO₂, CCPP90); influent vs effluent position.
- Sustainability: chemical emission factors from key figures (lye, lime, CO₂, …).
- Design charts: dosage sweeps, step profiles (pH, hardness, CCPP, sc).
- Honesty: some design mass-balance placeholders may still be hardcoded — verify against code when writing prose.

## Diagrams

- Mermaid: influent → (reactor vs bypass) → acid? → blend → product.
