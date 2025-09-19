#!/usr/bin/env python3
"""
Flash Unit Examples and Validation

This script demonstrates various flash unit calculations and validates
the implementation against known examples from the literature.
"""

from flash_unit import BenzeneTolueneFlash


def validate_against_readme_example():
    """
    Validate against the example in README.md:
    - 40 mol% benzene, 60 mol% toluene 
    - 100°C, pressure reduced from 2 atm to 1 atm
    - Expected results: ψ = 42%, vapor: 50% benzene, liquid: 28% benzene
    """
    print("=" * 70)
    print("VALIDATION: README.md Example (100°C, 1 atm)")
    print("=" * 70)
    
    flash_unit = BenzeneTolueneFlash()
    
    # README example uses mole fractions directly
    # We need to calculate equivalent weight percentages
    z_benzene_mol = 0.4
    z_toluene_mol = 0.6
    
    # Convert mole fractions to weight percentages for our function
    mw_benzene = flash_unit.molecular_weights['benzene']
    mw_toluene = flash_unit.molecular_weights['toluene']
    
    mass_benzene = z_benzene_mol * mw_benzene
    mass_toluene = z_toluene_mol * mw_toluene
    total_mass = mass_benzene + mass_toluene
    
    weight_percent_benzene = (mass_benzene / total_mass) * 100
    
    print(f"Converting from mole fractions to weight percent:")
    print(f"  Feed: {z_benzene_mol:.1f} mol benzene, {z_toluene_mol:.1f} mol toluene")
    print(f"  Equivalent: {weight_percent_benzene:.1f}% benzene by weight")
    print()
    
    # Run calculation at 100°C, 1 atm
    results = flash_unit.flash_calculation(weight_percent_benzene, 100.0, 1.0)
    
    print("RESULTS:")
    print(f"Temperature: 100°C")
    print(f"Pressure: 1 atm")
    print(f"Feed composition: {results['feed_composition']['benzene_mole_fraction']:.3f} mol benzene")
    print()
    
    print("Vapor pressures at 100°C:")
    print(f"  Benzene: {results['vapor_pressures_mmhg']['benzene']:.0f} mmHg")
    print(f"  Toluene: {results['vapor_pressures_mmhg']['toluene']:.0f} mmHg")
    print("  (README states: Benzene 1350 mmHg, Toluene 556 mmHg)")
    print()
    
    print("K-values:")
    print(f"  Benzene: {results['k_values']['benzene']:.2f}")
    print(f"  Toluene: {results['k_values']['toluene']:.2f}")
    print("  (README states: Benzene 1.78, Toluene 0.73)")
    print()
    
    print("Flash Results:")
    psi = results['vapor_fraction']
    liquid_comp = results['product_compositions']['liquid']
    vapor_comp = results['product_compositions']['vapor']
    
    print(f"  Vapor fraction: {psi:.3f} ({psi*100:.1f}%)")
    print(f"  (README states: 42%)")
    print()
    
    print("Product compositions:")
    print(f"  Liquid - Benzene: {liquid_comp['benzene']:.3f} ({liquid_comp['benzene']*100:.1f}%)")
    print(f"  Liquid - Toluene: {liquid_comp['toluene']:.3f} ({liquid_comp['toluene']*100:.1f}%)")
    print(f"  (README states: 28% benzene, 72% toluene)")
    print()
    
    print(f"  Vapor - Benzene: {vapor_comp['benzene']:.3f} ({vapor_comp['benzene']*100:.1f}%)")
    print(f"  Vapor - Toluene: {vapor_comp['toluene']:.3f} ({vapor_comp['toluene']*100:.1f}%)")
    print(f"  (README states: 50% benzene, 50% toluene)")
    print()


