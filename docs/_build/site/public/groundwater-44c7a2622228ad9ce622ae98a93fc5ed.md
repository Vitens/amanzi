# Groundwater Model

## Overview

The groundwater model simulates groundwater sources and their water quality characteristics. It serves as an emitter model that provides raw groundwater with specified chemical composition and flow rates to downstream treatment processes.

![Abstraction](../images/modelimages/Abstraction_overview.png)

## Model Components

The groundwater model inherits from the base `Model` class and functions as an emitter, providing a constant flow of groundwater with defined water quality parameters.

## Key Parameters

| Parameter | Description | Units |
| --- | --- | --- |
| `yearly_production` | Annual groundwater production | m³/year |
| `pH` | Groundwater pH | - |
| `temperature` | Groundwater temperature | °C |
| `oxygen` | Dissolved oxygen concentration | mg/L |
| `nitrogen` | Nitrogen concentration | mg/L |
| `methane` | Methane concentration | mg/L |
| `hydrogen-sulfide` | Hydrogen sulfide concentration | mg/L |
| `iron` | Iron concentration | mg/L |
| `manganese` | Manganese concentration | mg/L |
| `ammonium` | Ammonium concentration | mg/L |
| `calcium` | Calcium concentration | mg/L |
| `magnesium` | Magnesium concentration | mg/L |
| `sodium` | Sodium concentration | mg/L |
| `potassium` | Potassium concentration | mg/L |
| `bicarbonate` | Bicarbonate concentration | mg/L |
| `chloride` | Chloride concentration | mg/L |
| `nitrate` | Nitrate concentration | mg/L |
| `nitrite` | Nitrite concentration | mg/L |
| `sulfate` | Sulfate concentration | mg/L |
| `phosphate` | Phosphate concentration | mg/L |
| `silica` | Silica concentration | mg/L |
| `boron` | Boron concentration | mg/L |
| `strontium` | Strontium concentration | mg/L |
| `barium` | Barium concentration | mg/L |
| `fluoride` | Fluoride concentration | mg/L |
| `color` | Water color | - |
| `total-organic-carbon` | Total organic carbon | mg/L |

## Water Quality Configuration

### Redox State Determination

The model determines the redox state of the groundwater based on oxygen concentration:

**Aerobic Conditions** (O₂ > 0):
- Hydrogen sulfide: `S(-2)` (sulfate)
- Iron: `Fe` (ferric iron)
- Manganese: `Mn` (manganic manganese)
- Ammonium: `N(-3)` (ammonium)

**Anaerobic Conditions** (O₂ = 0):
- Hydrogen sulfide: `Sg` (sulfide)
- Iron: `[Fe+2]` (ferrous iron)
- Manganese: `[Mn+2]` (manganous manganese)
- Ammonium: `[N-3]` (ammonium)

### PHREEQC Solution Creation

The model creates a PHREEQC solution with the following structure:

```python
solution_parameters = {
    'pH': pH_value,
    'temp': temperature,
    'units': 'mg/l',
    'pe': 4,  # PHREEQC default
    'redox': 'O(-2)/O(0)',
    'O(0)': oxygen_concentration,
    'Oxg': 0.0000001,  # Prevent PHREEQC crashes
    # ... other chemical species
}
```

## Extraneous Properties

The model supports additional water quality parameters not tracked by PHREEQC:

### PFAS (Per- and Polyfluoroalkyl Substances)
- Custom PFAS compounds can be added
- Concentrations specified in configuration
- Zero concentrations are automatically removed

### VOC (Volatile Organic Compounds)
- Custom VOC compounds can be added
- Concentrations specified in configuration
- Zero concentrations are automatically removed

### Other Parameters
- Custom parameters for specific applications
- Flexible configuration system

## Flow Calculations

### Production Rate

The model calculates the production rate considering minor losses:

**Percentage-based losses:**
$$ Q_{production} = Q_{yearly} \cdot \eta_{minor} $$

**Fixed losses:**
$$ Q_{production} = Q_{yearly} - Q_{loss} $$

Where:
- $Q_{production}$ = actual production rate
- $Q_{yearly}$ = yearly production
- $\eta_{minor}$ = minor loss percentage
- $Q_{loss}$ = fixed loss amount

### Mass Balance Equations

The model provides mass balance equations for the solver:

$$ \text{Eq}_1: \text{Product flow} = 1 \text{ (normalized)} $$
$$ \text{Constant}: Q_{production} \text{ (actual flow rate)} $$

## Design Calculations

### Water Quality Parameters

The model calculates comprehensive water quality parameters:

**Physical Parameters:**
- **SC20** - Specific conductance at 20°C (μS/cm)
- **TDS** - Total dissolved solids (mg/L)
- **Osmotic pressure** - Osmotic pressure (bar)

**Chemical Parameters:**
- **pH** - Acidity/alkalinity
- **pe** - Redox potential
- **Hardness** - Total hardness (mg/L as CaCO₃)
- **SI** - Saturation index for calcite
- **CCPP** - Calcium carbonate precipitation potential
- **CCPP90** - CCPP at pH 9.0

**Ionic Balance:**
- **Cations** - Total cationic charge (meq/L)
- **Anions** - Total anionic charge (meq/L)
- **Charge balance** - Charge balance error
- **Balance error** - Mass balance error

### Oxygen Consumption Calculations

The model calculates oxygen consumption for treatment planning:

**Ionic oxygen consumption:**
$$ O_{2,ions} = C_{Fe^{2+}} \cdot 0.25 + C_{Mn^{2+}} \cdot 0.5 + C_{NH_4^+} \cdot 2 $$

**Gaseous oxygen consumption:**
$$ O_{2,gas} = C_{CH_4} \cdot 2 + C_{H_2S} \cdot 2 $$

**Total oxygen consumption:**
$$ O_{2,total} = (O_{2,ions} + O_{2,gas}) \cdot 32 \text{ mg/L} $$

### Carbonate System

The model calculates carbonate system parameters:

- **CO₂** - Carbon dioxide concentration (mg/L)
- **HCO₃⁻** - Bicarbonate concentration (mg/L)
- **CO₃²⁻** - Carbonate concentration (mg/L)

## Solution Equalization

The model performs solution equalization to ensure mass balance:

$$ \text{Solution.equalize('Calcite', 1000, 0)} $$

This ensures that all mass balances are properly solved and the solution is chemically consistent.

## Integration with Solver

The groundwater model integrates with the overall solver framework by:

1. **Emitter Function** - Provides constant flow of groundwater
2. **Mass Balance** - Establishes flow rates for downstream models
3. **Quality Calculation** - Provides water quality baseline
4. **Design Parameters** - Calculates treatment requirements
5. **Oxygen Demand** - Determines aeration needs


