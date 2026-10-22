---
lang: en
title: Compare in the report
type: how-to
audience: everyone
status: draft
---

# Compare in the report

The panel on the right updates as you edit. It shows quality, quantity, energy, and sustainability for the scenario that is open.

The report is the detailed view of that scenario, and the place where every scenario in the project is drawn side by side.

## Open the report

Click **Calculate project** on the top bar. The same command is under **Project**.

The report opens on **Single model**, for the scenario that is selected.

- **Water quality** — bars for each unit on the train. The list chooses the parameter (pH, hardness, and the rest). The two icons beside the list switch between ordinary bars and a step chart. The long list is the path through the plant. The table under the chart has the same numbers. Rest the pointer on a column to see how that step differs from the previous one. **Copy** puts the table on the clipboard.
- **Energy** — per m³ treated, per m³ delivered, and total consumption.
- **Sustainability** — the same kind of chart for CO₂.

Quantity (abstraction, distribution, loss) stays on the right-hand panel. It is drawn in the report when you turn on **Comparison**.

<video controls preload="metadata" src="../media/OpenReport.mp4" style="max-width: 100%; height: auto;" aria-label="Open the report, switch water-quality parameters, and copy the table">
Click Calculate project. Switch from pH to hardness, toggle the step chart, open energy and sustainability, then copy the water-quality table.
</video>

## Compare two scenarios

A comparison needs two scenarios that are not identical.

1. On the scenario tab at the bottom, click **⋮** and choose **Duplicate**. Name the copy and confirm with **Add scenario**.
2. On the copy, change one design choice. Double-click the unit. Under **Dosage**, set the number and press Enter. In the demo, **Pelletontharding** → **Base dosage** is lowered from 2 to 0.5. The dosing curves move with the number. See [Configure a unit](configure-a-unit.md).
3. Click **Calculate project**.
4. Turn on **Comparison**.

The scenario list at the top is disabled while **Comparison** is on, because every scenario is already on the page.

The comparison is grouped under four headings. On screen those headings are **Kwantiteit**, **Waterkwaliteit**, **Energie**, and **Duurzaamheid** (quantity, water quality, energy, sustainability). Each group has a chart and a table. The buttons or the list choose which number you are comparing.

A dose change shows up in water quality and sustainability. Quantity stays the same when you only change a chemical dose.

**Compact** (the switch labelled **Uitgebreid** / **Compact**) keeps the four charts and hides the tables.

<video controls preload="metadata" src="../media/DuplicateAndChange.mp4" style="max-width: 100%; height: auto;" aria-label="Duplicate Scenario 1 as Lower dose and lower the softening base dosage">
Open the scenario menu, duplicate Scenario 1 as Lower dose, double-click Pelletontharding, and set Base dosage to 0.5.
</video>

<video controls preload="metadata" src="../media/CompareScenarios.mp4" style="max-width: 100%; height: auto;" aria-label="Turn on Comparison and Compact to see both scenarios">
Click Calculate project, turn on Comparison, and switch to Compact. Quantity matches; hardness and CO₂ do not.
</video>

## Read one scenario, then come back

Turn **Comparison** off to return to **Single model**. The list at the top chooses which scenario's charts you are reading. Each scenario keeps its own numbers.

Turn **Comparison** on again. Both scenarios are still there. Closing the report does not remove them.

<video controls preload="metadata" src="../media/SwitchScenarioInReport.mp4" style="max-width: 100%; height: auto;" aria-label="Leave comparison, switch the scenario list, then turn comparison back on">
Turn Comparison off, read Scenario 1, switch the list to Lower dose, then turn Comparison on again. Both scenarios are still listed.
</video>

## What the report leaves out

The report does not open the design dialog of one unit. Double-click a block for that. The dialog has the unit schematic, **Mass balance**, **Hydraulic line**, and **Design tables**. More on that dialog is in [Use design view](use-design-view.md).

A membrane's element-by-element tables are in that dialog, not in the report. The demo plant has no membrane. The clip opens **Nafiltratie**, which is the same gesture.

<video controls preload="metadata" src="../media/DesignNotInReport.mp4" style="max-width: 100%; height: auto;" aria-label="Close the report and open Nafiltratie design view">
Close the report, double-click Nafiltratie, and open the schematic, the design tables, and the mass balance.
</video>

## Keep a copy of the numbers

The report has no print command and no file export. **Copy** on a table copies that table (shown in the first clip). **Project → Download** writes the project as JSON. That file is the inputs. Opening it again is described in [Save, load, download](save-load-download.md).

<video controls preload="metadata" src="../media/DownloadProject.mp4" style="max-width: 100%; height: auto;" aria-label="Download the project JSON from the Project menu">
Open the Project menu and click Download.
</video>