def demonstrate_temperature_effects():
    """
    Demonstrate how temperature affects the flash operation.
    """
    print("=" * 70)
    print("TEMPERATURE EFFECTS on 50:50 wt% Benzene-Toluene")
    print("=" * 70)
    
    flash_unit = BenzeneTolueneFlash()
    temperatures = [40, 60, 80, 100, 120]
    
    print("Temp(°C) | Vapor Fraction | Liquid Benzene | Vapor Benzene")
    print("-" * 60)
    
    for temp in temperatures:
        try:
            results = flash_unit.flash_calculation(50.0, temp, 1.0)
            psi = results['vapor_fraction']
            x_benzene = results['product_compositions']['liquid']['benzene']
            y_benzene = results['product_compositions']['vapor']['benzene']
            
            print(f"{temp:8.0f} | {psi:13.4f} | {x_benzene:13.4f} | {y_benzene:12.4f}")
        except Exception as e:
            print(f"{temp:8.0f} | Error: {str(e)}")
    
    print()


def demonstrate_pressure_effects():
    """
    Demonstrate how pressure affects the flash operation.
    """
    print("=" * 70)
    print("PRESSURE EFFECTS on 50:50 wt% Benzene-Toluene at 80°C")
    print("=" * 70)
    
    flash_unit = BenzeneTolueneFlash()
    pressures = [0.5, 1.0, 1.5, 2.0, 2.5]
    
    print("Press(atm) | Vapor Fraction | Liquid Benzene | Vapor Benzene")
    print("-" * 62)
    
    for pressure in pressures:
        try:
            results = flash_unit.flash_calculation(50.0, 80.0, pressure)
            psi = results['vapor_fraction']
            x_benzene = results['product_compositions']['liquid']['benzene']
            y_benzene = results['product_compositions']['vapor']['benzene']
            
            print(f"{pressure:10.1f} | {psi:13.4f} | {x_benzene:13.4f} | {y_benzene:12.4f}")
        except Exception as e:
            print(f"{pressure:10.1f} | Error: {str(e)}")
    
    print()


def main_problem_solution():
    """
    Solve the main problem: 50:50 weight percent benzene-toluene at 60°C, 1 atm.
    """
    print("=" * 70)
    print("MAIN PROBLEM SOLUTION")
    print("=" * 70)
    print("Problem: Flash unit with benzene-toluene (50:50 wt%) at 60°C, 1 atm")
    print()
    
    flash_unit = BenzeneTolueneFlash()
    results = flash_unit.flash_calculation(50.0, 60.0, 1.0)
    
    # Detailed analysis
    print("ANALYSIS:")
    print(f"At {60}°C and {1} atm:")
    
    k_benzene = results['k_values']['benzene']
    k_toluene = results['k_values']['toluene']
    
    print(f"  K-values: Benzene = {k_benzene:.3f}, Toluene = {k_toluene:.3f}")
    
    if k_benzene < 1 and k_toluene < 1:
        print("  Both K-values < 1: Both components prefer liquid phase")
        print("  Result: Minimal vaporization occurs")
    elif k_benzene > 1 and k_toluene > 1:
        print("  Both K-values > 1: Both components prefer vapor phase")
        print("  Result: Significant vaporization occurs")
    else:
        print("  Mixed K-values: One component prefers vapor, other prefers liquid")
        print("  Result: Moderate vaporization with separation")
    
    psi = results['vapor_fraction']
    print(f"  Vapor fraction: {psi:.6f} ({psi*100:.4f}%)")
    
    if psi < 0.001:
        print("  → This mixture remains almost entirely liquid at these conditions")
        print("  → To achieve significant vaporization, increase temperature or decrease pressure")
    
    print()
    print("RECOMMENDATIONS for better separation:")
    print("  1. Increase temperature (e.g., to 100°C)")
    print("  2. Decrease pressure (e.g., to 0.5 atm)")
    print("  3. Use both approaches for optimal separation")


if __name__ == "__main__":
    # Run the main problem solution
    main_problem_solution()
    
    print("\n" + "=" * 70)
    print("ADDITIONAL DEMONSTRATIONS")
    print("=" * 70)
    
    # Validate against README example
    validate_against_readme_example()
    
    # Demonstrate effects of operating conditions
    demonstrate_temperature_effects()
    demonstrate_pressure_effects()