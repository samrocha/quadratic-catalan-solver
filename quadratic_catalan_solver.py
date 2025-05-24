"""
Quadratic Equation Solver using Catalan Numbers
==============================================

This module implements an alternative method for solving second-degree equations
ax² + bx + c = 0 using Catalan number series when |A| ≤ 1/4, where A = ac/b².

Author: Claude AI System
Date: May 2025
"""

import math
from typing import Tuple, Optional, List
from dataclasses import dataclass


@dataclass
class QuadraticEquation:
    """Represents a quadratic equation ax² + bx + c = 0"""
    a: float
    b: float 
    c: float
    
    def __str__(self) -> str:
        return f"{self.a}x² + {self.b}x + {self.c} = 0"


@dataclass
class Solution:
    """Stores the solution results"""
    roots: List[float]
    method_used: str
    terms_used: Optional[int] = None
    error: Optional[float] = None


class CatalanSolver:
    """Quadratic equation solver using Catalan numbers"""
    
    # Configuration constants
    DEFAULT_TOLERANCE = 1e-10
    MAX_TERMS = 100
    ZERO_THRESHOLD = 1e-15
    CATALAN_THRESHOLD = 0.25
    
    def __init__(self, tolerance: float = DEFAULT_TOLERANCE):
        """
        Initialize the solver
        
        Args:
            tolerance: Desired precision for series convergence
        """
        self.tolerance = tolerance
    
    @staticmethod
    def catalan_number(n: int) -> int:
        """
        Calculate the nth Catalan number using optimized formula
        
        Args:
            n: Catalan number index (n >= 0)
            
        Returns:
            The nth Catalan number
            
        Formula: C(n) = (2n)! / ((n+1)! * n!)
        """
        if n == 0:
            return 1
        
        # Efficient calculation avoiding overflow
        result = 1
        for i in range(n):
            result = result * (2 * n - i) // (i + 1)
        
        return result // (n + 1)
    
    def _is_zero(self, value: float) -> bool:
        """Check if a value is numerically zero"""
        return abs(value) < self.ZERO_THRESHOLD
    
    def _solve_linear(self, equation: QuadraticEquation) -> Solution:
        """Solve linear equation bx + c = 0"""
        if self._is_zero(equation.b):
            # Case 0x + c = 0
            if self._is_zero(equation.c):
                return Solution([], "Infinite solutions")
            else:
                return Solution([], "No solution")
        
        root = -equation.c / equation.b
        return Solution([root], "Linear")
    
    def _solve_missing_c(self, equation: QuadraticEquation) -> Solution:
        """Solve ax² + bx = 0 (c = 0)"""
        root1 = 0.0
        root2 = -equation.b / equation.a
        return Solution([root1, root2], "Factorization (c=0)")
    
    def _solve_missing_b(self, equation: QuadraticEquation) -> Solution:
        """Solve ax² + c = 0 (b = 0)"""
        discriminant = -equation.c / equation.a
        
        if discriminant < 0:
            return Solution([], "No real solutions")
        
        sqrt_disc = math.sqrt(discriminant)
        return Solution([sqrt_disc, -sqrt_disc], "Direct root (b=0)")
    
    def _solve_standard_formula(self, equation: QuadraticEquation) -> Solution:
        """Solve using standard quadratic formula"""
        discriminant = equation.b**2 - 4*equation.a*equation.c
        
        if discriminant < 0:
            return Solution([], "No real solutions")
        
        sqrt_disc = math.sqrt(discriminant)
        denominator = 2 * equation.a
        
        root1 = (-equation.b + sqrt_disc) / denominator
        root2 = (-equation.b - sqrt_disc) / denominator
        
        return Solution([root1, root2], "Quadratic formula")
    
    def _compute_catalan_parameter(self, equation: QuadraticEquation) -> float:
        """Calculate parameter A = ac/b² for Catalan method"""
        return (equation.a * equation.c) / (equation.b**2)
    
    def _compute_exact_u(self, A: float) -> float:
        """Calculate exact solution u = (1 - √(1-4A))/(2A)"""
        if self._is_zero(A):
            return 1.0  # Limit when A → 0
        
        discriminant = 1 - 4*A
        if discriminant < 0:
            raise ValueError("Negative discriminant in transformation")
        
        return (1 - math.sqrt(discriminant)) / (2*A)
    
    def _compute_catalan_series(self, A: float, u_exact: float) -> Tuple[float, int]:
        """
        Calculate Catalan series until convergence
        
        Returns:
            Tuple with (series value, number of terms used)
        """
        u_series = 0.0
        n = 0
        
        while n < self.MAX_TERMS:
            # Calculate current term: C(n) * A^n
            catalan_n = self.catalan_number(n)
            term = catalan_n * (A ** n)
            u_series += term
            
            # Check convergence
            error = abs(u_series - u_exact)
            if error < self.tolerance:
                return u_series, n + 1
            
            n += 1
        
        # If doesn't converge, return best approximation
        return u_series, self.MAX_TERMS
    
    def _solve_catalan_method(self, equation: QuadraticEquation) -> Solution:
        """Solve using Catalan numbers method"""
        # Calculate parameter A
        A = self._compute_catalan_parameter(equation)
        
        # Check if method is applicable
        if abs(A) > self.CATALAN_THRESHOLD:
            return self._solve_standard_formula(equation)
        
        try:
            # Calculate exact solution for comparison
            u_exact = self._compute_exact_u(A)
            
            # Approximate by Catalan series
            u_series, terms_used = self._compute_catalan_series(A, u_exact)
            
            # Convert back to x: x = -(c/b) * u
            x1 = -(equation.c / equation.b) * u_series
            
            # Second root by Vieta's relation: x₁*x₂ = c/a
            x2 = equation.c / (equation.a * x1)
            
            # Calculate final error
            final_error = abs(u_series - u_exact)
            
            return Solution(
                roots=[x1, x2],
                method_used="Catalan series",
                terms_used=terms_used,
                error=final_error
            )
            
        except ValueError:
            # If fails, use standard method
            return self._solve_standard_formula(equation)
    
    def solve(self, equation: QuadraticEquation, verbose: bool = False) -> Solution:
        """
        Solve quadratic equation using the most appropriate method
        
        Args:
            equation: Equation to be solved
            verbose: If True, prints process details
            
        Returns:
            Solution object with roots and metadata
        """
        if verbose:
            print(f"Solving: {equation}")
            print("-" * 50)
        
        # Case 1: Linear equation (a ≈ 0)
        if self._is_zero(equation.a):
            solution = self._solve_linear(equation)
        
        # Case 2: c ≈ 0 (one root is zero)
        elif self._is_zero(equation.c):
            solution = self._solve_missing_c(equation)
        
        # Case 3: b ≈ 0 (no linear term)
        elif self._is_zero(equation.b):
            solution = self._solve_missing_b(equation)
        
        # Case 4: Complete quadratic equation
        else:
            A = self._compute_catalan_parameter(equation)
            
            if abs(A) <= self.CATALAN_THRESHOLD:
                solution = self._solve_catalan_method(equation)
            else:
                solution = self._solve_standard_formula(equation)
        
        if verbose:
            self._print_solution_details(equation, solution)
        
        return solution
    
    def _print_solution_details(self, equation: QuadraticEquation, solution: Solution):
        """Print details of the found solution"""
        print(f"Method used: {solution.method_used}")
        
        if solution.roots:
            print(f"Roots found: {len(solution.roots)}")
            for i, root in enumerate(solution.roots, 1):
                print(f"  x{i} = {root:.8f}")
                
                # Solution verification
                verification = (equation.a * root**2 + 
                              equation.b * root + 
                              equation.c)
                print(f"       Verification: {verification:.2e}")
        else:
            print("No real roots found")
        
        if solution.terms_used:
            print(f"Series terms used: {solution.terms_used}")
        
        if solution.error:
            print(f"Approximation error: {solution.error:.2e}")


