---
lang: en
title: Compare scenarios
type: tutorial
audience: novice
status: draft
---

# Compare scenarios

A scenario is one version of the plant, but there are always multiple ways to build a water treatment. Seeing what the best choice might be Amanzi can compare the scenarios with the calculate project button on the top right. 
The tabs sit at the bottom. Copy the layout, change one number, and read both versions in the report.

## Copy the layout

On the scenario tab, click the options control (⋮) and choose **Duplicate**. Name the copy (the clip uses **Lower dose**) and confirm with **Add scenario**.

The **+** beside the tabs opens a blank scenario: an empty canvas.

On the copy, double-click **Pelletontharding**. Under **Dosage**, set **Base dosage** from 2 to 0.5 and press Enter. One design change is enough.

Notes on a scenario are for the reader. They do not change the calculation.

<video controls preload="metadata" src="../media/DuplicateAndChange.mp4" style="max-width: 100%; height: auto;" aria-label="Duplicate Scenario 1 as Lower dose and set Pelletontharding base dosage to 0.5">
On the scenario tab, choose Duplicate, name the copy Lower dose, and confirm with Add scenario. On that copy, double-click Pelletontharding and set Base dosage from 2 to 0.5 under Dosage.
</video>

## Read both versions

Click **Calculate project**. The report opens on **Single model**, for the scenario that is selected. The sections there are **Water quality**, **Energy**, and **Sustainability**. Quantity stays on the right-hand panel until you turn on **Comparison**.

Turn on **Comparison** to see every scenario and select the parameter you want to compare. 

Charts, **Copy**, and the **Compact** / **Detailed** switch are in [Compare in the report](../how-to/compare-in-report.md). How CO₂ is computed for the sustainability values is detailed in [Quantity, energy, chemicals, CO₂](../explanation/quantity-energy-chemicals-co2.md).

<video controls preload="metadata" src="../media/CompareScenarios.mp4" style="max-width: 100%; height: auto;" aria-label="Turn on Comparison and Compact to see both scenarios">
Click Calculate project, turn on Comparison, and switch to Compact. Quantity matches; hardness and CO₂ do not.
</video>


