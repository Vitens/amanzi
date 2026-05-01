# Membrane Degassing Model

## Overview

The membrane degassing model simulates membrane-based degassing systems used for gas removal from water. It operates in one or two stages, using vacuum pressure and sweep gas to remove dissolved gases including N₂, CO₂, and CH₄ through membrane contactors.

## Model Components

The membrane degassing model inherits from both the base `Model` class and the `Balance` class, enabling it to handle mass balance calculations and gas transfer processes.

## Key Parameters

| Parameter | Description | Units |
| --- | --- | --- |
| `n2_rq_stage_1` | Nitrogen air-to-water ratio for stage 1 | - |
| `co2_rq_stage_1` | CO₂ air-to-water ratio for stage 1 | - |
| `n2_rq_stage_2` | Nitrogen air-to-water ratio for stage 2 | - |
| `co2_rq_stage_2` | CO₂ air-to-water ratio for stage 2 | - |
| `vacuum_stage_1` | Vacuum pressure for stage 1 | bar |
| `vacuum_stage_2` | Vacuum pressure for stage 2 | bar |
| `num_stages` | Number of stages (1 or 2) | - |

## Two-Stage Degassing Process

### Stage 1 Gas Phase

The first stage creates a gas phase with nitrogen and CO₂:

**Total Gas Flow:**
$$ Q_{total1} = Q_{N_2,1} + Q_{CO_2,1} $$

**Gas Composition:**
- **Nitrogen**: $f_{N_2,1} = \frac{Q_{N_2,1}}{Q_{total1}} \times P_{vacuum1}$
- **CO₂**: $f_{CO_2,1} = \frac{Q_{CO_2,1}}{Q_{total1}} \times P_{vacuum1}$
- **Methane**: 0
- **Water vapor**: 0

**Gas Volume:**
$$ V_{gas1} = \frac{Q_{total1}}{P_{vacuum1}} $$

### Stage 2 Gas Phase

The second stage creates a gas phase with nitrogen and CO₂:

**Total Gas Flow:**
$$ Q_{total2} = Q_{N_2,2} + Q_{CO_2,2} $$

**Gas Composition:**
- **Nitrogen**: $f_{N_2,2} = \frac{Q_{N_2,2}}{Q_{total2}} \times P_{vacuum2}$
- **CO₂**: $f_{CO_2,2} = \frac{Q_{CO_2,2}}{Q_{total2}} \times P_{vacuum2}$
- **Methane**: 0
- **Water vapor**: 0

**Gas Volume:**
$$ V_{gas2} = \frac{Q_{total2}}{P_{vacuum2}} $$

## Gas Transfer Process

### Stage 1 Interaction

The water interacts with the first gas phase:

$$ \text{Solution}_{effluent1} = \text{Solution}_{influent} \leftrightarrow \text{Gas}_{stage1} $$

### Stage 2 Interaction

The effluent from stage 1 interacts with the second gas phase:

$$ \text{Solution}_{effluent2} = \text{Solution}_{effluent1} \leftrightarrow \text{Gas}_{stage2} $$

### Final Effluent

The final effluent depends on the number of stages:

**Single Stage:**
$$ \text{Solution}_{final} = \text{Solution}_{effluent1} $$

**Two Stages:**
$$ \text{Solution}_{final} = \text{Solution}_{effluent2} $$

## Pressure Loss Calculation

The model calculates pressure loss through the membrane:

### EXF14x40 Membrane

$$ \Delta P = 0.0003 \times Q^2 + 0.0379 \times Q - 0.0601 $$

### Other Membrane Types

$$ \Delta P = 0.0006 \times Q^2 + 0.0527 \times Q + 0.2351 $$

Where:
- $\Delta P$ = pressure loss (bar)
- $Q$ = membrane load (m³/h)

## Design Calculations

### Water Quality Parameters

The model tracks the following parameters:

**Influent Parameters:**
- **pH** - Acidity/alkalinity
- **CO₂** - Carbon dioxide concentration (mg/L)
- **CH₄** - Methane concentration (mg/L)
- **N₂** - Nitrogen concentration (mg/L)
- **SI** - Saturation index for calcite

**Effluent Parameters:**
- **pH** - Acidity/alkalinity
- **CO₂** - Carbon dioxide concentration (mg/L)
- **CH₄** - Methane concentration (mg/L)
- **N₂** - Nitrogen concentration (mg/L)
- **SI** - Saturation index for calcite

### Gas Phase Analysis

**Gas Volume:**
- **Volume** - Actual gas volume at vacuum pressure
- **Normal Volume** - Gas volume at standard conditions (1 bar)

**Gas Composition (Dry Basis):**
- **CH₄** - Methane percentage
- **CO₂** - Carbon dioxide percentage
- **N₂** - Nitrogen percentage

## Context Properties

The model provides additional context for design calculations:

| Property | Description | Units |
| --- | --- | --- |
| `_gas` | First stage gas phase object | - |
| `_gas2` | Second stage gas phase object | - |
| `pressure_loss` | Pressure loss calculation function | bar |

## Stage Configuration

### Single Stage Operation

When `num_stages = 1`:
- Only stage 1 operates
- Final effluent = stage 1 effluent
- Simplified operation

### Two Stage Operation

When `num_stages = 2`:
- Both stages operate in series
- Final effluent = stage 2 effluent
- Enhanced gas removal

## Integration with Solver

The membrane degassing model integrates with the overall solver framework by:

1. **Mass Balance** - Calculates water flows through the membrane system
2. **Quality Calculation** - Processes gas transfer reactions
3. **Design Parameters** - Calculates membrane dimensions and performance
4. **Energy Calculation** - Determines vacuum pump power requirements
5. **Gas Management** - Handles gas phase formation and removal

## Applications

Membrane degassing is commonly used for:

- **CO₂ removal** - Reduction of carbon dioxide
- **Nitrogen removal** - Reduction of dissolved nitrogen
- **Methane stripping** - Removal of methane
- **pH adjustment** - CO₂ removal increases pH
- **Pre-treatment** - Preparation for downstream processes
- **Water conditioning** - Improvement of water quality
- **Gas recovery** - Collection of valuable gases

## Advantages

- **Selective removal** - Can target specific gases
- **No air contamination** - Avoids introducing atmospheric gases
- **Compact design** - Smaller footprint than aeration systems
- **Gas recovery** - Can recover valuable gases
- **pH control** - Effective for pH adjustment through CO₂ removal
- **Energy efficient** - Lower energy consumption than aeration
- **Scalable** - Can operate in single or multiple stages

## Design Considerations

### Vacuum Pressure

- **Lower pressure** - Higher gas removal efficiency
- **Higher pressure** - Lower energy consumption
- **Optimal pressure** - Balance between efficiency and energy

### Air-to-Water Ratio

- **Higher ratio** - Better gas removal
- **Lower ratio** - Lower energy consumption
- **Optimal ratio** - Balance between performance and cost

### Number of Stages

- **Single stage** - Simpler operation, lower efficiency
- **Two stages** - Higher efficiency, more complex operation
- **Optimal stages** - Balance between performance and complexity