def demonstrate_solver():
    """Demonstrate the solver usage with different examples"""
    print("QUADRATIC EQUATION SOLVER DEMONSTRATION")
    print("=" * 60)
    
    # Initialize solver
    solver = CatalanSolver(tolerance=1e-10)
    
    # Test cases
    test_cases = [
        QuadraticEquation(1, 4, 1),      # Favorable for Catalan
        QuadraticEquation(2, 6, 1),      # Another favorable case  
        QuadraticEquation(1, 2, 2),      # |A| > 1/4, uses standard formula
        QuadraticEquation(1, 0, -4),     # b = 0
        QuadraticEquation(1, 5, 0),      # c = 0
        QuadraticEquation(0, 3, -6),     # Linear
    ]
    
    for i, equation in enumerate(test_cases, 1):
        print(f"\nEXAMPLE {i}:")
        solution = solver.solve(equation, verbose=True)
        print()


def show_catalan_sequence():
    """Show the first Catalan numbers"""
    print("CATALAN NUMBERS SEQUENCE")
    print("=" * 40)
    print("n  | C(n)  | Example application")
    print("-" * 40)
    
    applications = [
        "Trivial way to parenthesize",
        "Single way: (ab)",  
        "Two ways: ((ab)c), (a(bc))",
        "Five ways to parenthesize abcd",
        "Paths in 4×4 grid",
        "Binary trees with 6 leaves",
        "Heptagon triangulations",
        "Well-parenthesized expressions"
    ]
    
    for n in range(8):
        catalan_n = CatalanSolver.catalan_number(n)
        app = applications[n] if n < len(applications) else "..."
        print(f"{n:2d} | {catalan_n:4d}  | {app}")


# Main entry point
if __name__ == "__main__":
    show_catalan_sequence()
    print("\n")
    demonstrate_solver()