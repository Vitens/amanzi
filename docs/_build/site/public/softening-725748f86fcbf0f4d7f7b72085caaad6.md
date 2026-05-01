# Softening Model

## Overview

The softening model simulates pellet softening processes used for water hardness removal. It combines chemical dosing with precipitation reactions and includes bypass flow control and acid neutralization for pH adjustment.

![Softening](../images/modelimages/Pellet_softener.png)

## Model Components

The softening model inherits from both the base `Model` class and the `Balance` class, enabling it to handle mass balance calculations and chemical precipitation processes.

## Key Parameters

| Parameter | Description | Units |
| --- | --- | --- |
| `base_chemical` | Base chemical for softening (NaOH, Ca(OH)₂) | - |
| `soften_to_si` | Target saturation index for calcite | - |
| `acid_chemical` | Acid chemical for neutralization | - |
| `base_dosage` | Base chemical dosage | mmol/L |
| `acid_dosage` | Acid chemical dosage | mmol/L |
| `acid_position` | Acid dosing position ('reactor-outlet', 'bypass', 'after-bypass') | - |
| `bypass_open` | Bypass flow fraction | - |
| `nominal_capacity` | Reactor capacity | m³/h |
| `bypass_capacity` | Bypass capacity | m³/h |
| `fe_capture` | Iron capture efficiency | - |
| `mn_capture` | Manganese capture efficiency | - |

## Softening Process

### Flow Distribution

The model calculates flow distribution between reactor and bypass:

**Total Flow:**
$$ Q_{total} = Q_{reactor} + Q_{bypass} $$

**Bypass Fraction:**
$$ f_{bypass} = \frac{Q_{bypass}}{Q_{total}} $$

Where:
- $Q_{reactor} = \text{nominal\_capacity}$
- $Q_{bypass} = \text{bypass\_open} \times \text{bypass\_capacity}$

### Chemical Dosing

**Base Chemical Addition:**
$$ \text{Solution}_{dosed} = \text{Solution}_{influent} + \text{Base}_{chemical} \times \text{Base}_{dosage} $$

**Acid Chemical Addition:**
$$ \text{Solution}_{neutralized} = \text{Solution}_{input} + \text{Acid}_{chemical} \times \text{Acid}_{dosage} $$

### Precipitation Reactions

**Iron Capture:**
$$ \text{Fe}^{2+} + \text{CO}_3^{2-} \rightarrow \text{FeCO}_3 \downarrow $$

**Manganese Capture:**
$$ \text{Mn}^{2+} + \text{CO}_3^{2-} \rightarrow \text{MnCO}_3 \downarrow $$

**Calcite Precipitation:**
$$ \text{Ca}^{2+} + \text{CO}_3^{2-} \rightarrow \text{CaCO}_3 \downarrow $$

### Softening Process Steps

The softening process follows these sequential steps:

1. **Influent** - Raw water input
2. **Dosing** - Base chemical addition
3. **Precipitation** - Iron and manganese capture
4. **Softening** - Calcite precipitation to target SI
5. **Mixing** - Combination of softened and bypass flows
6. **Neutralization** - Acid addition for pH adjustment
7. **Effluent** - Final treated water

## Acid Dosing Positions

### Reactor Outlet
Acid is added to the softened water before mixing:

$$ \text{Solution}_{neutralized} = \text{Solution}_{softened} + \text{Acid}_{dose} $$

### Bypass
Acid is added to the bypass flow:

$$ \text{Solution}_{neutralized} = \text{Solution}_{bypass} + \text{Acid}_{dose} $$

### After Bypass
Acid is added to the mixed flow:

$$ \text{Solution}_{neutralized} = \text{Solution}_{mixed} + \text{Acid}_{dose} $$

## Flow Mixing

The final effluent is a mixture of softened and bypass flows:

$$ \text{Solution}_{mixed} = \text{Solution}_{softened} \times (1 - f_{bypass}) + \text{Solution}_{bypass} \times f_{bypass} $$

## Porosity Calculation

The model calculates pellet bed porosity using the Richardson-Zaki equation:

$$ \text{Porosity} = f(v, d_p, \rho_p, \rho_w, \mu) $$

**Optimization Equation:**
$$ \min_{x} \left| 130 \cdot \frac{v^{1.2}}{g} \cdot \frac{\mu^{0.8}}{d_p^{1.8}} \cdot \frac{\rho_w}{\rho_p - \rho_w} - \frac{x^3}{(1-x)^{0.8}} \right| $$

Where:
- $v$ = velocity (m/s)
- $d_p$ = pellet diameter (m)
- $\rho_p$ = pellet density (kg/m³)
- $\rho_w$ = water density (1000 kg/m³)
- $\mu$ = dynamic viscosity (1.3e-6 m²/s)
- $g$ = gravity constant (9.81 m/s²)

## Design Calculations

### Water Quality Parameters

The model tracks the following parameters through each process step:

- **pH** - Acidity/alkalinity
- **HCO₃⁻** - Bicarbonate concentration (mg/L)
- **CO₂** - Carbon dioxide concentration (mg/L)
- **Ca** - Calcium concentration (mg/L)
- **Mg** - Magnesium concentration (mg/L)
- **Hardness** - Total hardness (mg/L as CaCO₃)
- **CCPP90** - Calcium carbonate precipitation potential at pH 9.0
- **SI** - Saturation index for calcite
- **SC** - Specific conductance (mS/cm)

### Process Steps

The model provides detailed analysis for each process step:

1. **Influent** - Raw water quality
2. **Dosed** - After base chemical addition
3. **Softened** - After calcite precipitation
4. **Mixed** - After flow mixing
5. **Neutralized** - After acid addition
6. **Effluent** - Final water quality

### Dosage Charts

The model generates performance charts showing the relationship between chemical dosage and water quality:

**Chart Generation:**
- **Dosage Range**: 0 to 4 mmol/L in 40 steps
- **Chemicals**: NaOH and Ca(OH)₂
- **Parameters**: pH, hardness, HCO₃⁻, specific conductance

**Chart Types:**
- **Dosed pH** - pH after chemical addition
- **Softened pH** - pH after precipitation
- **Softened Hardness** - Hardness after precipitation
- **Softened HCO₃⁻** - Bicarbonate after precipitation
- **Softened SC** - Specific conductance after precipitation

## Mass Balance

The model provides mass balance information:

**Influent Masses:**
- Na: 123 mg/L
- Ca: 100 mg/L
- Mg: 20 mg/L

**Effluent Masses:**
- Na: 120 mg/L
- Ca: 100 mg/L
- Mg: 20 mg/L

## Integration with Solver

The softening model integrates with the overall solver framework by:

1. **Mass Balance** - Calculates flow distribution and mixing
2. **Quality Calculation** - Processes chemical reactions and precipitation
3. **Design Parameters** - Calculates reactor dimensions and chemical requirements
4. **Chemical Consumption** - Tracks chemical usage for cost calculations
5. **Precipitation Analysis** - Monitors scaling potential and precipitation efficiency
