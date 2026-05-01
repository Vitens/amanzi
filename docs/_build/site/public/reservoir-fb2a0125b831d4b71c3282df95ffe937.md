# Reservoir Model

## Overview

The reservoir model simulates water storage reservoirs with optional integrated aeration systems. It provides water storage capacity and can perform gas transfer processes to improve water quality through CO₂ removal, oxygen addition, and methane stripping.

## Model Components

The reservoir model inherits from the base `Model` class and functions as both a storage unit and a treatment process when integrated aeration is enabled.

## Key Parameters

| Parameter | Description | Units |
| --- | --- | --- |
| `integrated_aeration` | Enable integrated aeration system | bool |
| `co2_removal` | CO₂ removal efficiency | - |
| `o2_saturation` | Oxygen saturation efficiency | - |

## Reservoir Operations

### Storage Mode

In basic storage mode, the reservoir simply stores water without treatment:

$$ \text{Reservoir}_{stored} = \text{Influent}_{water} $$

### Integrated Aeration Mode

When integrated aeration is enabled, the reservoir performs gas transfer processes:

#### Air Composition

The model uses standard atmospheric air composition:
- **Oxygen**: 21% (0.21)
- **Nitrogen**: 79% (0.79)
- **Carbon dioxide**: 0.043% (0.00043)

#### Gas Transfer Calculations

**Oxygen Saturation:**
$$ C_{O_2,max} = C_{O_2,saturated} $$

**Oxygen Addition:**
$$ C_{O_2,added} = \max(0, C_{O_2,max} \times \eta_{O_2} - C_{O_2,influent}) $$

**CO₂ Removal:**
$$ C_{CO_2,removed} = (C_{CO_2,influent} - C_{CO_2,min}) \times \eta_{CO_2} $$

**Methane Removal:**
$$ C_{CH_4,removed} = C_{CH_4,influent} \times 0.999 $$

Where:
- $C_{O_2,max}$ = maximum oxygen concentration
- $C_{O_2,saturated}$ = oxygen concentration at saturation
- $\eta_{O_2}$ = oxygen saturation efficiency
- $\eta_{CO_2}$ = CO₂ removal efficiency
- $C_{CO_2,min}$ = minimum CO₂ concentration

#### Solution Changes

The model applies the following changes to the water solution:

$$ \text{Solution}_{final} = \text{Solution}_{influent} + \Delta C_{O_2} - \Delta C_{CO_2} - \Delta C_{CH_4} $$

Where:
- $\Delta C_{O_2} = C_{O_2,added}$
- $\Delta C_{CO_2} = C_{CO_2,removed}$
- $\Delta C_{CH_4} = C_{CH_4,removed}$

## Mass Balance Equations

The reservoir model provides mass balance equations for the solver:

### Flow Balance

**All incoming streams must equal all outgoing streams:**

$$ \sum Q_{incoming} \times \eta_{minor} + \sum Q_{outgoing} \times (-1) + \sum Q_{flush} \times (-1) = Q_{minor} $$

Where:
- $Q_{incoming}$ = incoming flow rates
- $Q_{outgoing}$ = outgoing flow rates
- $Q_{flush}$ = flush flow rates
- $\eta_{minor}$ = minor loss percentage
- $Q_{minor}$ = minor loss flow rate

## Stream Types

### Product Stream

The reservoir provides treated water through the product stream:

$$ \text{Product}_{out} = \text{Reservoir}_{stored} $$

### Flush Stream

The reservoir can provide stored water through the flush stream:

$$ \text{Flush}_{out} = \text{Reservoir}_{stored} $$

## Water Quality Processing

### Aeration Process

When integrated aeration is enabled, the process follows these steps:

1. **Air Interaction** - Water interacts with atmospheric air
2. **Saturation Calculation** - Determine maximum oxygen concentration
3. **Gas Transfer** - Calculate oxygen addition and CO₂ removal
4. **Solution Update** - Apply concentration changes
5. **Storage** - Store the treated water

### Quality Parameters

The model tracks the following water quality parameters:
- **pH** - Acidity/alkalinity
- **O₂** - Dissolved oxygen concentration
- **CO₂** - Carbon dioxide concentration
- **CH₄** - Methane concentration

## Design Considerations

### Aeration Efficiency

The aeration efficiency depends on:
- **Contact time** - Duration of air-water contact
- **Surface area** - Available surface for gas transfer
- **Mixing** - Degree of water mixing
- **Temperature** - Water temperature affects gas solubility

### Storage Capacity

The reservoir provides:
- **Water storage** - Temporary storage of treated water
- **Flow equalization** - Balancing of flow variations
- **Emergency storage** - Backup water supply
- **Quality improvement** - Gas transfer processes

## Integration with Solver

The reservoir model integrates with the overall solver framework by:

1. **Mass Balance** - Balances incoming and outgoing flows
2. **Quality Calculation** - Processes water quality through aeration
3. **Storage Management** - Manages water storage and release
4. **Flow Control** - Controls flow distribution to downstream processes
5. **Emergency Supply** - Provides backup water supply

## Applications

Reservoirs are commonly used for:
- **Water storage** - Temporary storage of treated water
- **Flow equalization** - Balancing flow variations
- **Emergency supply** - Backup water supply during maintenance
- **Quality improvement** - Gas transfer through aeration
- **Pressure management** - Maintaining system pressure
- **Process buffering** - Smoothing process variations
