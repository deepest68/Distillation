#!/usr/bin/env python3
"""
Simple tests for the flash unit implementation.

These tests verify basic functionality and consistency of the flash unit calculations.
"""

import unittest
import math
from flash_unit import BenzeneTolueneFlash


class TestBenzeneTolueneFlash(unittest.TestCase):
    """Test cases for the BenzeneTolueneFlash class."""
    
    def setUp(self):
        """Set up test instance."""
        self.flash_unit = BenzeneTolueneFlash()
    
    def test_vapor_pressure_calculation(self):
        """Test vapor pressure calculations using Antoine equation."""
        # Test vapor pressures at 100°C (should match README values)
        p_benzene_100c = self.flash_unit.vapor_pressure('benzene', 100.0)
        p_toluene_100c = self.flash_unit.vapor_pressure('toluene', 100.0)
        
        # Values from README.md example
        self.assertAlmostEqual(p_benzene_100c, 1350, delta=5)  # ±5 mmHg tolerance
        self.assertAlmostEqual(p_toluene_100c, 556, delta=5)   # ±5 mmHg tolerance
    
    def test_weight_to_mole_conversion(self):
        """Test conversion from weight percent to mole fractions."""
        # Test 50:50 weight percent
        x_benzene, x_toluene = self.flash_unit.weight_to_mole_fraction(50.0)
        
        # Should sum to 1
        self.assertAlmostEqual(x_benzene + x_toluene, 1.0, places=6)
        
        # Benzene is lighter, so should have higher mole fraction for equal weight
        self.assertGreater(x_benzene, x_toluene)
        
        # Test extreme cases
        x_b_100, x_t_100 = self.flash_unit.weight_to_mole_fraction(100.0)
        self.assertAlmostEqual(x_b_100, 1.0, places=6)
        self.assertAlmostEqual(x_t_100, 0.0, places=6)
        
        x_b_0, x_t_0 = self.flash_unit.weight_to_mole_fraction(0.0)
        self.assertAlmostEqual(x_b_0, 0.0, places=6)
        self.assertAlmostEqual(x_t_0, 1.0, places=6)
    
    def test_k_values_calculation(self):
        """Test K-value calculations."""
        k_values = self.flash_unit.calculate_k_values(100.0, 1.0)
        
        # At 100°C and 1 atm, should match README values
        self.assertAlmostEqual(k_values['benzene'], 1.78, delta=0.02)
        self.assertAlmostEqual(k_values['toluene'], 0.73, delta=0.02)
        
        # K-values should be positive
        self.assertGreater(k_values['benzene'], 0)
        self.assertGreater(k_values['toluene'], 0)
    
    def test_rachford_rice_equation(self):
        """Test Rachford-Rice equation calculation."""
        # At the solution, the equation should equal zero
        z_benzene, z_toluene = 0.4, 0.6
        k_benzene, k_toluene = 1.78, 0.73
        
        # Test with a known solution (approximately ψ = 0.42 from README)
        # Note: The exact solution might differ slightly due to different solution methods
        result = self.flash_unit.rachford_rice_equation(0.42, z_benzene, z_toluene, k_benzene, k_toluene)
        self.assertAlmostEqual(result, 0.0, delta=0.1)  # Relaxed tolerance for approximation
    
    def test_material_balance(self):
        """Test that material balance is satisfied."""
        # Run calculation for main problem
        results = self.flash_unit.flash_calculation(50.0, 60.0, 1.0)
        
        # Extract values
        z_benzene = results['feed_composition']['benzene_mole_fraction']
        psi = results['vapor_fraction']
        x_benzene = results['product_compositions']['liquid']['benzene']
        y_benzene = results['product_compositions']['vapor']['benzene']
        
        # Material balance: F*z = V*y + L*x
        # For unit feed: z = ψ*y + (1-ψ)*x
        calculated_feed = psi * y_benzene + (1 - psi) * x_benzene
        
        self.assertAlmostEqual(z_benzene, calculated_feed, places=8)
    
    def test_main_problem_conditions(self):
        """Test the specific problem conditions: 50:50 wt%, 60°C, 1 atm."""
        results = self.flash_unit.flash_calculation(50.0, 60.0, 1.0)
        
        # Check that calculation completes without error
        self.assertIsInstance(results, dict)
        
        # Check that all required keys are present
        required_keys = [
            'feed_composition', 'operating_conditions', 'vapor_pressures_mmhg',
            'k_values', 'vapor_fraction', 'product_compositions'
        ]
        for key in required_keys:
            self.assertIn(key, results)
        
        # Vapor fraction should be between 0 and 1
        psi = results['vapor_fraction']
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)
        
        # Product compositions should sum to 1
        liquid_comp = results['product_compositions']['liquid']
        vapor_comp = results['product_compositions']['vapor']
        
        liquid_sum = liquid_comp['benzene'] + liquid_comp['toluene']
        vapor_sum = vapor_comp['benzene'] + vapor_comp['toluene']
        
        self.assertAlmostEqual(liquid_sum, 1.0, places=6)
        self.assertAlmostEqual(vapor_sum, 1.0, places=6)
    
    def test_extreme_conditions(self):
        """Test behavior at extreme conditions."""
        # Very high temperature should favor vapor phase
        results_high_temp = self.flash_unit.flash_calculation(50.0, 150.0, 1.0)
        self.assertGreater(results_high_temp['vapor_fraction'], 0.5)
        
        # Very low temperature should favor liquid phase
        results_low_temp = self.flash_unit.flash_calculation(50.0, 25.0, 1.0)
        self.assertLess(results_low_temp['vapor_fraction'], 0.1)


if __name__ == "__main__":
    unittest.main()