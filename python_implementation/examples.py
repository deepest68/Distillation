"""
Practical Examples for Flash Calculations

This module demonstrates practical applications of the flash calculation
methods for various chemical systems.

Author: Generated for Distillation Repository
Date: 2024
"""

import numpy as np
import matplotlib.pyplot as plt
from flash_calculations import FlashCalculator, print_flash_results, sensitivity_analysis


def benzene_toluene_example():
    """
    Reproduce the benzene-toluene flash calculation from the theory section.
    This example matches the theoretical calculations in the README.
    """
    print("BENZENE-TOLUENE FLASH CALCULATION EXAMPLE")
    print("=" * 50)
    
    # Define component data (Antoine constants)
    benzene_toluene_data = {
        'benzene': {'A': 6.90565, 'B': 1211.033, 'C': 220.79},
        'toluene': {'A': 6.95464, 'B': 1344.8, 'C': 219.482}
    }
    
    # Create flash calculator
    flash_calc = FlashCalculator(benzene_toluene_data)
    
    # Perform flash calculation (conditions from theory example)
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
    plt.suptitle('Benzene-Toluene Flash Calculation Results', fontsize=16)
    plt.show()
    
    return results


def multicomponent_example():
    """
    Example flash calculation for a three-component hydrocarbon mixture.
    """
    print("\nMULTI-COMPONENT FLASH CALCULATION EXAMPLE")
    print("=" * 50)
    
    # Define component data for propane-butane-pentane mixture
    multicomponent_data = {
        'propane': {'A': 6.82973, 'B': 803.997, 'C': 246.99},
        'butane': {'A': 6.83029, 'B': 945.906, 'C': 240.0},
        'pentane': {'A': 6.85221, 'B': 1064.840, 'C': 232.014}
    }
    
    multi_calc = FlashCalculator(multicomponent_data)
    
    # Flash calculation for three-component mixture
    multi_results = multi_calc.binary_flash(
        T=60,   # °C
        P=760,  # mmHg
        z_feed=[0.3, 0.4, 0.3],  # Propane, Butane, Pentane
        F=200   # mol/hr
    )
    
    print_flash_results(multi_results)
    
    # Create visualization
    fig = multi_calc.plot_flash_results(multi_results)
    plt.suptitle('Propane-Butane-Pentane Flash Calculation', fontsize=16)
    plt.show()
    
    return multi_results


def sensitivity_analysis_example():
    """
    Demonstrate sensitivity analysis for flash calculations.
    """
    print("\nSENSITIVITY ANALYSIS EXAMPLE")
    print("=" * 40)
    
    # Use benzene-toluene system
    benzene_toluene_data = {
        'benzene': {'A': 6.90565, 'B': 1211.033, 'C': 220.79},
        'toluene': {'A': 6.95464, 'B': 1344.8, 'C': 219.482}
    }
    
    flash_calc = FlashCalculator(benzene_toluene_data)
    
    # Base case conditions
    base_case = {
        'T': 100,
        'P': 760,
        'z_feed': [0.4, 0.6],
        'F': 100
    }
    
    # Temperature sensitivity
    print("Analyzing temperature sensitivity...")
    temp_range = np.linspace(80, 120, 20)
    temp_sensitivity = sensitivity_analysis(flash_calc, base_case, 'T', temp_range)
    
    # Pressure sensitivity  
    print("Analyzing pressure sensitivity...")
    pressure_range = np.linspace(500, 1000, 20)
    pressure_sensitivity = sensitivity_analysis(flash_calc, base_case, 'P', pressure_range)
    
    # Plot results
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    
    # Temperature effects
    ax1.plot(temp_sensitivity['T'], temp_sensitivity['vapor_fraction'], 'b-o', markersize=4)
    ax1.set_xlabel('Temperature (°C)')
    ax1.set_ylabel('Vapor Fraction')
    ax1.set_title('Vapor Fraction vs Temperature')
    ax1.grid(True, alpha=0.3)
    
    ax2.plot(temp_sensitivity['T'], temp_sensitivity['separation_factor'], 'r-s', markersize=4)
    ax2.set_xlabel('Temperature (°C)')
    ax2.set_ylabel('Separation Factor')
    ax2.set_title('Separation Factor vs Temperature')
    ax2.grid(True, alpha=0.3)
    
    # Pressure effects
    ax3.plot(pressure_sensitivity['P'], pressure_sensitivity['vapor_fraction'], 'g-^', markersize=4)
    ax3.set_xlabel('Pressure (mmHg)')
    ax3.set_ylabel('Vapor Fraction')
    ax3.set_title('Vapor Fraction vs Pressure')
    ax3.grid(True, alpha=0.3)
    
    ax4.plot(pressure_sensitivity['P'], pressure_sensitivity['separation_factor'], 'm-d', markersize=4)
    ax4.set_xlabel('Pressure (mmHg)')
    ax4.set_ylabel('Separation Factor')
    ax4.set_title('Separation Factor vs Pressure')
    ax4.grid(True, alpha=0.3)
    
    plt.suptitle('Flash Calculation Sensitivity Analysis', fontsize=16)
    plt.tight_layout()
    plt.show()
    
    return temp_sensitivity, pressure_sensitivity


