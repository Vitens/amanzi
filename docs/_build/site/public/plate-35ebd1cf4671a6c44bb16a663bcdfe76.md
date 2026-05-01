# Plate Model

## Overview

The plate model simulates plate aeration systems used for gas transfer processes in water treatment. It performs gas exchange between water and air through plate contactors, with optional recirculation of off-gas to improve efficiency and reduce fresh air requirements.

## Model Components

The plate model inherits from both the base `Model` class and the `Balance` class, enabling it to handle mass balance calculations and gas transfer processes.

## Key Parameters

| Parameter | Description | Units |
| --- | --- | --- |
| `RQ` | Air-to-water ratio | - |
| `recirculation` | Gas recirculation ratio | - |
| `efficiency` | Plate aeration efficiency | - |

## Air Composition

The model uses standard atmospheric air composition:

| Component | Fraction | Description |
| --- | --- | --- |
| `O2(g)` | 0.208 | Oxygen (20.8%) |
| `Ntg(g)` | 0.7916 | Nitrogen (79.16%) |
| `CO2(g)` | 0.0004 | Carbon dioxide (0.04%) |
| `Mtg(g)` | 0 | Methane (0%) |
| `H2Sg(g)` | 0 | Hydrogen sulfide (0%) |
| `H2O(g)` | 0 | Water vapor (0%) |

## Aeration Process

### Gas Transfer Calculation

The aeration process follows these steps:

1. **Air Processing** - Create air gas phase with specified composition
2. **Gas-Water Interaction** - Perform gas transfer between air and water
3. **Off-Gas Calculation** - Determine gas composition after interaction
4. **Recirculation** - Mix fresh air with recirculated off-gas
5. **Iteration** - Repeat process for multiple passes

### Recirculation Logic

**Fresh Gas Volume:**
$$ V_{fresh} = RQ - V_{off} \cdot \eta_{recirculation} $$

**Fresh Gas Fraction:**
$$ f_{fresh} = \frac{V_{fresh}}{RQ} $$

**Off-Gas Fraction:**
$$ f_{off} = 1 - f_{fresh} $$

**Mixed Gas Composition:**
$$ C_{mixed} = C_{fresh} \cdot f_{fresh} + C_{off} \cdot f_{off} $$

Where:
- $RQ$ = air-to-water ratio
- $V_{off}$ = off-gas volume
- $\eta_{recirculation}$ = recirculation ratio
- $C_{fresh}$ = fresh air composition
- $C_{off}$ = off-gas composition

### Iteration Control

The model performs multiple iterations based on recirculation:

- **No recirculation** ($\eta_{recirculation} = 0$): 1 iteration
- **With recirculation** ($\eta_{recirculation} > 0$): 3 iterations

## Blower Power Calculation

The model calculates blower power requirements using the following equation:

$$ P = \frac{Q_{air} \cdot \rho_{air} \cdot R \cdot T \cdot \frac{\kappa}{\kappa-1} \cdot \left(\left(\frac{P_{out}}{P_{in}}\right)^{\frac{\kappa-1}{\kappa}} - 1\right)}{\eta \cdot M_{air} \cdot 3600000} $$

Where:
- $P$ = blower power (kWh)
- $Q_{air}$ = air flow rate (m³/s)
- $\rho_{air}$ = air density (kg/m³)
- $R$ = gas constant (8.31446 J/(mol·K))
- $T$ = air temperature (K)
- $\kappa$ = specific heat ratio (1.4)
- $P_{out}$ = outlet pressure (Pa)
- $P_{in}$ = inlet pressure (101325 Pa)
- $\eta$ = blower efficiency
- $M_{air}$ = molecular weight of air (28.97e-3 kg/mol)

## Design Calculations

### Performance Charts

The model generates performance charts showing the relationship between air-to-water ratio (RQ) and water quality parameters:

**Chart Generation Process:**
1. **RQ Range**: 1 to 50 in 100 steps
2. **Parameter Calculation**: Calculate water quality for each RQ value
3. **Chart Data**: Generate x-y data points for visualization

### Water Quality Parameters

The model tracks the following water quality parameters:

**Influent Parameters:**
- **pH** - Acidity/alkalinity
- **CH₄** - Methane concentration (mg/L)
- **N₂** - Nitrogen concentration (mg/L)
- **CO₂** - Carbon dioxide concentration (mg/L)
- **H₂S** - Hydrogen sulfide concentration (mg/L)
- **O₂** - Oxygen concentration (mg/L)

**Effluent Parameters:**
- Same parameters as influent, calculated after aeration

### Gas Phase Analysis

The model provides detailed gas phase analysis:

**Gas Composition (Dry Basis):**
- **CH₄** - Methane percentage
- **N₂** - Nitrogen percentage
- **CO₂** - Carbon dioxide percentage
- **O₂** - Oxygen percentage
- **H₂S** - Hydrogen sulfide percentage

**Gas Volume:**
$$ V_{gas} = \frac{V_{actual}}{\eta_{efficiency}} $$

Where:
- $V_{gas}$ = total gas volume
- $V_{actual}$ = actual gas volume
- $\eta_{efficiency}$ = plate efficiency

## Context Properties

The model provides additional context for design calculations:

| Property | Description | Units |
| --- | --- | --- |
| `blower_power` | Blower power calculation function | - |
| `Air_density` | Air density at operating conditions | kg/m³ |
| `deltaPtotal` | Total pressure drop | Pa |

## Air Properties

The model calculates air properties at operating conditions:

**Air Density:**
$$ \rho_{air} = \frac{P \cdot M_{air}}{R \cdot T} $$

Where:
- $P$ = air pressure (1.023e5 Pa)
- $M_{air}$ = molecular weight of air
- $R$ = gas constant
- $T$ = air temperature (20°C)

## Integration with Solver

The plate model integrates with the overall solver framework by:

1. **Mass Balance** - Calculates water flows through the plate system
2. **Quality Calculation** - Processes gas transfer reactions
3. **Design Parameters** - Calculates plate dimensions and performance
4. **Energy Calculation** - Determines blower power requirements
5. **Performance Analysis** - Generates efficiency curves and design charts

## Applications

Plate aeration is commonly used for:
- **Groundwater treatment** - Removal of CO₂ and CH₄
- **Oxygen addition** - Increasing dissolved oxygen levels
- **Gas stripping** - Removal of volatile organic compounds
- **pH adjustment** - CO₂ removal increases pH
- **Pre-treatment** - Preparation for downstream processes
- **Recirculation systems** - Efficient gas transfer with reduced air consumption
