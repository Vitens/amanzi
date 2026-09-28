---
title: Membranes
type: explanation
audience: keyuser
status: outline
---

# Membranes

RO/NF stacks, membrane contactors, and vacuum degassing.

## Content to write

- **RO/NF:** recovery split; permeate vs concentrate (waste); *Kw* from manufacturer test data and 3 %/°C correction; osmotic pressure (NaCl coefficient); spacer headloss; stage pressure solve; optiflux flag.
- Element database (CSV) → selectable types (ESPA2-LD, AK-400H, …).
- Quality via rejection, not full ion-exchange membranes.
- **Membrane degassing:** 1–2 stage vacuum contactor; PHREEQC `interact` with N₂/CO₂ sweep at set vacuum; empirical ΔP vs load.
- **Vacuum stripper:** equilibrium at variable pressure; design charts pH/SI/gas vs vacuum; H₂S must be H₂S not Seaborgium (historical bug, fixed 1.0.2).
- When RO vs aeration vs vacuum for gases vs salts.

## Diagrams

- Mermaid: feed → stages → permeate (product) + concentrate (waste).
