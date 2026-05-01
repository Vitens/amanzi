# Mass Balance

## Overview

The mass balance system provides detailed chemical-level analysis for each treatment unit in the water treatment process. It tracks the transformation of water quality parameters from influent to effluent streams, enabling comprehensive analysis of treatment efficiency and chemical changes.

## Mass Balance Components

Each treatment unit maintains its own mass balance based on PHREEQC solution objects, allowing for precise tracking of:

- **Chemical species concentrations** - Individual ion concentrations (Ca²⁺, Mg²⁺, Na⁺, Cl⁻, etc.)
- **Abstract parameters** - pH, conductivity, hardness, saturation indices
- **Dissolved gases** - O₂, CO₂, CH₄, N₂, H₂S
- **Extraneous properties** - PFAS, VOC, color, TOC

## Stream Analysis

### Product Streams

The mass balance tracks changes in the main product stream:

**Influent → Effluent Analysis:**
- **Concentration changes** - Absolute change in parameter values
- **Percentage changes** - Relative change as percentage of influent value
- **Treatment efficiency** - Removal or addition efficiency

### Waste Streams

For treatment units with waste streams, the mass balance provides:

**Waste Stream Analysis:**
- **Concentrate streams** - RO/NF concentrate quality
- **Backwash water** - Sand filter backwash characteristics
- **Sludge streams** - Softening sludge composition
- **Gas streams** - Off-gas from aeration processes

## Mass Balance Calculations

### Concentration Changes

**Absolute Change:**
$$ \Delta C = C_{effluent} - C_{influent} $$

**Percentage Change:**
$$ \Delta C\% = \frac{C_{effluent} - C_{influent}}{C_{influent}} \times 100\% $$

### Treatment Efficiency

**Removal Efficiency:**
$$ \eta_{removal} = \frac{C_{influent} - C_{effluent}}{C_{influent}} \times 100\% $$

**Addition Efficiency:**
$$ \eta_{addition} = \frac{C_{effluent} - C_{influent}}{C_{target} - C_{influent}} \times 100\% $$

## Display Format

### Value Formatting

The mass balance uses intelligent formatting based on parameter magnitude:

- **Values > 100**: Displayed with 0 decimal places
- **Values 10-100**: Displayed with 1 decimal place  
- **Values < 10**: Displayed with 2 decimal places
- **Undefined values**: Displayed as "-"

### Change Indicators

**Visual Indicators:**
- **Green background**: Increased concentrations (positive change)
- **Red background**: Decreased concentrations (negative change)
- **Percentage limits**: Changes > 1000% or < -1000% displayed as "-"

## Applications

### Treatment Process Analysis

Mass balance analysis is particularly valuable for:

**Chemical Treatment Processes:**
- **Softening** - Ca²⁺ and Mg²⁺ removal efficiency
- **Ion exchange** - Ion removal and replacement
- **Chemical dosing** - pH adjustment and coagulation

**Physical Treatment Processes:**
- **Filtration** - Particle and contaminant removal
- **Aeration** - Gas transfer efficiency
- **Membrane processes** - Rejection and passage rates

### Waste Stream Management

**Concentrate Analysis:**
- **RO concentrate** - Salt concentration and scaling potential
- **NF concentrate** - Hardness and organic matter concentration
- **Backwash water** - Suspended solids and iron content

**Gas Stream Analysis:**
- **Off-gas composition** - CH₄, CO₂, N₂ concentrations
- **Gas recovery potential** - Valuable gas collection
- **Environmental impact** - Greenhouse gas emissions

## Integration with Solver

The mass balance integrates with the overall solver framework by:

1. **Quality Calculation** - Processes water quality changes through each unit
2. **Stream Tracking** - Monitors influent and effluent quality
3. **Efficiency Analysis** - Calculates treatment efficiencies
4. **Waste Management** - Tracks waste stream characteristics
5. **Reporting** - Generates comprehensive mass balance reports

## Quality Parameters

The mass balance tracks comprehensive water quality parameters:

### Physical Parameters
- **pH** - Acidity/alkalinity
- **Conductivity** - Electrical conductivity
- **Temperature** - Water temperature
- **Color** - Water color
- **Turbidity** - Suspended solids

### Chemical Parameters
- **Major ions** - Ca²⁺, Mg²⁺, Na⁺, K⁺, Cl⁻, SO₄²⁻, HCO₃⁻
- **Nutrients** - NH₄⁺, NO₃⁻, NO₂⁻, PO₄³⁻
- **Metals** - Fe, Mn, Al, Cu, Zn
- **Gases** - O₂, CO₂, CH₄, N₂, H₂S

### Derived Parameters
- **Hardness** - Total hardness as CaCO₃
- **Alkalinity** - Total alkalinity
- **Saturation indices** - Calcite, gypsum, etc.
- **CCPP** - Calcium carbonate precipitation potential 