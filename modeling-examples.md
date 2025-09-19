# Distillation Modeling Examples and Case Studies

## Binary Distillation Case Study: Benzene-Toluene Separation

### Problem Statement
Design a distillation column to separate a feed containing 40 mol% benzene and 60 mol% toluene. The feed rate is 100 kmol/hr at the bubble point. Specifications:
- Distillate: 95 mol% benzene
- Bottoms: 5 mol% benzene
- Reflux ratio: 1.5 times minimum

### Thermodynamic Data
```
Component     | Benzene | Toluene
Antoine A     | 6.90565 | 6.95464
Antoine B     | 1211.033| 1344.8
Antoine C     | 220.79  | 219.482
Relative Vol. | 2.4 (at 90°C)
```

### McCabe-Thiele Solution

#### Step 1: Equilibrium Curve
Using Raoult's Law and Antoine equation to generate VLE data.

#### Step 2: Operating Lines
- Feed line slope: q/(q-1) = ∞ (bubble point feed)
- Rectifying line: y = 0.6x + 0.38
- Stripping line: y = 1.85x - 0.0425

#### Step 3: Theoretical Stages
Stepping between equilibrium and operating lines yields:
- Theoretical stages: 8 (including reboiler)
- Feed stage: 4th from top
- Actual stages: 11 (assuming 75% efficiency)

### Rigorous Simulation Results (Aspen Plus)
```
Stream           | Feed  | Distillate | Bottoms
Flow (kmol/hr)   | 100   | 38.9       | 61.1
Benzene (mol%)   | 40    | 95.0       | 5.0
Toluene (mol%)   | 60    | 5.0        | 95.0
Temperature (°C) | 92.7  | 80.3       | 109.8
```

## Multi-Component Case Study: Depropanizer Column

### System Description
Separation of C3/C4 hydrocarbons in a refinery gas plant:

#### Feed Composition (mol%)
- Propane (C3): 35%
- Propylene (C3=): 25%
- n-Butane (nC4): 20%
- Isobutane (iC4): 15%
- Pentane+ (C5+): 5%

### Design Specifications
- Light key: Propylene (99% recovery in distillate)
- Heavy key: n-Butane (95% recovery in bottoms)
- Feed rate: 1000 kmol/hr
- Feed condition: 40°C, 2000 kPa

### Shortcut Method Results

#### Fenske Equation (Minimum Stages)
```
N_min = ln[(0.99/0.01) × (0.05/0.95)] / ln(1.8) = 8.3 stages
```

#### Underwood Method (Minimum Reflux)
```
R_min = 0.85 (calculated iteratively)
```

#### Actual Design
- Operating reflux: R = 1.3 × R_min = 1.1
- Actual stages: 22 (Gilliland correlation)
- Feed stage: 12th from top

### Rigorous Simulation Verification
Process simulation confirms shortcut estimates within 10% accuracy.

## Industrial Example: Ethylene Plant Demethanizer

### Process Context
Recovery of ethylene from steam cracker off-gas in a petrochemical complex.

### Operating Conditions
- Top pressure: 3500 kPa
- Bottom temperature: -85°C
- Refrigeration system: Propylene cascade
- Feed rate: 15,000 kmol/hr

### Key Components
- Methane: Light key component
- Ethylene: Heavy key component
- Hydrogen: Non-distributed (overhead)
- Ethane: Non-distributed (bottoms)

### Design Challenges
1. **Cryogenic Operation**: Special materials and insulation
2. **High Pressure**: Thick-walled vessels and piping
3. **Energy Integration**: Refrigeration optimization
4. **Safety**: Hydrocarbon release prevention

### Performance Metrics
- Ethylene recovery: >99.5%
- Energy consumption: 0.8 GJ/tonne ethylene
- Column efficiency: 85% (structured packing)

## Reactive Distillation Example: MTBE Synthesis

### Reaction System
```
Methanol + Isobutylene ⇌ MTBE
```

### Column Configuration
- Reaction zone: Stages 8-15 (catalyst packing)
- Rectifying section: Stages 1-7
- Stripping section: Stages 16-25
- Total stages: 25

### Design Considerations
1. **Catalyst Selection**: Acidic ion-exchange resin
2. **Temperature Control**: Exothermic reaction management
3. **Residence Time**: Adequate for reaction completion
4. **Separation**: Simultaneous product recovery

### Performance Results
- Isobutylene conversion: 98%
- MTBE purity: 99.2%
- Energy savings: 30% vs. separate reaction/separation

## Advanced Control Case Study

### Model Predictive Control Implementation

#### Controlled Variables
- Distillate composition (x_D)
- Bottoms composition (x_B)
- Column pressure (P)

#### Manipulated Variables
- Reflux flow rate (L)
- Reboiler duty (Q_R)
- Distillate flow rate (D)

#### Disturbance Variables
- Feed flow rate (F)
- Feed composition (z_F)
- Feed temperature (T_F)

### Control Performance
- Composition variance reduction: 60%
- Energy optimization: 15% savings
- Product quality improvement: 99.5% on-spec time

## Economic Optimization Example

### Cost Components
1. **Capital Costs**:
   - Column shell: $500,000
   - Internals: $200,000
   - Heat exchangers: $300,000
   - Total: $1,000,000

2. **Operating Costs** ($/year):
   - Steam: $400,000
   - Cooling water: $50,000
   - Electricity: $100,000
   - Maintenance: $80,000
   - Total: $630,000

### Optimization Variables
- Number of stages
- Reflux ratio
- Feed stage location
- Operating pressure

### Results
- Optimal stages: 28
- Optimal reflux ratio: 1.2
- NPV optimization: 15% IRR
- Payback period: 3.2 years

## Troubleshooting Guide

### Common Problems and Solutions

#### Poor Separation Efficiency
**Symptoms**: Off-specification products
**Causes**: 
- Flooding or weeping
- Poor liquid distribution
- Damaged internals

**Solutions**:
- Hydraulic debottlenecking
- Redistributor installation
- Internal inspection/replacement

#### High Energy Consumption
**Symptoms**: Excessive utility costs
**Causes**:
- Excessive reflux ratio
- Poor heat integration
- Fouled heat exchangers

**Solutions**:
- Reflux optimization
- Heat exchanger cleaning
- Process integration studies

#### Control Problems
**Symptoms**: Composition oscillations
**Causes**:
- Poor controller tuning
- Inadequate instrumentation
- Process nonlinearities

**Solutions**:
- Advanced control implementation
- Analyzer upgrades
- Model-based control

## References

1. Kister, H.Z. "Distillation Design" McGraw-Hill, 1992
2. Seader, J.D. et al. "Separation Process Principles" Wiley, 2016
3. Luyben, W.L. "Distillation Design and Control Using Aspen" Wiley, 2013
4. Taylor, R. & Krishna, R. "Multicomponent Mass Transfer" Wiley, 1993