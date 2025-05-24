"""
Unit Tests for Quadratic Equation Solver
========================================

This module contains comprehensive tests to validate the functionality
of the quadratic equation solver with Catalan numbers.

Execution: python -m pytest test_quadratic_solver.py -v
"""

import pytest
import math
from typing import List

from quadratic_catalan_solver import CatalanSolver, QuadraticEquation

# Import classes from main module
# from quadratic_solver import QuadraticEquation, CatalanSolver, Solution


class TestCatalanNumber:
    """Test Catalan number calculations"""
    
    def test_catalan_base_cases(self):
        """Test base cases of Catalan numbers"""
        # First known numbers: 1, 1, 2, 5, 14, 42, 132, 429
        expected = [1, 1, 2, 5, 14, 42, 132, 429]
        
        for n, expected_value in enumerate(expected):
            actual = CatalanSolver.catalan_number(n)
            assert actual == expected_value, f"C({n}) should be {expected_value}, but was {actual}"
    
    def test_catalan_larger_values(self):
        """Test larger values of Catalan numbers"""
        # C(10) = 16796
        assert CatalanSolver.catalan_number(10) == 16796
        
        # C(15) = 9694845 
        assert CatalanSolver.catalan_number(15) == 9694845


class TestQuadraticEquation:
    """Test QuadraticEquation class"""
    
    def test_equation_creation(self):
        """Test equation creation"""
        eq = QuadraticEquation(1, -2, 1)
        assert eq.a == 1
        assert eq.b == -2  
        assert eq.c == 1
    
    def test_equation_string_representation(self):
        """Test string representation of equation"""
        eq = QuadraticEquation(2, -3, 1)
        expected = "2x² + -3x + 1 = 0"
        assert str(eq) == expected


class TestCatalanSolver:
    """Test the main solver"""
    
    @pytest.fixture
    def solver(self):
        """Fixture that creates a default solver"""
        return CatalanSolver(tolerance=1e-10)
    
    def test_solver_initialization(self):
        """Test solver initialization"""
        solver = CatalanSolver(tolerance=1e-8)
        assert solver.tolerance == 1e-8
        
        # Test default values
        default_solver = CatalanSolver()
        assert default_solver.tolerance == CatalanSolver.DEFAULT_TOLERANCE
    
    def test_is_zero_method(self, solver):
        """Test zero value detection"""
        assert solver._is_zero(0.0)
        assert solver._is_zero(1e-16)
        assert not solver._is_zero(1e-10)
        assert not solver._is_zero(0.1)
    
    def test_linear_equations(self, solver):
        """Test linear equation solving"""
        # 3x + 6 = 0 → x = -2
        eq = QuadraticEquation(0, 3, 6)
        solution = solver.solve(eq)
        
        assert len(solution.roots) == 1
        assert abs(solution.roots[0] - (-2.0)) < 1e-10
        assert solution.method_used == "Linear"
    
    def test_missing_c_case(self, solver):
        """Test equations with c = 0"""
        # x² + 2x = 0 → x = 0 or x = -2
        eq = QuadraticEquation(1, 2, 0)
        solution = solver.solve(eq)
        
        assert len(solution.roots) == 2
        roots_set = set(solution.roots)
        expected_set = {0.0, -2.0}
        
        for root in solution.roots:
            assert any(abs(root - expected) < 1e-10 for expected in expected_set)
    
    def test_missing_b_case(self, solver):
        """Test equations with b = 0"""
        # x² - 4 = 0 → x = ±2
        eq = QuadraticEquation(1, 0, -4)
        solution = solver.solve(eq)
        
        assert len(solution.roots) == 2
        roots_sorted = sorted(solution.roots)
        assert abs(roots_sorted[0] - (-2.0)) < 1e-10
        assert abs(roots_sorted[1] - 2.0) < 1e-10
    
    def test_catalan_method_favorable_case(self, solver):
        """Test Catalan method in favorable case"""
        # x² + 4x + 1 = 0
        # A = (1×1)/(4²) = 1/16 = 0.0625 ≤ 0.25
        eq = QuadraticEquation(1, 4, 1)
        solution = solver.solve(eq)
        
        assert len(solution.roots) == 2
        assert solution.method_used == "Catalan series"
        assert solution.terms_used is not None
        assert solution.error is not None
        assert solution.error < solver.tolerance
        
        # Check if roots are approximately correct
        # Using quadratic formula for comparison
        expected_roots = self._quadratic_formula(1, 4, 1)
        for actual_root in solution.roots:
            assert any(abs(actual_root - expected) < 1e-8 
                      for expected in expected_roots)
    
    def test_catalan_method_unfavorable_case(self, solver):
        """Test when Catalan method doesn't apply"""
        # x² + 2x + 2 = 0
        # A = (1×2)/(2²) = 0.5 > 0.25
        eq = QuadraticEquation(1, 2, 2)
        solution = solver.solve(eq)
        
        # Should use standard quadratic formula
        assert solution.method_used == "Quadratic formula"
        # Should have no real roots
        assert len(solution.roots) == 0
    
    def test_perfect_square(self, solver):
        """Test equation with zero discriminant"""
        # x² - 4x + 4 = 0 → (x-2)² = 0 → x = 2 (double)
        eq = QuadraticEquation(1, -4, 4)
        solution = solver.solve(eq)
        
        assert len(solution.roots) == 2
        assert abs(solution.roots[0] - 2.0) < 1e-10
        assert abs(solution.roots[1] - 2.0) < 1e-10
    
    def test_no_real_roots(self, solver):
        """Test equation with no real roots"""
        # x² + x + 1 = 0 (discriminant < 0)
        eq = QuadraticEquation(1, 1, 1)
        solution = solver.solve(eq)
        
        assert len(solution.roots) == 0
    
    def _quadratic_formula(self, a: float, b: float, c: float) -> List[float]:
        """Helper method to calculate roots using quadratic formula"""
        discriminant = b**2 - 4*a*c
        
        if discriminant < 0:
            return []
        
        sqrt_disc = math.sqrt(discriminant)
        root1 = (-b + sqrt_disc) / (2*a)
        root2 = (-b - sqrt_disc) / (2*a)
        
        return [root1, root2]


