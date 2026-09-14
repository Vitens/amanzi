---
title: Limitations
type: reference
audience: everyone
status: outline
---

# Limitations

Facts about what the current product does not do. No workarounds beyond pointing at the UI that *does* exist.

## Content to write

- **Ion exchange** is not in the process library and is not exported in the calculation package.
- **Activated carbon:** PFAS / breakthrough calculations run in **design view**. The plant-wide quality walk does **not** currently apply PFAS removal on the product stream (optional spray aeration on that block still can).
- No Excel, CSV, or GIS import of water analyses; composition is entered on Abstraction (and similar forms).
- No user accounts; persistence is browser storage plus downloaded JSON.
- Engine failures can surface as a generic invalid state with little solver detail.
- Spray aeration as a standalone library block may error if Sauter diameter is unset (note only if still true when writing).
- Steady-state models: no time-series plant control, no SCADA.
- Canvas coordinates are not a map.
- Documentation language is English only; UI has en/nl/de.
