# Flash Unit Python Implementation

This directory contains a Python implementation of flash unit calculations for benzene-toluene binary mixtures.

## Files

- `flash_unit.py` - Main implementation of the `BenzeneTolueneFlash` class
- `flash_unit_examples.py` - Examples and validation scripts
- `README_flash.md` - This documentation file

## Problem Solved

The implementation solves the specific problem:
**"Add the python code for a flash unit with two components (benzene and toluene) at 1 atm, 60 deg.C for the 50:50 weight percent binary mixture."**

## Key Features

### 1. BenzeneTolueneFlash Class
- Antoine equation implementation for vapor pressure calculations
- Weight percent to mole fraction conversion
- K-value calculations using ideal solution assumptions
- Rachford-Rice equation solver using Newton-Raphson method
- Complete material balance calculations

### 2. Thermodynamic Data
Uses Antoine constants from the repository's modeling examples:
- **Benzene**: A=6.90565, B=1211.033, C=220.79
- **Toluene**: A=6.95464, B=1344.8, C=219.482

### 3. Results for the Specified Problem

For 50:50 weight percent benzene-toluene at 60°C and 1 atm:

```
Feed composition: 50.0% benzene, 50.0% toluene (by weight)
                  54.1% benzene, 45.9% toluene (by mole)

Operating conditions: 60.0°C, 1.0 atm

Vapor pressures: Benzene 391.5 mmHg, Toluene 139.0 mmHg
K-values: Benzene 0.515, Toluene 0.183

Results:
- Vapor fraction: 0.0000 (0.00%)
- Liquid fraction: 1.0000 (100.00%)
- Mixture remains entirely in liquid phase
```

### 4. Physical Interpretation

At 60°C and 1 atm, both K-values are less than 1, indicating both components prefer the liquid phase. This results in minimal vaporization. For significant separation, higher temperature or lower pressure would be needed.

## Usage

### Basic Usage
```python
from flash_unit import BenzeneTolueneFlash

flash_unit = BenzeneTolueneFlash()
results = flash_unit.flash_calculation(
    weight_percent_benzene=50.0,
    temperature_c=60.0,
    pressure_atm=1.0
)
```

### Run Examples
```bash
python flash_unit.py              # Main problem solution
python flash_unit_examples.py     # Comprehensive examples and validation
```

## Validation

The implementation has been validated against:
1. Literature values for vapor pressures and K-values at 100°C
2. Material balance verification (conservation of mass)
3. Thermodynamically consistent behavior across different conditions

## Mathematical Foundation

The implementation uses:
- **Antoine Equation**: log₁₀(P°) = A - B/(T + C)
- **K-values**: K = P°/P (ideal solution assumption)
- **Rachford-Rice Equation**: Σ[zᵢ(Kᵢ-1)/(1+ψ(Kᵢ-1))] = 0
- **Material Balance**: F = V + L, Fzᵢ = Vyᵢ + Lxᵢ

Where:
- P° = vapor pressure, P = system pressure
- ψ = vapor fraction (V/F)
- zᵢ, yᵢ, xᵢ = mole fractions in feed, vapor, liquid phases