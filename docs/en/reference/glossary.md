---
lang: en
title: Glossary
type: reference
audience: everyone
status: draft
---

# Glossary

**Abstraction.** The groundwater source block. Library name **Abstraction**.

**AggCO₂.** Aggressive carbon dioxide, the CO₂ that can still dissolve calcite.

**Backwash.** Wash water that cleans a filter bed. On the canvas it is a flush stream.

**Canvas.** The drawing of units and streams. Also called the flowsheet.

**CCPP, TACC₉₀.** Calcium-carbonate precipitation potential. The panel label is **TACC₉₀**. The dosing target is `CCPP90`.

**EGV.** Electrical conductivity, mS/m. The key-figure tag for the related limit is `sc20`.

**Flush.** The dotted stream. Backwash and other wash water.

**HTU, NTU.** Height of a transfer unit, and the number of them. The packed tower uses both.

**Key figure.** A shared lookup: an efficiency, an emission factor, or a quality limit. Tag, default, and unit live in the key-figure list.

**Kw.** Water permeability of a membrane element, m³/(m²·bar·h), from the manufacturer test row and a temperature correction.

**NF.** Nanofiltration. In this app it is a membrane-stack element type, not a separate block.

**Output.** The sink of the product stream. Library name **Output**. The demo block is often named **Levering**.

**Pellet softening.** The calcite pellet reactor. The library name is **Pelletontharding**.

**PHREEQC.** The chemistry engine. Amanzi calls it through PhreeqPython in the browser.

**Product.** The blue stream. Water that continues toward delivery.

**Project.** The file of one or more scenarios, plus project key-figure overwrites. JSON on disk. A browser copy as well, after Save.

**RQ.** Air-to-water ratio on an aerator. Dimensionless.

**RO.** Reverse osmosis. The membrane filtration block.

**Scenario.** One version of the plant inside a project. One steady operating point.

**SI.** Saturation index of calcite, unless a unit says otherwise.

**TAC.** Alkalinity as shown on the quality panel.

**TH.** Hardness as labelled on the pellet-softening drawing. The plant panel calls the plant result **Hardness**.

**Waste.** The red stream. Water that is not delivered as drinking water.
