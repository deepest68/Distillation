#!/usr/bin/env python3
"""
Flash Unit Calculation for Benzene-Toluene Binary Mixture

This module implements a flash unit calculation for a two-component system
containing benzene and toluene. The implementation includes:
- Antoine equation for vapor pressure calculations
- Rachford-Rice equation solver for vapor fraction
- Material balance calculations
- K-value calculations

Author: Generated for Distillation repository
"""

import math
from typing import Tuple, Dict


class BenzeneTolueneFlash:
    """
    Flash unit calculator for benzene-toluene binary mixture.
    
    This class implements the flash operation calculations for a binary mixture
    of benzene and toluene using the Rachford-Rice equation and vapor-liquid
    equilibrium relationships.
    """
    
    def __init__(self):
        """Initialize with component properties."""
        # Antoine equation constants for vapor pressure calculation
        # log10(P_sat) = A - B/(T + C), where P_sat is in mmHg, T in °C
        self.antoine_constants = {
            'benzene': {'A': 6.90565, 'B': 1211.033, 'C': 220.79},
            'toluene': {'A': 6.95464, 'B': 1344.8, 'C': 219.482}
        }
        
        # Molecular weights (g/mol)
        self.molecular_weights = {
            'benzene': 78.11,
            'toluene': 92.14
        }
    
    def vapor_pressure(self, component: str, temperature_c: float) -> float:
        """
        Calculate vapor pressure using Antoine equation.
        
        Args:
            component: 'benzene' or 'toluene'
            temperature_c: Temperature in Celsius
            
        Returns:
            Vapor pressure in mmHg
        """
        constants = self.antoine_constants[component]
        A, B, C = constants['A'], constants['B'], constants['C']
        
        log_p_sat = A - B / (temperature_c + C)
        p_sat_mmhg = 10 ** log_p_sat
        
        return p_sat_mmhg
    
    def weight_to_mole_fraction(self, weight_percent_benzene: float) -> Tuple[float, float]:
        """
        Convert weight percent to mole fractions.
        
        Args:
            weight_percent_benzene: Weight percentage of benzene (0-100)
            
        Returns:
            Tuple of (mole_fraction_benzene, mole_fraction_toluene)
        """
        # Convert percentages to fractions
        w_benzene = weight_percent_benzene / 100.0
        w_toluene = 1.0 - w_benzene
        
        # Calculate moles
        mw_benzene = self.molecular_weights['benzene']
        mw_toluene = self.molecular_weights['toluene']
        
        # Assume 100g total mass for calculation
        moles_benzene = (w_benzene * 100) / mw_benzene
        moles_toluene = (w_toluene * 100) / mw_toluene
        
        total_moles = moles_benzene + moles_toluene
        
        x_benzene = moles_benzene / total_moles
        x_toluene = moles_toluene / total_moles
        
        return x_benzene, x_toluene
    
    def calculate_k_values(self, temperature_c: float, pressure_atm: float) -> Dict[str, float]:
        """
        Calculate K-values (equilibrium distribution coefficients).
        
        Args:
            temperature_c: Temperature in Celsius
            pressure_atm: Pressure in atmospheres
            
        Returns:
            Dictionary with K-values for benzene and toluene
        """
        # Convert pressure to mmHg
        pressure_mmhg = pressure_atm * 760.0
        
        # Calculate vapor pressures
        p_sat_benzene = self.vapor_pressure('benzene', temperature_c)
        p_sat_toluene = self.vapor_pressure('toluene', temperature_c)
        
        # Calculate K-values (assuming ideal solution)
        k_benzene = p_sat_benzene / pressure_mmhg
        k_toluene = p_sat_toluene / pressure_mmhg
        
        return {
            'benzene': k_benzene,
            'toluene': k_toluene
        }
    
    def rachford_rice_equation(self, psi: float, z_benzene: float, z_toluene: float,
                              k_benzene: float, k_toluene: float) -> float:
        """
        Rachford-Rice equation for flash calculations.
        
        Args:
            psi: Vapor fraction (V/F)
            z_benzene: Mole fraction of benzene in feed
            z_toluene: Mole fraction of toluene in feed
            k_benzene: K-value for benzene
            k_toluene: K-value for toluene
            
        Returns:
            Value of Rachford-Rice equation (should be zero at solution)
        """
        term1 = z_benzene * (k_benzene - 1) / (1 + psi * (k_benzene - 1))
        term2 = z_toluene * (k_toluene - 1) / (1 + psi * (k_toluene - 1))
        
        return term1 + term2
    
    def solve_vapor_fraction(self, z_benzene: float, z_toluene: float,
                            k_benzene: float, k_toluene: float,
                            tolerance: float = 1e-6, max_iterations: int = 100) -> float:
        """
        Solve for vapor fraction using Newton-Raphson method.
        
        Args:
            z_benzene: Mole fraction of benzene in feed
            z_toluene: Mole fraction of toluene in feed
            k_benzene: K-value for benzene
            k_toluene: K-value for toluene
            tolerance: Convergence tolerance
            max_iterations: Maximum number of iterations
            
        Returns:
            Vapor fraction (psi)
        """
        # Initial guess
        psi = 0.5
        
        for iteration in range(max_iterations):
            # Calculate function value
            f = self.rachford_rice_equation(psi, z_benzene, z_toluene, k_benzene, k_toluene)
            
            # Calculate derivative
            dpsi = 1e-8
            f_plus = self.rachford_rice_equation(psi + dpsi, z_benzene, z_toluene, k_benzene, k_toluene)
            df_dpsi = (f_plus - f) / dpsi
            
            # Newton-Raphson update
            psi_new = psi - f / df_dpsi
            
            # Ensure psi stays within bounds [0, 1]
            psi_new = max(0.0, min(1.0, psi_new))
            
            # Check convergence
            if abs(psi_new - psi) < tolerance:
                return psi_new
            
            psi = psi_new
        
        raise RuntimeError(f"Failed to converge after {max_iterations} iterations")
    
    def calculate_product_compositions(self, psi: float, z_benzene: float, z_toluene: float,
                                     k_benzene: float, k_toluene: float) -> Dict[str, Dict[str, float]]:
        """
        Calculate liquid and vapor product compositions.
        
        Args:
            psi: Vapor fraction
            z_benzene: Mole fraction of benzene in feed
            z_toluene: Mole fraction of toluene in feed
            k_benzene: K-value for benzene
            k_toluene: K-value for toluene
            
        Returns:
            Dictionary with liquid and vapor compositions
        """
        # Liquid compositions
        x_benzene = z_benzene / (1 + psi * (k_benzene - 1))
        x_toluene = z_toluene / (1 + psi * (k_toluene - 1))
        
        # Vapor compositions
        y_benzene = k_benzene * x_benzene
        y_toluene = k_toluene * x_toluene
        
        # Normalize vapor compositions to ensure they sum to 1
        y_total = y_benzene + y_toluene
        if y_total > 0:
            y_benzene = y_benzene / y_total
            y_toluene = y_toluene / y_total
        
        return {
            'liquid': {
                'benzene': x_benzene,
                'toluene': x_toluene
            },
            'vapor': {
                'benzene': y_benzene,
                'toluene': y_toluene
            }
        }
    
    def flash_calculation(self, weight_percent_benzene: float, temperature_c: float,
                         pressure_atm: float) -> Dict:
        """
        Complete flash calculation for benzene-toluene mixture.
        
        Args:
            weight_percent_benzene: Weight percentage of benzene in feed
            temperature_c: Temperature in Celsius
            pressure_atm: Pressure in atmospheres
            
        Returns:
            Dictionary containing all flash calculation results
        """
        # Convert weight percent to mole fractions
        z_benzene, z_toluene = self.weight_to_mole_fraction(weight_percent_benzene)
        
        # Calculate K-values
        k_values = self.calculate_k_values(temperature_c, pressure_atm)
        k_benzene = k_values['benzene']
        k_toluene = k_values['toluene']
        
        # Calculate vapor pressures for reference
        p_sat_benzene = self.vapor_pressure('benzene', temperature_c)
        p_sat_toluene = self.vapor_pressure('toluene', temperature_c)
        
        # Solve for vapor fraction
        psi = self.solve_vapor_fraction(z_benzene, z_toluene, k_benzene, k_toluene)
        
        # Calculate product compositions
        compositions = self.calculate_product_compositions(psi, z_benzene, z_toluene, k_benzene, k_toluene)
        
        return {
            'feed_composition': {
                'benzene_weight_percent': weight_percent_benzene,
                'toluene_weight_percent': 100 - weight_percent_benzene,
                'benzene_mole_fraction': z_benzene,
                'toluene_mole_fraction': z_toluene
            },
            'operating_conditions': {
                'temperature_c': temperature_c,
                'pressure_atm': pressure_atm,
                'pressure_mmhg': pressure_atm * 760
            },
            'vapor_pressures_mmhg': {
                'benzene': p_sat_benzene,
                'toluene': p_sat_toluene
            },
            'k_values': {
                'benzene': k_benzene,
                'toluene': k_toluene
            },
            'vapor_fraction': psi,
            'liquid_fraction': 1 - psi,
            'product_compositions': compositions,
            'liquid_flow_fraction': 1 - psi,
            'vapor_flow_fraction': psi
        }


