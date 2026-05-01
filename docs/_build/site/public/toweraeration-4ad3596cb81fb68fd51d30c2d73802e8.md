# Tower Aeration Model

## Overview

The tower aeration model simulates packed tower aeration systems used for gas transfer processes in water treatment. It performs detailed calculations for gas transfer efficiency, pressure drop, flooding characteristics, and removal rates for various compounds including CO₂, CH₄, O₂, and volatile organic compounds (VOCs).

![Toweraeration](../images/modelimages/Toweraeration.png)

## Model Components

The tower aeration model inherits from both the base `Model` class and the `Balance` class, enabling it to handle mass balance calculations and complex gas transfer processes.

## Key Parameters

| Parameter | Description | Units |
| --- | --- | --- |
| `rq` | Air-to-water ratio | - |
| `diameter` | Tower diameter | m |
| `packingmaterial` | Type of packing material | - |
| `bed_height` | Packing bed height | m |
| `minimal_capacity` | Minimum design capacity | m³/h |
| `nominal_capacity` | Nominal design capacity | m³/h |
| `maximal_capacity` | Maximum design capacity | m³/h |
| `ambient_temperature` | Ambient air temperature | °C |
| `model_component` | Target component for design ('CO2', 'Mtg', 'Oxg') | - |

## Gas Transfer Calculations

### Henry's Law and Stripping Factor

The model calculates gas transfer using Henry's Law and stripping factor:

**Henry's Constant:**
$$ H_c = \frac{C_{gas}}{C_{liquid}} $$

**Stripping Factor:**
$$ S_f = H_c \times RQ $$

**Concentration Change:**
$$ z = \exp\left(\frac{\text{bed\_height} \times (S_f - 1)}{HTU_{ov} \times S_f}\right) $$

**Outlet Concentration:**
$$ C_{out} = \frac{S_f \times C_{out,eq} \times z - S_f \times C_{out,eq} + S_f \times C_{in} - C_{in}}{S_f \times z - 1} $$

**Transfer Efficiency:**
$$ \eta = \frac{C_{in} - C_{out}}{C_{in}} $$

Where:
- $H_c$ = Henry's constant (dimensionless)
- $RQ$ = air-to-water ratio
- $HTU_{ov}$ = overall height of transfer unit
- $C_{out,eq}$ = equilibrium concentration

### Number of Transfer Units (NTU)

$$ NTU_{ov} = \frac{S_f}{S_f - 1} \times \ln\left(\frac{(C_{in} - C_{gas}/H_c) \times (S_f - 1)}{(C_{out} - C_{gas}/H_c) \times S_f} + \frac{1}{S_f}\right) $$

## Component-Specific Calculations

### Carbon Dioxide (CO₂)

**Gas Concentration:**
$$ C_{gas} = \frac{0.82}{16 \times 1000} \text{ mol/m³} $$

**Influent Concentration:**
$$ C_{in} = C_{CO_2,influent} \text{ (mmol/L)} $$

### Methane (CH₄)

**Gas Concentration:**
$$ C_{gas} = 0 \text{ mol/m³} $$

**Influent Concentration:**
$$ C_{in} = C_{CH_4,influent} \text{ (mmol/L)} $$

### Oxygen (O₂)

**Gas Concentration:**
$$ C_{gas} = \frac{0.208 \times 101325}{8.31446 \times (273.15 + T_{gas})} \text{ mol/m³} $$

**Influent Concentration:**
$$ C_{in} = C_{O_2,influent} \text{ (mmol/L)} $$

### Volatile Organic Compounds (VOCs)

**Gas Concentration:**
$$ C_{gas} = 0 \text{ mol/m³} $$

**Influent Concentration:**
$$ C_{in} = C_{VOC,influent} \text{ (mg/L)} $$

## Tower Operation Analysis

### Operating Point Calculation

The model calculates the operating point using Engel-Stichlmair correlations:

**Operating Parameters:**
- **Pressure drop**: $dp_{tot}$ (Pa)
- **Liquid holdup**: $h_{tot}$ (m)
- **Flooding factor**: $F$ (dimensionless)
- **Flooding factor percentage**: $F \times 100\%$

### Flooding Analysis

**Flooding Detection:**
The model detects flooding conditions when:
- Pressure drop becomes complex
- Liquid holdup becomes complex
- Operating point calculation fails

**Flooding Factor:**
$$ F = \frac{\text{Actual loading}}{\text{Flooding loading}} $$

### Capacity Calculations

**Liquid Capacity:**
$$ C_{liq} = u_l \times \sqrt{\frac{\rho_l}{\rho_l - \rho_g}} $$

**Gas Capacity:**
$$ C_{gas} = u_g \times \sqrt{\frac{\rho_g}{\rho_l - \rho_g}} $$

Where:
- $u_l$ = liquid velocity (m/s)
- $u_g$ = gas velocity (m/s)
- $\rho_l$ = liquid density (kg/m³)
- $\rho_g$ = gas density (kg/m³)

## Blower Power Calculation

The model calculates blower power requirements:

$$ P = \frac{Q_{air} \times \rho_{air} \times R \times T \times \frac{\kappa}{\kappa-1} \times \left(\left(\frac{P_{out}}{P_{in}}\right)^{\frac{\kappa-1}{\kappa}} - 1\right)}{\eta \times M_{air} \times 3600000} $$

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

The model generates comprehensive performance charts:

**Flooding Charts:**
- **Flooding line**: Maximum capacity before flooding
- **Operating line**: Recommended operating capacity (65% of flooding)
- **Working point**: Current operating conditions

**Efficiency Charts:**
- **Efficiency vs. RQ**: Removal efficiency vs. air-to-water ratio
- **Efficiency vs. Height**: Removal efficiency vs. bed height
- **VOC Concentration**: VOC concentration vs. RQ

### Water Quality Parameters

**Influent Parameters:**
- **pH** - Acidity/alkalinity
- **O₂** - Dissolved oxygen (mg/L)
- **CO₂** - Carbon dioxide (mg/L)
- **CH₄** - Methane (mg/L)

**Effluent Parameters:**
- **pH** - Acidity/alkalinity
- **O₂** - Dissolved oxygen (mg/L)
- **CO₂** - Carbon dioxide (mg/L)
- **CH₄** - Methane (mg/L)

### Model Parameters

**Operating Parameters:**
- **F** - Flooding factor
- **Liquid load** - Liquid loading rate (m³/m²/h)
- **Flooding factor** - Flooding factor percentage
- **Liquid holdup** - Liquid holdup percentage
- **Pressure drop** - Pressure drop (mbar)

## Unit Conversion

The model handles unit conversions for VOC concentrations:

**Unit Conversions:**
- **ng/L to mg/L**: Divide by 1,000,000
- **μg/L to mg/L**: Divide by 1,000
- **mg/L**: No conversion needed

## Context Properties

The model provides additional context for design calculations:

| Property | Description | Units |
| --- | --- | --- |
| `blower_power` | Blower power calculation function | - |
| `deltaPtotal` | Total pressure drop | Pa |
| `Air_density` | Air density at operating conditions | kg/m³ |
| `packing` | Packing material properties | - |
| `engel_stickl` | Engel-Stichlmair correlation object | - |
| `operationpoint` | Operating point calculation function | - |

## Integration with Solver

The tower aeration model integrates with the overall solver framework by:

1. **Mass Balance** - Calculates water flows through the tower
2. **Quality Calculation** - Processes gas transfer reactions
3. **Design Parameters** - Calculates tower dimensions and performance
4. **Energy Calculation** - Determines blower power requirements
5. **Performance Analysis** - Generates efficiency curves and design charts


