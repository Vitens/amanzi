# Spray Aerator Model

## Overview

The spray aerator model simulates spray aeration systems used for gas transfer processes in water treatment. It performs gas exchange between water and air through spray nozzles, removing dissolved gases like CO₂ and CH₄ while providing oxygen transfer capabilities.

## Model Components

The spray aerator model inherits from both the base `Model` class and the `Balance` class, enabling it to handle mass balance calculations and gas transfer processes.

## Key Parameters

| Parameter | Description | Units |
| --- | --- | --- |
| `fall_height` | Height of water fall | m |
| `rq` | Air-to-water ratio | - |
| `ambient_temperature` | Ambient air temperature | °C |
| `model_component` | Target component for design ('CO2', 'Mtg', 'Oxg') | - |

## Gas Transfer Calculations

### Sauter Diameter

The model uses the Sauter diameter to characterize droplet size:

$$ d_{sauter} = 0.00025 \text{ m} $$

**Droplet Geometry:**
- **Surface area**: $A = \frac{\pi \times d_{sauter}^2}{4}$
- **Volume**: $V = \frac{\pi \times d_{sauter}^3}{6}$

### Exposure Time

The exposure time is calculated based on free fall:

$$ t = \sqrt{\frac{2 \times h}{g}} $$

Where:
- $t$ = exposure time (s)
- $h$ = fall height (m)
- $g$ = gravitational acceleration (9.81 m/s²)

### Diffusion Coefficient

The model calculates the diffusion coefficient for each compound:

$$ D_{comp} = f(T_{water}, T_{air}, \text{compound}) $$

Where:
- $D_{comp}$ = diffusion coefficient (m²/s)
- $T_{water}$ = water temperature (°C)
- $T_{air}$ = air temperature (°C)

### Gas Transfer Coefficient

The gas transfer coefficient is calculated using:

$$ k_2 = 2 \times \frac{A}{V} \times \sqrt{\frac{D_{comp} \times t}{\pi}} $$

Where:
- $k_2$ = gas transfer coefficient (s⁻¹)
- $A$ = droplet surface area (m²)
- $V$ = droplet volume (m³)
- $D_{comp}$ = diffusion coefficient (m²/s)
- $t$ = exposure time (s)

### Transfer Efficiency

The transfer efficiency is calculated using:

$$ \eta = 1 - \exp(-k_2) $$

Where:
- $\eta$ = transfer efficiency (dimensionless)
- $k_2$ = gas transfer coefficient (s⁻¹)

## Component-Specific Calculations

### Carbon Dioxide (CO₂)

**Transfer Process:**
$$ \text{CO}_2 + \text{H}_2\text{O} \leftrightarrow \text{H}_2\text{CO}_3 $$

**Efficiency Calculation:**
$$ \eta_{CO_2} = f(\text{RQ}, h, d_{sauter}) $$

### Methane (CH₄)

**Transfer Process:**
$$ \text{CH}_4 \rightarrow \text{CH}_4(\text{g}) $$

**Efficiency Calculation:**
$$ \eta_{CH_4} = f(\text{RQ}, h, d_{sauter}) $$

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

**Height Charts:**
- **Range**: 0.01 to 4 m in 50 steps
- **Parameter**: Transfer efficiency vs. fall height
- **Formula**: $\eta = f(h, \text{RQ}, d_{sauter})$

**Sauter Diameter Charts:**
- **Range**: 0.000001 to 0.001 m in 500 steps
- **Heights**: 0.5, 1, 1.5, 2 m
- **Parameter**: Transfer efficiency vs. droplet size
- **Formula**: $\eta = f(d_{sauter}, h, \text{RQ})$

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

## Context Properties

The model provides additional context for design calculations:

| Property | Description | Units |
| --- | --- | --- |
| `blower_power` | Blower power calculation function | - |
| `Air_density` | Air density at operating conditions | kg/m³ |

## Design Optimization

### Fall Height Optimization

The transfer efficiency increases with fall height:

$$ \frac{\partial \eta}{\partial h} > 0 $$

**Optimal Height:**
- **Minimum**: 0.5 m for basic aeration
- **Optimal**: 1.5-2.0 m for good efficiency
- **Maximum**: 4.0 m for maximum efficiency

### Droplet Size Optimization

The transfer efficiency depends on droplet size:

$$ \eta = f(d_{sauter}) $$

**Optimal Droplet Size:**
- **Small droplets**: High surface area, short exposure time
- **Large droplets**: Low surface area, long exposure time
- **Optimal size**: Balance between surface area and exposure time

## Integration with Solver

The spray aerator model integrates with the overall solver framework by:

1. **Mass Balance** - Calculates water flows through the spray system
2. **Quality Calculation** - Processes gas transfer reactions
3. **Design Parameters** - Calculates spray system dimensions and performance
4. **Energy Calculation** - Determines blower power requirements
5. **Performance Analysis** - Generates efficiency curves and design charts

## Applications

Spray aeration is commonly used for:

- **CO₂ removal** - Reduction of carbon dioxide
- **Methane stripping** - Removal of methane
- **Oxygen addition** - Increasing dissolved oxygen
- **pH adjustment** - CO₂ removal increases pH
- **Pre-treatment** - Preparation for downstream processes
- **Groundwater treatment** - Removal of dissolved gases
- **Water conditioning** - Improvement of water quality

## Advantages

- **Simple design** - Minimal equipment required
- **Low maintenance** - Few moving parts
- **Energy efficient** - Gravity-driven operation
- **Flexible operation** - Adjustable fall height
- **Cost effective** - Low capital and operating costs
- **Easy installation** - Simple construction
