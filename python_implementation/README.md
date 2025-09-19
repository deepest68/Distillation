# Python Implementation for Flash Calculations

This directory contains Python implementations of flash calculation methods described in the main documentation.

## Files

- **`flash_calculations.py`** - Core flash calculation functions and FlashCalculator class
- **`examples.py`** - Practical examples demonstrating various flash calculation scenarios
- **`requirements.txt`** - Python package dependencies

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from flash_calculations import FlashCalculator, print_flash_results

# Define component data (Antoine constants)
benzene_toluene_data = {
    'benzene': {'A': 6.90565, 'B': 1211.033, 'C': 220.79},
    'toluene': {'A': 6.95464, 'B': 1344.8, 'C': 219.482}
}

# Create flash calculator
flash_calc = FlashCalculator(benzene_toluene_data)

# Perform flash calculation
results = flash_calc.binary_flash(
    T=100,  # °C
    P=760,  # mmHg (1 atm)
    z_feed=[0.4, 0.6],  # 40% benzene, 60% toluene
    F=100   # mol/hr
)

# Display results
print_flash_results(results)

# Create visualization
fig = flash_calc.plot_flash_results(results)
```

## Running Examples

To run all examples:

```python
python examples.py
```

This will execute:
- Benzene-toluene flash calculation (matching theory section)
- Multi-component hydrocarbon mixture example
- Sensitivity analysis
- Industrial crude oil flash example
- Comparison of different operating conditions

## Features

- **Binary and multi-component flash calculations**
- **Rachford-Rice equation solver**
- **Material balance verification**
- **Visualization capabilities**
- **Sensitivity analysis tools**
- **Industrial application examples**
- **Non-ideal behavior support (activity coefficients)**

## Integration

These functions can be easily integrated into larger process simulation frameworks or used as standalone calculation tools for educational and industrial purposes.