---
lang: en
title: Set key figures
type: how-to
audience: everyone
status: draft
---

# Set key figures

Key figures are shared numbers: emission factors, pump efficiencies, and quality limits. Leave them alone while you draw the plant. Change one when the assumption should change, for example the electricity emission factor, or a quality limit you have to design to. A unit's own settings stay on the unit. See [Configure a unit](configure-a-unit.md).

The panel on the right shows the result of those numbers. The list itself is a dialog. The database behind the list is described in [Key figures](../reference/key-figures.md).

## Open the list

Click **Key figures** on the top bar. The same command is under **Project**.

The columns are **Name**, **Tag**, **Default**, **Project**, **Scenario**, and **UOM**. **Default** is the built-in value. An empty **Project** or **Scenario** cell is not an override. The grey number in the box is that default, shown so you know what you would be replacing.

**Filter...** narrows the list. Capitals matter. `electricity` finds **Emission factor for electricity** (tag `carbon_intensity_grid`, 250 gCO₂/kWh). `hardness` finds the hardness limits under **Quality standards**.

The quality limits in this list are rows such as pH, hardness, iron, and manganese. Sum4, Sum20, and PEQ are not in this version of the list.

<video controls preload="metadata" src="../media/SearchKeyFigures.mp4" style="max-width: 100%; height: auto;" aria-label="Open Key figures and filter for electricity, then hardness">
Click Key figures. Filter for electricity, then for hardness.
</video>

## A project value applies to every scenario

Type in the **Project** cell. The row turns yellow. The filter button shows how many figures you have changed.

In the clip the electricity factor goes from 250 to 100 gCO₂/kWh. Close the dialog. On the right, **Specific emissions** fall from 335 to 299 gCO₂-eq/m³, and **Total emissions** from 3177 to 2840 ton CO₂-eq/y. Every scenario uses that project value unless its own **Scenario** cell is filled.

<video controls preload="metadata" src="../media/ProjectKeyFigure.mp4" style="max-width: 100%; height: auto;" aria-label="Set the project electricity factor to 100 and watch specific emissions fall">
Type 100 in the Project cell for the electricity factor. Specific emissions fall from 335 to 299.
</video>

## A scenario value applies to one scenario

Duplicate the scenario when that copy should use a different assumption. On the copy, type in the **Scenario** cell. That number wins over the project value for this scenario only. The other scenarios keep the project value.

In the clip **High grid** sets the electricity factor to 500. Its specific emissions are 394 gCO₂-eq/m³. **Scenario 1** has an empty scenario cell, so it keeps the project value of 100 and stays at 299.

<video controls preload="metadata" src="../media/ScenarioKeyFigure.mp4" style="max-width: 100%; height: auto;" aria-label="Duplicate a scenario and set its electricity factor to 500">
Duplicate the scenario as High grid and type 500 in the Scenario cell. Specific emissions rise to 394.
</video>

## See only your changes, then clear a cell

The button beside the filter shows only the rows you have changed. The count on it is how many.

The orange icon in a cell clears that cell. The row then uses the database default again, unless the other column still has a number. Clearing the scenario cell leaves the project number in force. Clearing the project cell as well returns the built-in 250. In the clip, specific emissions return to 335.

<video controls preload="metadata" src="../media/RestoreKeyFigure.mp4" style="max-width: 100%; height: auto;" aria-label="Filter to changed key figures and clear the project and scenario cells">
Show only the changed row, clear the scenario cell, then the project cell. Specific emissions return to 335.
</video>
