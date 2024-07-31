# Solver steps

## Solving a scenario

**1. Solve Mass Balance**

Calculate the water flows in the network by solving the mass balance

**2. Solve Chemical model**

Recursive walk through model from emitter to output model, run quality calculation for every model

**3. Calculate design output parameters**

Calculate all design output parameters for all models

**4. Calculate energy consumption**

Use design outputs as input, run energy calculation to determine required heads in the model, calculate other consumers

**5. Calculate Chemical Consumption**

Sum chemical consumption per model and chemical

**6. Calculate CO2 emissions**

Convert energy to CO2eq, chemicals to CO2eq, gather direct process emissions (CO2, CH4) and indirect emissions (power generation from captured CH4)

**7. Generate summary**

Summarize production, quality, energy, chemical and CO2 per model and calculate totals for the whole scenario

## Solving a Project

**1. Solve individual scenarios**

**2. Summarize metrics**
