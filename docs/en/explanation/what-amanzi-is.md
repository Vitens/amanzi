---
lang: en
title: What Amanzi is
type: explanation
audience: novice
status: draft
---

# What Amanzi is

Amanzi is a design tool for drinking-water treatment, built by Vitens. A treatment scenario is a drawing of a plant plus the numbers that drawing implies: how much water moves, what is in it, how much energy and chemical the plant uses, and the CO₂ that follows from those uses. Comparing two scenarios means comparing two such drawings. Doing that in a spreadsheet splits the drawing from the calculation. Amanzi keeps them in one project.

You get a flowsheet, several what-if versions of it, and four families of results on the plant: quantity, quality, energy, and sustainability. Chemical use sits inside the units and in the CO₂ account. The [tutorials](../tutorials/index.md) walk the demo. The [how-to guides](../how-to/index.md) say how to change a unit, a key figure, or a file. The [reference](../reference/index.md) lists fields. This section says why the numbers come out as they do.

Amanzi is a calculator for a design you are considering. It does not operate a plant, replace a laboratory analysis, or stand in for a permit or a construction drawing. It also does not replay a day of operation. Each scenario is one steady operating point.

The calculation runs in the browser. The hosted demo and a copy you serve yourself use the same idea: the project stays on the computer where the page is open, and the chemistry engine loads there. There is no plant model waiting on a server. Opening either one is described in [Open hosted or local](../how-to/open-hosted-or-local.md).

Amanzi is licensed under the GNU General Public License, version 3. The About dialog in the app shows that notice and a BibTeX entry for the software, with Vitens as author and the address `https://github.com/Vitens/Amanzi`. The year and version in that entry follow the copy you have open.
