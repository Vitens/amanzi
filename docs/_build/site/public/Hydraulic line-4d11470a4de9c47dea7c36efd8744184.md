# Hydraulic Line

## Overview

The hydraulic line feature provides a comprehensive visualization and analysis of the hydraulic system in water treatment scenarios. It displays the height mapping of each treatment unit, pressure requirements, and automatically calculates booster pump requirements based on hydraulic head requirements throughout the treatment process.

## Hydraulic System Components

### Model Classification

The hydraulic solver classifies treatment models into two main categories:

**Pressurized Models:**
- **Reverse Osmosis (RO)** - Requires high operating pressure
- **Nanofiltration (NF)** - Requires moderate operating pressure  
- **Membrane Degassing** - Requires vacuum pressure
- **Integrated Booster Systems** - Models with built-in pumps

**Non-Pressurized Models:**
- **Cascades** - Gravity-driven flow
- **Sand Filters** - Open gravity systems
- **Tower Aerators** - Atmospheric pressure operation
- **Vacuum Systems** - Sub-atmospheric pressure
- **Reservoirs** - Storage with atmospheric pressure

### Hydraulic Parameters

| Parameter | Description | Units |
| --- | --- | --- |
| `pressurized` | Whether the model operates under pressure | bool |
| `integrated_booster` | Whether the model has a built-in booster pump | bool |
| `inlet_elevation` | Height of the model inlet | m |
| `outlet_elevation` | Height of the model outlet | m |
| `minimal_head` | Minimum required hydraulic head | m |
| `total_headloss` | Total headloss through the model | m |

## Hydraulic Calculation Process

### Step 1: Backward Traversal

The solver starts from leaf nodes (final treatment units) and works backward to source nodes:

**Non-Pressurized Models:**
$$ H_{in} = Z_{in} + \Delta H_{inlet} $$

$$ H_{out} = H_{in} - \Delta H_{total} $$

**Pressurized Models:**
$$ H_{out} = \max(H_{out,required}, H_{out,current}) $$

$$ H_{in} = H_{out} + \Delta H_{total} $$

Where:
- $H_{in}$ = inlet hydraulic head (m)
- $H_{out}$ = outlet hydraulic head (m)
- $Z_{in}$ = inlet elevation (m)
- $\Delta H_{inlet}$ = inlet headloss (m)
- $\Delta H_{total}$ = total model headloss (m)

### Step 2: Forward Traversal

The solver moves from source nodes (well pumps) forward through the treatment chain:

**Head Propagation:**
$$ H_{in} = \max(H_{out,upstream}) $$

**Booster Pump Calculation:**
$$ H_{booster} = H_{in,downstream} - H_{out,upstream} $$

**Integrated Booster Systems:**
$$ H_{booster,integrated} = H_{out} - H_{in} + \Delta H_{total} $$

## Booster Pump Requirements

### Connection Boosters

When the outlet head of an upstream model is insufficient for the downstream model:

**Booster Head:**
$$ H_{booster} = H_{in,downstream} - H_{out,upstream} $$

**Booster Efficiency:**
$$ \eta_{connection} = \eta_{booster} $$

**Combined Efficiency:**
$$ \eta_{combined} = \frac{1}{\frac{H_{out}}{\eta_{upstream} \times H_{out}} + \frac{H_{booster}}{\eta_{booster} \times H_{booster}}} $$

### Integrated Boosters

For models with built-in booster pumps:

**Booster Head Calculation:**
$$ H_{booster} = H_{out} - H_{in} + \Delta H_{total} $$

**Model Efficiency:**
$$ \eta_{model} = \frac{1}{\frac{H_{in}}{\eta_{upstream} \times H_{in}} + \frac{H_{booster}}{\eta_{booster} \times H_{booster}}} $$

**Recovery Correction:**
$$ \eta_{downstream} = \eta_{model} \times R $$

Where $R$ = recovery ratio

## Pressure Requirements

### Supply Pressure

**Distribution Requirements:**
- **Minimum inlet pressure** - Required for distribution system
- **Pressure zones** - Different pressure requirements for different areas
- **Peak demand** - Pressure requirements during high demand

### Operating Pressure

**Pressurized Systems:**
- **RO systems** - 10-50 bar operating pressure
- **NF systems** - 5-15 bar operating pressure
- **Membrane degassing** - 0.1-0.5 bar vacuum pressure

**Non-Pressurized Systems:**
- **Gravity systems** - Atmospheric pressure
- **Open systems** - Atmospheric pressure with elevation head

## Visual Representation

### Height Mapping

The hydraulic line displays:

**Model Positioning:**
- **Elevation levels** - Each model positioned at its elevation
- **Process dimensions** - Height changes through each unit
- **Flow direction** - Visual flow path through the system

**Pressure Indicators:**
- **Supply pressure** - Inlet pressure in water column height
- **Discharge pressure** - Outlet pressure in water column height
- **Operating pressure** - Required pressure for pressurized systems

### Interactive Features

**Model Adjustment:**
- **Drag and drop** - Move models up and down to change elevation
- **Automatic updates** - Parameter changes update design tables
- **Pressure recalculation** - Automatic booster pump placement

**Real-time Updates:**
- **Parameter synchronization** - Height changes update model parameters
- **Booster placement** - Automatic booster pump addition/removal
- **Efficiency calculation** - Updated pump efficiency calculations

## Pump Efficiency Calculations

### Weighted Average Efficiency

**Upstream Efficiency:**
$$ \eta_{upstream} = \frac{1}{\sum_{i} \frac{1}{\eta_i} \times Q_i} $$

**Downstream Efficiency:**
$$ \eta_{downstream} = \eta_{model} \times R $$

### Efficiency Parameters

| Parameter | Description | Units |
| --- | --- | --- |
| `well_efficiency` | Well pump efficiency (default: 55%) | % |
| `booster_efficiency` | Booster pump efficiency | % |
| `model_efficiency` | Treatment model efficiency | % |

## System Summary

### Hydraulic Metrics

**Total Boosters:**
$$ N_{boosters} = \sum_{connections} \text{booster\_required} $$

**Total Headloss:**
$$ H_{total,loss} = \sum_{connections} H_{loss} $$

**System Efficiency:**
$$ \eta_{system} = \frac{\sum_{models} \eta_{model} \times Q_{model}}{\sum_{models} Q_{model}} $$

## Applications

### Design Optimization

**Pressure Management:**
- **Optimal elevation** - Minimize booster pump requirements
- **Pressure zones** - Efficient pressure distribution
- **Energy optimization** - Minimize pumping energy

**System Integration:**
- **Model compatibility** - Ensure hydraulic compatibility
- **Flow control** - Maintain proper flow rates
- **Pressure control** - Maintain required pressures

### Operational Analysis

**Performance Monitoring:**
- **Pressure tracking** - Monitor system pressures
- **Efficiency analysis** - Track pump efficiency
- **Energy consumption** - Monitor pumping energy

**Maintenance Planning:**
- **Booster maintenance** - Schedule booster pump maintenance
- **Pressure testing** - Plan pressure system testing
- **System upgrades** - Identify system improvement opportunities 




