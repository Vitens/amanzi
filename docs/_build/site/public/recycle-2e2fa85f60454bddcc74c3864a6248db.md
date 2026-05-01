# Recycle Model

## Overview

The recycle model simulates recycling systems used in water treatment processes. It functions as a splitter that divides incoming flow into product and waste streams, with the ability to recycle a portion of the flow back into the system for further treatment.

## Model Components

The recycle model inherits from both the base `Model` class and the `Splitter` class, enabling it to handle flow splitting and recycling operations.

## Key Parameters

| Parameter | Description | Units |
| --- | --- | --- |
| `recycle_efficiency` | Fraction of flow recycled (default: 0.8) | - |

## Flow Splitting

### Split Ratio

The model divides the incoming flow based on the recycle efficiency:

$$ f_{recycle} = \text{recycle\_efficiency} $$

$$ f_{product} = 1 - f_{recycle} $$

Where:
- $f_{recycle}$ = fraction of flow recycled
- $f_{product}$ = fraction of flow sent to product

### Flow Distribution

**Product Flow:**
$$ Q_{product} = Q_{influent} \times f_{product} $$

**Recycled Flow:**
$$ Q_{recycled} = Q_{influent} \times f_{recycle} $$

**Waste Flow:**
$$ Q_{waste} = Q_{influent} \times f_{recycle} $$

## Water Quality Processing

### Solution Handling

The model processes water quality through the following steps:

1. **Solution Copying** - Creates copies of the influent solution
2. **Product Solution** - Assigns solution to product stream
3. **Waste Solution** - Assigns solution to waste stream
4. **Quality Preservation** - Maintains water quality characteristics

### Quality Parameters

The model preserves all water quality parameters:
- **pH** - Acidity/alkalinity
- **Dissolved gases** - O₂, CO₂, CH₄, N₂
- **Ionic species** - All major and minor ions
- **Extraneous properties** - PFAS, VOC, other parameters

## Mass Balance Considerations

### Mass Conservation

The recycle model ensures mass conservation by:

$$ \text{Mass}_{influent} = \text{Mass}_{product} + \text{Mass}_{waste} $$

### Convergence Requirements

The model sets mass to zero to ensure convergence:

$$ \text{Mass}_{recycle} = 0 $$

This prevents the model from accumulating mass during iterative calculations.

## Emitter Solutions

The model provides two output streams:

### Product Stream
- **Purpose**: Treated water for downstream use
- **Flow rate**: $Q_{influent} \times (1 - f_{recycle})$
- **Quality**: Same as influent

### Waste Stream
- **Purpose**: Waste water for disposal or further treatment
- **Flow rate**: $Q_{influent} \times f_{recycle}$
- **Quality**: Same as influent

## Design Considerations

### Recycle Efficiency

The recycle efficiency affects system performance:

- **High efficiency** (0.8-0.9): Maximum water recovery
- **Medium efficiency** (0.5-0.7): Balanced operation
- **Low efficiency** (0.1-0.3): Minimal recycling

### System Integration

The recycle model integrates with other treatment processes:

- **Upstream processes** - Receives treated water
- **Downstream processes** - Provides product water
- **Waste management** - Handles waste stream
- **Process optimization** - Optimizes water recovery

## Applications

Recycle systems are commonly used for:

- **Water recovery** - Maximizing water reuse
- **Process optimization** - Improving treatment efficiency
- **Waste minimization** - Reducing waste generation
- **Energy efficiency** - Reducing energy consumption
- **Cost reduction** - Lowering operational costs
- **Environmental compliance** - Meeting discharge requirements

## Advantages

- **Water conservation** - Reduces water consumption
- **Waste reduction** - Minimizes waste generation
- **Cost savings** - Reduces operational costs
- **Flexibility** - Adjustable recycle ratios
- **Process control** - Easy flow management
- **System integration** - Compatible with other processes

## Limitations

- **Convergence issues** - May require careful tuning
- **Mass balance** - Requires proper mass conservation
- **Flow control** - Needs accurate flow measurement
- **Quality control** - May accumulate contaminants
- **System complexity** - Adds complexity to process design