def main():
    """
    Example usage of the flash unit calculator for the specified problem:
    50:50 weight percent benzene-toluene mixture at 60°C and 1 atm.
    """
    # Create flash unit instance
    flash_unit = BenzeneTolueneFlash()
    
    # Problem specifications
    weight_percent_benzene = 50.0  # 50:50 weight percent
    temperature_c = 60.0  # 60°C
    pressure_atm = 1.0  # 1 atm
    
    print("=" * 60)
    print("FLASH UNIT CALCULATION: BENZENE-TOLUENE MIXTURE")
    print("=" * 60)
    print(f"Feed composition: {weight_percent_benzene:.1f}% benzene, {100-weight_percent_benzene:.1f}% toluene (by weight)")
    print(f"Operating conditions: {temperature_c}°C, {pressure_atm} atm")
    print()
    
    # Perform flash calculation
    results = flash_unit.flash_calculation(weight_percent_benzene, temperature_c, pressure_atm)
    
    # Display results
    print("FEED COMPOSITION:")
    print(f"  Benzene: {results['feed_composition']['benzene_weight_percent']:.1f} wt%, "
          f"{results['feed_composition']['benzene_mole_fraction']:.4f} mol fraction")
    print(f"  Toluene: {results['feed_composition']['toluene_weight_percent']:.1f} wt%, "
          f"{results['feed_composition']['toluene_mole_fraction']:.4f} mol fraction")
    print()
    
    print("VAPOR PRESSURES at {}°C:".format(temperature_c))
    print(f"  Benzene: {results['vapor_pressures_mmhg']['benzene']:.1f} mmHg")
    print(f"  Toluene: {results['vapor_pressures_mmhg']['toluene']:.1f} mmHg")
    print()
    
    print("K-VALUES:")
    print(f"  Benzene: {results['k_values']['benzene']:.3f}")
    print(f"  Toluene: {results['k_values']['toluene']:.3f}")
    print()
    
    print("FLASH RESULTS:")
    print(f"  Vapor fraction (ψ): {results['vapor_fraction']:.4f} ({results['vapor_fraction']*100:.2f}%)")
    print(f"  Liquid fraction: {results['liquid_fraction']:.4f} ({results['liquid_fraction']*100:.2f}%)")
    print()
    
    print("PRODUCT COMPOSITIONS:")
    liquid_comp = results['product_compositions']['liquid']
    vapor_comp = results['product_compositions']['vapor']
    
    print("  Liquid phase:")
    print(f"    Benzene: {liquid_comp['benzene']:.4f} ({liquid_comp['benzene']*100:.2f}%)")
    print(f"    Toluene: {liquid_comp['toluene']:.4f} ({liquid_comp['toluene']*100:.2f}%)")
    
    print("  Vapor phase:")
    print(f"    Benzene: {vapor_comp['benzene']:.4f} ({vapor_comp['benzene']*100:.2f}%)")
    print(f"    Toluene: {vapor_comp['toluene']:.4f} ({vapor_comp['toluene']*100:.2f}%)")
    print()
    
    # Verification - check material balance
    z_benzene = results['feed_composition']['benzene_mole_fraction']
    psi = results['vapor_fraction']
    x_benzene = liquid_comp['benzene']
    y_benzene = vapor_comp['benzene']
    
    material_balance_check = psi * y_benzene + (1 - psi) * x_benzene
    print("MATERIAL BALANCE VERIFICATION:")
    print(f"  Feed benzene fraction: {z_benzene:.6f}")
    print(f"  Calculated from products: {material_balance_check:.6f}")
    print(f"  Difference: {abs(z_benzene - material_balance_check):.8f}")
    
    if abs(z_benzene - material_balance_check) < 1e-6:
        print("  ✓ Material balance satisfied")
    else:
        print("  ✗ Material balance error")


if __name__ == "__main__":
    main()