def industrial_example():
    """
    Industrial example: Crude oil fractionation flash calculation.
    """
    print("\nINDUSTRIAL EXAMPLE: CRUDE OIL FLASH")
    print("=" * 40)
    
    # Simplified crude oil components (light naphtha and heavy naphtha)
    crude_data = {
        'light_naphtha': {'A': 6.87776, 'B': 1171.530, 'C': 224.366},  # n-hexane approx
        'heavy_naphtha': {'A': 6.90240, 'B': 1267.828, 'C': 216.636}   # n-heptane approx
    }
    
    crude_calc = FlashCalculator(crude_data)
    
    # Industrial flash conditions
    industrial_results = crude_calc.binary_flash(
        T=150,  # °C (typical flash temperature)
        P=500,  # mmHg (vacuum operation)
        z_feed=[0.3, 0.7],  # 30% light, 70% heavy naphtha
        F=1000  # mol/hr (industrial scale)
    )
    
    print_flash_results(industrial_results)
    
    # Economic analysis
    print("\nECONOMIC ANALYSIS:")
    print(f"Light product recovery: {industrial_results['vapor_flow_molhr']:.1f} mol/hr "
          f"({100*industrial_results['vapor_fraction']:.1f}% of feed)")
    print(f"Heavy product: {industrial_results['liquid_flow_molhr']:.1f} mol/hr")
    print(f"Light component purity in vapor: "
          f"{100*industrial_results['vapor_composition']['light_naphtha']:.1f}%")
    
    return industrial_results


def comparison_example():
    """
    Compare flash calculations at different operating conditions.
    """
    print("\nCOMPARISON OF OPERATING CONDITIONS")
    print("=" * 45)
    
    # Benzene-toluene system
    benzene_toluene_data = {
        'benzene': {'A': 6.90565, 'B': 1211.033, 'C': 220.79},
        'toluene': {'A': 6.95464, 'B': 1344.8, 'C': 219.482}
    }
    
    flash_calc = FlashCalculator(benzene_toluene_data)
    
    # Different operating conditions
    conditions = [
        {'T': 80, 'P': 760, 'name': 'Low Temperature'},
        {'T': 100, 'P': 760, 'name': 'Base Case'},
        {'T': 120, 'P': 760, 'name': 'High Temperature'},
        {'T': 100, 'P': 500, 'name': 'Vacuum Operation'},
        {'T': 100, 'P': 1000, 'name': 'High Pressure'}
    ]
    
    results_comparison = []
    
    for condition in conditions:
        result = flash_calc.binary_flash(
            T=condition['T'],
            P=condition['P'], 
            z_feed=[0.4, 0.6],
            F=100
        )
        
        results_comparison.append({
            'condition': condition['name'],
            'temperature': condition['T'],
            'pressure': condition['P'],
            'vapor_fraction': result['vapor_fraction'],
            'benzene_recovery': result['vapor_flow_molhr'] * result['vapor_composition']['benzene'],
            'separation_efficiency': result['vapor_composition']['benzene'] - result['liquid_composition']['benzene']
        })
    
    # Display comparison table
    print(f"{'Condition':<18} {'T(°C)':<6} {'P(mmHg)':<8} {'Vapor Frac':<11} {'Benzene Recovery':<15} {'Sep. Efficiency':<15}")
    print("-" * 85)
    
    for res in results_comparison:
        print(f"{res['condition']:<18} {res['temperature']:<6.0f} {res['pressure']:<8.0f} "
              f"{res['vapor_fraction']:<11.3f} {res['benzene_recovery']:<15.1f} "
              f"{res['separation_efficiency']:<15.3f}")
    
    # Visualization
    conditions_names = [res['condition'] for res in results_comparison]
    vapor_fractions = [res['vapor_fraction'] for res in results_comparison]
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(conditions_names, vapor_fractions, color=['skyblue', 'orange', 'lightcoral', 'lightgreen', 'plum'])
    plt.ylabel('Vapor Fraction')
    plt.title('Vapor Fraction Comparison for Different Operating Conditions')
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    
    # Add value labels on bars
    for bar, vf in zip(bars, vapor_fractions):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
                f'{vf:.3f}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.show()
    
    return results_comparison


def main():
    """
    Run all example calculations.
    """
    print("FLASH CALCULATION EXAMPLES")
    print("=" * 60)
    print("This module demonstrates various flash calculation examples")
    print("for binary and multi-component systems.\n")
    
    try:
        # Run examples
        benzene_results = benzene_toluene_example()
        multi_results = multicomponent_example()
        temp_sens, press_sens = sensitivity_analysis_example()
        industrial_results = industrial_example()
        comparison_results = comparison_example()
        
        print("\n" + "="*60)
        print("ALL EXAMPLES COMPLETED SUCCESSFULLY!")
        print("="*60)
        
        return {
            'benzene_toluene': benzene_results,
            'multicomponent': multi_results,
            'sensitivity': {'temperature': temp_sens, 'pressure': press_sens},
            'industrial': industrial_results,
            'comparison': comparison_results
        }
        
    except Exception as e:
        print(f"\nError running examples: {str(e)}")
        print("Please ensure all required packages are installed:")
        print("pip install numpy matplotlib scipy pandas")
        return None


if __name__ == "__main__":
    results = main()