class TestIntegration:
    """Integration tests for the complete system"""
    
    def test_solution_verification(self):
        """Test if found solutions actually satisfy the equation"""
        solver = CatalanSolver()
        test_cases = [
            QuadraticEquation(1, 4, 1),    # Catalan case
            QuadraticEquation(2, -7, 3),   # Standard case
            QuadraticEquation(1, 0, -9),   # b = 0
            QuadraticEquation(3, 12, 0),   # c = 0
        ]
        
        for eq in test_cases:
            solution = solver.solve(eq)
            
            for root in solution.roots:
                # Substitute in original equation
                result = eq.a * root**2 + eq.b * root + eq.c
                
                # Check if result is close to zero
                assert abs(result) < 1e-8, f"Root {root} doesn't satisfy {eq}"
    
    def test_catalan_convergence_properties(self):
        """Test convergence properties of Catalan series"""
        solver = CatalanSolver(tolerance=1e-12)
        
        # Cases with different A values
        test_equations = [
            QuadraticEquation(1, 8, 1),     # A = 1/64 ≈ 0.0156
            QuadraticEquation(1, 4, 1),     # A = 1/16 = 0.0625  
            QuadraticEquation(4, 8, 1),     # A = 1/16 = 0.0625
            QuadraticEquation(1, 2, 0.24),  # A ≈ 0.24 (close to limit)
        ]
        
        for eq in test_equations:
            A = (eq.a * eq.c) / (eq.b**2)
            
            if abs(A) <= 0.25:
                solution = solver.solve(eq)
                
                # Should use Catalan method
                assert solution.method_used == "Catalan series"
                
                # Faster convergence for smaller A
                if abs(A) < 0.1:
                    assert solution.terms_used <= 10
                
                # Error should be within tolerance
                assert solution.error < solver.tolerance


class TestEdgeCases:
    """Test extreme cases and special situations"""
    
    def test_very_small_coefficients(self):
        """Test very small coefficients"""
        solver = CatalanSolver()
        
        # Coefficients close to zero
        eq = QuadraticEquation(1e-14, 1, 1)
        solution = solver.solve(eq)
        
        # Should be treated as linear equation
        assert solution.method_used == "Linear"
    
    def test_very_large_coefficients(self):
        """Test very large coefficients"""
        solver = CatalanSolver()
        
        eq = QuadraticEquation(1e6, 2e6, 1e6)
        solution = solver.solve(eq)
        
        # Should find valid solution
        assert len(solution.roots) <= 2
        
        # Check roots if they exist
        for root in solution.roots:
            result = eq.a * root**2 + eq.b * root + eq.c
            relative_error = abs(result) / max(abs(eq.a), abs(eq.b), abs(eq.c))
            assert relative_error < 1e-10
    
    def test_tolerance_settings(self):
        """Test different tolerance settings"""
        tolerances = [1e-6, 1e-10, 1e-14]
        eq = QuadraticEquation(1, 4, 1)  # Favorable case for Catalan
        
        for tol in tolerances:
            solver = CatalanSolver(tolerance=tol)
            solution = solver.solve(eq)
            
            if solution.method_used == "Catalan series":
                assert solution.error <= tol * 10  # Tolerance margin


# Function to run all tests
def run_all_tests():
    """Run all tests and report results"""
    import time
    
    print("RUNNING QUADRATIC SOLVER TESTS")
    print("=" * 50)
    
    start_time = time.time()
    
    # List of test classes
    test_classes = [
        TestCatalanNumber,
        TestQuadraticEquation, 
        TestCatalanSolver,
        TestIntegration,
        TestEdgeCases
    ]
    
    total_tests = 0
    passed_tests = 0
    
    for test_class in test_classes:
        print(f"\n{test_class.__name__}:")
        print("-" * 30)
        
        # Instantiate test class
        test_instance = test_class()
        
        # Execute test methods
        test_methods = [method for method in dir(test_instance) 
                       if method.startswith('test_')]
        
        for method_name in test_methods:
            total_tests += 1
            
            try:
                # Execute test
                test_method = getattr(test_instance, method_name)
                
                # Inject dependencies if needed
                if hasattr(test_instance, 'solver') and method_name != 'solver':
                    test_method(CatalanSolver())
                else:
                    test_method()
                
                print(f"  ✓ {method_name}")
                passed_tests += 1
                
            except Exception as e:
                print(f"  ✗ {method_name}: {str(e)}")
    
    elapsed_time = time.time() - start_time
    
    print(f"\n{'='*50}")
    print(f"RESULTS: {passed_tests}/{total_tests} tests passed")
    print(f"Execution time: {elapsed_time:.2f}s")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed!")
    else:
        print(f"⚠️  {total_tests - passed_tests} tests failed")


if __name__ == "__main__":
    run_all_tests()