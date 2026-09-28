---
title: Aeration
type: explanation
audience: keyuser
status: outline
---

# Aeration

Packed tower, spray, plate, and cascade in Amanzi: what each model does and which correlations it uses.

## Content to write

- Why groundwater works aerate: CH₄, CO₂, O₂, VOC.
- **Tower:** Onda *k_L a* / HTU → NTU efficiency; Engel–Stichlmair holdup, ΔP, flooding; blower as isentropic compression; Henry and diffusion from `tower/compounds.py`; packing catalog (Raflux).
- **Spray:** penetration theory *k = 2(A/V)√(D t / π)*; fall time *√(2h/g)*; optional Sauter diameter issue.
- **Plate:** PHREEQC `interact` with optional recirculated off-gas (few iterations).
- **Cascade:** empirical *k_eff*(log step height); ΔC = (C_sat − C_in)(1 − (1 − k)^steps); CH₄ C_sat from Duan & Mao 2006.
- When to pick which (qualitative): packed tower vs cheap spray/cascade vs plate; VOC stripping favours the tower.
- Membrane/vacuum degassing compared in one paragraph; details on [Membranes](membranes.md).
- Citations listed fully on [Literature](literature.md).

## Diagrams

- Mermaid comparison: four aeration blocks → gases they target.
