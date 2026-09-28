---
title: How Amanzi calculates
type: explanation
audience: keyuser
status: outline
---

# How Amanzi calculates

The engine behind the canvas. Order of solvers, PHREEQC, recycles, and design vs plant walk.

## Content to write

- JSON project → `Project` / `Scenario` → models instantiated by type name → connections.
- Solver order: **quantity → quality → hydraulics → energy → chemicals → sustainability**.
- Quantity: mass balance on product/waste/flush; splitters and recycles.
- Quality: PHREEQC (`phreeqpython.Solution`) walking the graph; extraneous dict for PFAS, VOC, Other, TOC, colour (not in the PHREEQC database).
- Recycle / emitter iteration: up to 100 passes, precision 0.0001; failure is a mass-balance exception.
- Hydraulics: heads, boosters, headloss mixins (Balance, Loss, Splitter).
- Energy, chemicals, then CO₂ from energy + chemical emission factors + process emissions (key figures).
- **`design()` vs `run_quality()`:** design view can run richer physics (GAC breakthrough, tower flooding charts) than the plant-wide quality walk. State the GAC gap explicitly.
- Parametric YAML: inputs, equation outputs, `if` visibility, validation expressions — concept only, not a schema spec.

## Diagrams

- Mermaid sequence of the six solvers, then a quality loop over recycles.
