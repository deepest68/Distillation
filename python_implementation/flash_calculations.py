"""
Flash Calculation Module for Distillation Systems

This module provides comprehensive tools for performing flash calculations
in distillation systems, including binary and multi-component mixtures.

Author: Generated for Distillation Repository
Date: 2024
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
import pandas as pd


def calculate_k_values(T, P, components):
    """
    Calculate K-values using Antoine equation and ideal gas assumption.
    
    Parameters:
    T (float): Temperature in Celsius
    P (float): Pressure in mmHg
    components (dict): Dictionary with component names as keys and Antoine constants as values
                      Each component should have 'A', 'B', 'C' parameters
    
    Returns:
    dict: K-values for each component
    """
    K_values = {}
    
    for component, antoine in components.items():
        # Calculate vapor pressure using Antoine equation
        A, B, C = antoine['A'], antoine['B'], antoine['C']
        P_sat = 10**(A - B/(C + T))  # Vapor pressure in mmHg
        
        # Calculate K-value
        K_values[component] = P_sat / P
    
    return K_values


def rachford_rice_equation(psi, z, K):
    """
    Rachford-Rice equation for flash calculations.
    
    Parameters:
    psi (float): Vapor fraction
    z (array): Feed composition (mole fractions)
    K (array): K-values for each component
    
    Returns:
    float: Rachford-Rice equation residual
    """
    return np.sum(z * (K - 1) / (1 + psi * (K - 1)))


def solve_flash_calculation(z, K, initial_guess=0.5):
    """
    Solve flash calculation using Rachford-Rice equation.
    
    Parameters:
    z (array): Feed composition (mole fractions)
    K (array): K-values for each component
    initial_guess (float): Initial guess for vapor fraction
    
    Returns:
    tuple: (vapor_fraction, liquid_composition, vapor_composition)
    """
    # Solve for vapor fraction
    psi_solution = fsolve(rachford_rice_equation, initial_guess, args=(z, K))[0]
    
    # Constrain vapor fraction between 0 and 1
    psi = max(0, min(1, psi_solution))
    
    # Calculate liquid and vapor compositions
    x = z / (1 + psi * (K - 1))  # Liquid composition
    y = K * x  # Vapor composition
    
    return psi, x, y


def flash_unit_material_balance(F, z, psi, x, y):
    """
    Verify material balance around flash unit.
    
    Parameters:
    F (float): Feed flow rate
    z (array): Feed composition
    psi (float): Vapor fraction
    x (array): Liquid composition
    y (array): Vapor composition
    
    Returns:
    dict: Material balance results
    """
    V = psi * F  # Vapor flow rate
    L = F - V    # Liquid flow rate
    
    # Overall material balance check
    overall_balance = abs(F - (V + L))
    
    # Component material balance check
    component_balance = []
    for i in range(len(z)):
        balance_error = abs(F * z[i] - (V * y[i] + L * x[i]))
        component_balance.append(balance_error)
    
    return {
        'vapor_flow': V,
        'liquid_flow': L,
        'overall_balance_error': overall_balance,
        'component_balance_errors': np.array(component_balance)
    }


class FlashCalculator:
    """
    A comprehensive flash calculation class for binary and multi-component systems.
    """
    
    def __init__(self, components_data):
        """
        Initialize flash calculator with component data.
        
        Parameters:
        components_data (dict): Dictionary containing Antoine constants for each component
        """
        self.components_data = components_data
        self.component_names = list(components_data.keys())
    
    def binary_flash(self, T, P, z_feed, F=100):
        """
        Perform flash calculation for binary mixture.
        
        Parameters:
        T (float): Temperature in Celsius
        P (float): Pressure in mmHg
        z_feed (list): Feed composition [mol fraction component 1, mol fraction component 2]
        F (float): Feed flow rate (mol/hr)
        
        Returns:
        dict: Complete flash calculation results
        """
        # Calculate K-values
        K_values = calculate_k_values(T, P, self.components_data)
        K = np.array([K_values[comp] for comp in self.component_names])
        z = np.array(z_feed)
        
        # Solve flash calculation
        psi, x, y = solve_flash_calculation(z, K)
        
        # Material balance verification
        balance = flash_unit_material_balance(F, z, psi, x, y)
        
        # Prepare results
        results = {
            'temperature_C': T,
            'pressure_mmHg': P,
            'feed_composition': dict(zip(self.component_names, z)),
            'K_values': K_values,
            'vapor_fraction': psi,
            'liquid_composition': dict(zip(self.component_names, x)),
            'vapor_composition': dict(zip(self.component_names, y)),
            'feed_flow_molhr': F,
            'vapor_flow_molhr': balance['vapor_flow'],
            'liquid_flow_molhr': balance['liquid_flow'],
            'material_balance_check': {
                'overall_error': balance['overall_balance_error'],
                'component_errors': dict(zip(self.component_names, balance['component_balance_errors']))
            }
        }
        
        return results
    
    def plot_flash_results(self, results):
        """
        Create visualization of flash calculation results.
        
        Parameters:
        results (dict): Results from flash calculation
        """
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
        
        components = list(results['feed_composition'].keys())
        
        # Composition comparison
        compositions = ['Feed', 'Liquid', 'Vapor']
        comp1_values = [
            results['feed_composition'][components[0]],
            results['liquid_composition'][components[0]],
            results['vapor_composition'][components[0]]
        ]
        comp2_values = [
            results['feed_composition'][components[1]],
            results['liquid_composition'][components[1]],
            results['vapor_composition'][components[1]]
        ]
        
        x = np.arange(len(compositions))
        width = 0.35
        
        ax1.bar(x - width/2, comp1_values, width, label=components[0], alpha=0.8)
        ax1.bar(x + width/2, comp2_values, width, label=components[1], alpha=0.8)
        ax1.set_xlabel('Stream')
        ax1.set_ylabel('Mole Fraction')
        ax1.set_title('Composition Comparison')
        ax1.set_xticks(x)
        ax1.set_xticklabels(compositions)
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Flow rates
        streams = ['Feed', 'Vapor', 'Liquid']
        flow_rates = [
            results['feed_flow_molhr'],
            results['vapor_flow_molhr'],
            results['liquid_flow_molhr']
        ]
        colors = ['blue', 'red', 'green']
        
        ax2.bar(streams, flow_rates, color=colors, alpha=0.7)
        ax2.set_ylabel('Flow Rate (mol/hr)')
        ax2.set_title('Stream Flow Rates')
        ax2.grid(True, alpha=0.3)
        
        # K-values
        K_vals = [results['K_values'][comp] for comp in components]
        ax3.bar(components, K_vals, color=['orange', 'purple'], alpha=0.7)
        ax3.set_ylabel('K-value')
        ax3.set_title('Equilibrium Distribution Coefficients')
        ax3.grid(True, alpha=0.3)
        
        # Vapor fraction visualization
        ax4.pie([results['vapor_fraction'], 1-results['vapor_fraction']], 
                labels=['Vapor', 'Liquid'], autopct='%1.1f%%', 
                colors=['lightcoral', 'lightblue'])
        ax4.set_title('Phase Distribution')
        
        plt.tight_layout()
        return fig


def print_flash_results(results):
    """
    Print formatted flash calculation results.
    
    Parameters:
    results (dict): Results from flash calculation
    """
    print("="*60)
    print("FLASH CALCULATION RESULTS")
    print("="*60)
    print(f"Temperature: {results['temperature_C']:.1f}°C")
    print(f"Pressure: {results['pressure_mmHg']:.0f} mmHg")
    print()
    
    print("K-VALUES:")
    for comp, k_val in results['K_values'].items():
        print(f"  {comp}: {k_val:.2f}")
    print()
    
    print("COMPOSITIONS (mole fraction):")
    print(f"{'Component':<12} {'Feed':<8} {'Liquid':<8} {'Vapor':<8}")
    print("-" * 40)
    for comp in results['feed_composition'].keys():
        print(f"{comp:<12} {results['feed_composition'][comp]:<8.3f} "
              f"{results['liquid_composition'][comp]:<8.3f} "
              f"{results['vapor_composition'][comp]:<8.3f}")
    print()
    
    print("FLOW RATES:")
    print(f"  Feed: {results['feed_flow_molhr']:.1f} mol/hr")
    print(f"  Vapor: {results['vapor_flow_molhr']:.1f} mol/hr")
    print(f"  Liquid: {results['liquid_flow_molhr']:.1f} mol/hr")
    print(f"  Vapor fraction: {results['vapor_fraction']:.1%}")
    print()
    
    print("MATERIAL BALANCE CHECK:")
    print(f"  Overall balance error: {results['material_balance_check']['overall_error']:.2e}")
    for comp, error in results['material_balance_check']['component_errors'].items():
        print(f"  {comp} balance error: {error:.2e}")


def antoine_with_pressure_correction(T, P, A, B, C, omega=0):
    """
    Modified Antoine equation with pressure correction for non-ideal behavior.
    
    Parameters:
    T (float): Temperature in Celsius
    P (float): System pressure in mmHg
    A, B, C (float): Antoine constants
    omega (float): Acentric factor for pressure correction
    
    Returns:
    float: Corrected vapor pressure
    """
    P_sat = 10**(A - B/(C + T))
    
    # Pressure correction factor (simplified)
    if omega > 0:
        correction = 1 + omega * (P / P_sat - 1) * 0.1
        P_sat *= correction
    
    return P_sat


def flash_with_activity_coefficients(z, K, gamma_L=None, phi_V=None):
    """
    Flash calculation including activity coefficients and fugacity coefficients.
    
    Parameters:
    z (array): Feed composition
    K (array): K-values
    gamma_L (array): Liquid activity coefficients (default: ideal)
    phi_V (array): Vapor fugacity coefficients (default: ideal)
    
    Returns:
    tuple: (vapor_fraction, liquid_composition, vapor_composition)
    """
    if gamma_L is None:
        gamma_L = np.ones_like(z)
    if phi_V is None:
        phi_V = np.ones_like(z)
    
    # Modified K-values for non-ideal behavior
    K_modified = K * gamma_L / phi_V
    
    return solve_flash_calculation(z, K_modified)


def sensitivity_analysis(flash_calculator, base_conditions, parameter, range_values):
    """
    Perform sensitivity analysis on flash calculation parameters.
    
    Parameters:
    flash_calculator: FlashCalculator instance
    base_conditions (dict): Base case conditions
    parameter (str): Parameter to vary ('T', 'P', or composition)
    range_values (array): Range of values to test
    
    Returns:
    pandas.DataFrame: Results for each parameter value
    """
    results_list = []
    
    for value in range_values:
        conditions = base_conditions.copy()
        
        if parameter == 'T':
            conditions['T'] = value
        elif parameter == 'P':
            conditions['P'] = value
        elif parameter.startswith('z_'):
            # Modify composition while maintaining closure
            comp_index = int(parameter.split('_')[1])
            conditions['z_feed'][comp_index] = value
            conditions['z_feed'][1-comp_index] = 1 - value
        
        result = flash_calculator.binary_flash(**conditions)
        
        results_list.append({
            parameter: value,
            'vapor_fraction': result['vapor_fraction'],
            'benzene_liquid': result['liquid_composition'].get('benzene', 0),
            'benzene_vapor': result['vapor_composition'].get('benzene', 0),
            'separation_factor': calculate_separation_factor(result)
        })
    
    return pd.DataFrame(results_list)


def calculate_separation_factor(results):
    """
    Calculate separation factor from flash results.
    
    Parameters:
    results (dict): Flash calculation results
    
    Returns:
    float: Separation factor
    """
    components = list(results['vapor_composition'].keys())
    if len(components) >= 2:
        comp1, comp2 = components[0], components[1]
        y1, y2 = results['vapor_composition'][comp1], results['vapor_composition'][comp2]
        x1, x2 = results['liquid_composition'][comp1], results['liquid_composition'][comp2]
        
        if x1 > 0 and x2 > 0:
            return (y1/x1) / (y2/x2)
    return 1.0


def process_stream_flash(stream_data, flash_conditions):
    """
    Flash calculation for process simulation integration.
    
    Parameters:
    stream_data (dict): Process stream information
    flash_conditions (dict): Flash operating conditions
    
    Returns:
    dict: Updated stream data with vapor and liquid outlets
    """
    # Extract relevant data
    composition = stream_data['composition']
    flow_rate = stream_data['flow_rate']
    
    # Perform flash calculation
    flash_calc = FlashCalculator(stream_data['component_data'])
    results = flash_calc.binary_flash(
        T=flash_conditions['temperature'],
        P=flash_conditions['pressure'],
        z_feed=list(composition.values()),
        F=flow_rate
    )
    
    # Create output streams
    vapor_stream = {
        'flow_rate': results['vapor_flow_molhr'],
        'composition': results['vapor_composition'],
        'temperature': flash_conditions['temperature'],
        'pressure': flash_conditions['pressure'],
        'phase': 'vapor'
    }
    
    liquid_stream = {
        'flow_rate': results['liquid_flow_molhr'],
        'composition': results['liquid_composition'],
        'temperature': flash_conditions['temperature'],
        'pressure': flash_conditions['pressure'],
        'phase': 'liquid'
    }
    
    return {'vapor': vapor_stream, 'liquid': liquid_stream}