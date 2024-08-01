# Energymodel

## Defining parameters

| Parameter | Description | Units |
| --- | --- | --- |
| $Z_{in}$       | Inlet height (height of inlet wier, pump inlet, height of reactor inlet, etc. | m |
| $Z_{out}$       | Outlet height (height of outlet, reactor overflow wier, etc. only defined for non-pressurized, upflow systems | m |
| $H_{in}$ | Required/Calculated hydraulic head at the inlet | m |
| $H_{out}$ | Available hydraulic head at the outlet | m |
| $\Delta_{H}$ | Total headloss in the model, defined by Delta_H_model + Delta_H_inlet | m |
| $\Delta_{H_{Model}}$ | Headloss in model, for example cascade fall height, filter bed resistance, etc | m |
| $\Delta_{H_{inlet}}$ | Headloss in model inlet, for example due to control valves or overflow wiers | m |
| *Pressurized* | Whether the model is pressurized or not | bool |
| *IntegratedBooster* | Whether the model comes with an integrated booster, i.e. RO, NF, membrane degassing | bool |


## Calculating H_in and H_out

The hydraulic head at the inlet $H_{in}$ and outlet $H_{out}$ are calculated based on whether the model is pressurized, comes with an integrated booster pump and whether the outlet height is heigher then the inlet height:

**1. Not pressurized, water flows in downward direction (cascades, open sand filters, tower aerators, vacuum systems, reservoirs)**

The required hydraulic head $H_{in}$ is defined as the height of the inlet $Z_{in}$ plus the headloss in the model inlet works $\Delta_{H_{inlet}}$

$$ H_{in} = Z_{in} + \Delta_{H_{inlet}} $$

The available hydraulic head in the outlet $H_{out}$ is defined as the height of the inlet $Z_{in}$ minus the headloss in the model $\Delta_{H_{Model}}$

$$ H_{out} = Z_{in} - \Delta_{H_{model}} $$

**2. Not pressurized, water flows in upward direction (pellet softening)**

If water flows upward, the required hydraulic head $H_{in}$ is defined as the height of the outlet $Z_{out}$ minus the height of the inlet $Z_{in}$ plus the inlet and model headloss:

$$ H_{in} = Z_{out} - Z_{in} + \Delta_{H_{inlet}} + \Delta_{H_{model}} $$

The available hydraulic head in the outlet $H_{out}$ is equal to the height of the outlet $Z_{out}$ 

$$ H_{out} = Z_{out} $$

**3. Pressurized, no integrated booster pump**

For pressurized models the *required* outlet head $H_{out}$ is defined as the required inlet head $H_{in, downstream}$ of the downstream model.

$$ H_{out} = H_{in, downstream} $$

The *required* inlet head $H_{in}$ is defined as the outlet head plus the total headloss in the model $\Delta_H$

$$ H_{in} = H_{out} + \Delta_H $$

The *actual* inlet and outlet heads may be increased by the upstream heads. In case of multiple pressurized feeding models the highest $H_{out}$ is taken as $H_{in}$

**4. Pressurized, with integrated booster pump**

If the model is equipped with an integrated booster pump the outlet head $H_{out}$ is equal to the inlet head $H_{in, downstream}$ of the downstream model.

The minimal required $H_{in}$ for the model is equal to the $Z_{in}$ (height of the booster pump inlet) plus $\Delta_{H_{inlet}}$ plus 1 meter to prevent cavitation.

$$ H_{in} = Z_{in} + \Delta_{H_{inlet}} + 1 $$

The head *added* by the booster pump should be enough to overcome the model headloss $\Delta_{H_{model}}$ and to reach the required $H_{out}$

$$ H_{booster} = H_{out} + \Delta_{H_{model}} - H_{in} $$

## Calculating Required Booster pumps ##

The required booster pumps are calculated by following the product flows from output to source models. Whenever the $H_{in}$ of a model is higher then the $_{out}$ of the upstream model, a booster pump is added to the connection to supply the required head.


