# Cascade Model

## Overview

The cascade model simulates cascade aeration systems used for gas transfer processes in water treatment. It performs gas exchange between water and air through multiple cascade steps, removing dissolved gases like CO₂ and CH₄ while adding oxygen to the water.

## Model Components

The cascade model inherits from both the base `Model` class and the `Balance` class, enabling it to handle mass balance calculations and gas transfer processes.

## Key Parameters

| Parameter | Description | Units |
| --- | --- | --- |
| `number_of_steps` | Number of cascade steps | - |
| `step_height` | Height of each cascade step | m |

## Gas Transfer Properties

The model calculates gas transfer efficiency and saturation concentrations for different gases based on the cascade step height. The properties are calculated at 10°C:

### Oxygen (O₂)
- **Transfer efficiency**: $k_{eff} = 28.85 \cdot \ln(h) + 50.066$
- **Saturation concentration**: 11.3 mg/L
- **Molecular weight**: 32 g/mol

### Carbon Dioxide (CO₂)
- **Transfer efficiency**: $k_{eff} = 0.6832 \cdot \ln(h) + 15.017$
- **Saturation concentration**: 0.79 mg/L
- **Molecular weight**: 44 g/mol

### Methane (CH₄)
- **Transfer efficiency**: $k_{eff} = -19.196 \cdot h^2 + 75.161 \cdot h - 0.3$
- **Saturation concentration**: 0.023 mg/L
- **Molecular weight**: 16 g/mol

Where $h$ is the step height in meters.

## Gas Transfer Calculation

The model calculates gas concentration changes for each gas using the following equation:

$$ \Delta C = (C_s - C_{in}) \cdot (1 - (1 - k_X)^n) $$

Where:
- $\Delta C$ = concentration change (mg/L)
- $C_s$ = saturation concentration (mg/L)
- $C_{in}$ = influent concentration (mg/L)
- $k_X$ = transfer efficiency coefficient (dimensionless)
- $n$ = number of cascade steps

The transfer efficiency coefficient is calculated as:
$$ k_X = \frac{k_{eff}}{100} $$

## Aeration Process

The aeration process follows these steps:

1. **Gas Property Calculation** - Determine transfer efficiency and saturation concentrations
2. **Concentration Conversion** - Convert influent concentrations to mg/L
3. **Transfer Calculation** - Calculate concentration changes for each gas
4. **Solution Update** - Apply concentration changes to the water solution

## Design Calculations

### Oxygen Saturation

The model calculates oxygen saturation by interacting the influent water with air at atmospheric conditions:

```python
air_composition = {
    'O2(g)': 0.208,    # 20.8% oxygen
    'Ntg(g)': 0.7916,  # 79.16% nitrogen
    'CO2(g)': 0.0004,  # 0.04% carbon dioxide
    'Mtg(g)': 0,       # 0% methane
    'H2Sg(g)': 0,      # 0% hydrogen sulfide
    'H2O(g)': 0,       # 0% water vapor
}
```

### Efficiency Calculations

The model calculates removal and transfer efficiencies:

**CO₂ Removal Efficiency:**
$$ \text{Efficiency} = \left(1 - \frac{C_{effluent}}{C_{influent}}\right) \times 100\% $$

**CH₄ Removal Efficiency:**
$$ \text{Efficiency} = \max\left(0, \left(1 - \frac{C_{effluent}}{C_{influent} + 10^{-6}}\right)\right) \times 100\% $$

**O₂ Saturation Efficiency:**
$$ \text{Efficiency} = \frac{C_{effluent}}{C_{saturation}} \times 100\% $$

## Design Output

The model provides comprehensive design output including:

### Water Quality Parameters
- **pH** - Acidity/alkalinity
- **CH₄** - Methane concentration (mg/L)
- **N₂** - Nitrogen concentration (mg/L)
- **CO₂** - Carbon dioxide concentration (mg/L)
- **O₂** - Oxygen concentration (mg/L)

### Performance Charts
The model generates performance charts showing the relationship between:
- Number of cascade steps vs. water quality parameters
- Removal efficiencies for CO₂ and CH₄
- Oxygen saturation efficiency

### Influent vs. Effluent Comparison
- Direct comparison of influent and effluent water quality
- Quantification of gas transfer performance

## Integration with Solver

The cascade model integrates with the overall solver framework by:

1. **Mass Balance** - Calculates water flows through the cascade
2. **Quality Calculation** - Processes gas transfer reactions
3. **Design Parameters** - Calculates cascade dimensions and performance
4. **Energy Calculation** - Determines pumping requirements for cascade operation
5. **Performance Analysis** - Generates efficiency curves and design charts


