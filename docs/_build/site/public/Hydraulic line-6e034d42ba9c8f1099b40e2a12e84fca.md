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

The hydraulic solver uses a two-phase iterative approach to determine the optimal hydraulic head distribution throughout the treatment system. This process ensures that all models receive adequate pressure while minimizing energy consumption.

### Solver Algorithm Overview

The solver operates through two main phases:

1. **Backward Traversal** - Determines minimum required heads
2. **Forward Traversal** - Calculates actual operating heads and booster requirements

The algorithm iterates twice to ensure convergence and accurate head calculations for all pressurized systems.

### Step 1: Backward Traversal

The solver starts from leaf nodes (final treatment units) and works backward to source nodes, determining the minimum required hydraulic heads:

**Node Classification:**
- **Leaf Nodes** - Models with no downstream connections (typically output models)
- **Source Nodes** - Models with no upstream connections (typically groundwater wells)

**Non-Pressurized Models:**
$$ H_{in} = Z_{in} + \Delta H_{inlet} $$

$$ H_{out} = H_{in} - \Delta H_{total} $$

**Pressurized Models:**
$$ H_{out} = \max(H_{out,required}, H_{out,current}) $$

$$ H_{in} = H_{out} + \Delta H_{total} $$

**Backward Traversal Process:**

1. **Identify downstream requirements** - For pressurized models, determine the maximum head required by downstream models
2. **Calculate outlet head** - Set outlet head to meet downstream requirements
3. **Calculate inlet head** - Determine inlet head based on outlet head and total headloss
4. **Handle integrated boosters** - For models with integrated boosters, ensure minimum head requirements are met
5. **Propagate upstream** - Continue backward to upstream models

**Key Equations:**
- **Downstream head requirement**: $H_{out,required} = \max(H_{in,downstream})$
- **Inlet head calculation**: $H_{in} = \max(H_{out} + \Delta H_{total}, H_{minimal}, H_{out,upstream})$

### Step 2: Forward Traversal

The solver moves from source nodes (well pumps) forward through the treatment chain, calculating actual operating heads and determining booster pump requirements:

**Forward Traversal Process:**

1. **Start from source nodes** - Begin with groundwater wells or other source models
2. **Propagate head values** - Move head values from upstream to downstream models
3. **Calculate booster requirements** - Determine where booster pumps are needed
4. **Update efficiency calculations** - Calculate weighted average pump efficiencies
5. **Handle integrated boosters** - Calculate booster head for models with integrated pumps

**Head Propagation:**
$$ H_{in} = \max(H_{out,upstream}) $$

**Booster Pump Calculation:**
$$ H_{booster} = H_{in,downstream} - H_{out,upstream} $$

**Integrated Booster Systems:**
$$ H_{booster,integrated} = H_{out} - H_{in} + \Delta H_{total} $$

### Iterative Convergence

The solver performs two complete iterations to ensure accurate head calculations:

**First Iteration:**
- Establishes initial head values
- Identifies basic booster requirements
- Calculates preliminary efficiency values

**Second Iteration:**
- Refines head calculations based on upstream/downstream dependencies
- Confirms booster pump requirements
- Finalizes efficiency calculations

**Convergence Criteria:**
- All pressurized models have consistent head values
- Booster pump requirements are stable
- Efficiency calculations are accurate

### Solver Logic Flow

```
1. Initialize all models with default head values
2. Classify models as pressurized or non-pressurized
3. Perform backward traversal (2 iterations):
   a. Start from leaf nodes
   b. Calculate minimum required heads
   c. Propagate requirements upstream
4. Perform forward traversal:
   a. Start from source nodes
   b. Propagate actual head values
   c. Calculate booster requirements
   d. Update efficiency calculations
5. Generate system summary
```

### Error Handling

**Negative Booster Head:**
- If calculated booster head is negative, set to zero
- Log warning message for debugging
- Adjust outlet head to maintain hydraulic balance

**Missing Efficiency Values:**
- Wait for upstream connections to have assigned efficiency values
- Use default efficiency values when necessary
- Calculate weighted averages for multiple upstream connections

Where:
- $H_{in}$ = inlet hydraulic head (m)
- $H_{out}$ = outlet hydraulic head (m)
- $Z_{in}$ = inlet elevation (m)
- $\Delta H_{inlet}$ = inlet headloss (m)
- $\Delta H_{total}$ = total model headloss (m)

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




