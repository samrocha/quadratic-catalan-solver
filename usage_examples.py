"""
Usage Examples for Quadratic Equation Solver
===========================================

This file demonstrates how to use the quadratic equation solver
with Catalan numbers efficiently and following best practices.

Author: Claude AI System
Date: May 2025
"""

import sys
from typing import List
import matplotlib.pyplot as plt
import numpy as np

# Import classes from main module (uncomment when using)
# from quadratic_solver import QuadraticEquation, CatalanSolver, Solution


def basic_usage_example():
    """Basic usage example of the solver"""
    print("EXAMPLE 1: Basic Usage")
    print("-" * 30)
    
    # Create solver with default tolerance
    solver = CatalanSolver()
    
    # Solve equation x² + 4x + 1 = 0
    equation = QuadraticEquation(a=1, b=4, c=1)
    solution = solver.solve(equation, verbose=True)
    
    # Access results
    if solution.roots:
        print(f"Number of roots: {len(solution.roots)}")
        print(f"Roots: {solution.roots}")
        print(f"Method used: {solution.method_used}")
        
        if solution.terms_used:
            print(f"Series terms: {solution.terms_used}")


def batch_solving_example():
    """Example of batch solving multiple equations"""
    print("\nEXAMPLE 2: Batch Solving")
    print("-" * 35)
    
    solver = CatalanSolver(tolerance=1e-12)
    
    # List of equations to solve
    equations = [
        ("x² + 4x + 1 = 0", QuadraticEquation(1, 4, 1)),
        ("2x² + 6x + 1 = 0", QuadraticEquation(2, 6, 1)),
        ("x² + 2x + 2 = 0", QuadraticEquation(1, 2, 2)),
        ("x² - 5x + 6 = 0", QuadraticEquation(1, -5, 6)),
        ("3x + 9 = 0", QuadraticEquation(0, 3, 9)),
    ]
    
    results = []
    
    for description, eq in equations:
        print(f"\nSolving: {description}")
        solution = solver.solve(eq)
        
        results.append({
            'equation': description,
            'method': solution.method_used,
            'roots': solution.roots,
            'terms_used': solution.terms_used
        })
        
        # Solution summary
        if solution.roots:
            roots_str = ", ".join(f"{root:.6f}" for root in solution.roots)
            print(f"  Roots: {roots_str}")
        else:
            print("  No real roots")
        
        print(f"  Method: {solution.method_used}")
    
    return results


def convergence_analysis_example():
    """Example of Catalan series convergence analysis"""
    print("\nEXAMPLE 3: Convergence Analysis")
    print("-" * 40)
    
    # Different tolerances for comparison
    tolerances = [1e-4, 1e-8, 1e-12]
    equation = QuadraticEquation(1, 6, 1)  # A = 1/36 ≈ 0.028
    
    print(f"Equation: {equation}")
    print(f"A = ac/b² = {(equation.a * equation.c) / (equation.b**2):.6f}")
    print()
    
    for tol in tolerances:
        solver = CatalanSolver(tolerance=tol)
        solution = solver.solve(equation)
        
        if solution.method_used == "Catalan series":
            print(f"Tolerance: {tol:.0e}")
            print(f"  Terms used: {solution.terms_used}")
            print(f"  Final error: {solution.error:.2e}")
            print(f"  Main root: {solution.roots[0]:.10f}")
        else:
            print(f"Tolerance {tol}: Standard method used")


def performance_comparison_example():
    """Example of performance comparison between methods"""
    print("\nEXAMPLE 4: Performance Comparison")
    print("-" * 42)
    
    import time
    
    # Equations favorable to Catalan method
    catalan_favorable = [
        QuadraticEquation(1, 8, 1),    # A = 1/64
        QuadraticEquation(1, 6, 1),    # A = 1/36
        QuadraticEquation(2, 10, 1),   # A = 1/50
        QuadraticEquation(1, 4, 0.5),  # A = 1/32
    ]
    
    solver_catalan = CatalanSolver()
    num_iterations = 1000
    
    print(f"Solving {len(catalan_favorable)} equations {num_iterations} times each...")
    
    # Test with Catalan method
    start_time = time.time()
    for _ in range(num_iterations):
        for eq in catalan_favorable:
            solution = solver_catalan.solve(eq)
    catalan_time = time.time() - start_time
    
    print(f"Catalan method time: {catalan_time:.4f}s")
    print(f"Average time per equation: {(catalan_time / (len(catalan_favorable) * num_iterations) * 1000):.2f}ms")


def error_handling_example():
    """Example of error handling and special cases"""
    print("\nEXAMPLE 5: Special Cases Handling")
    print("-" * 45)
    
    solver = CatalanSolver()
    
    # Special cases
    special_cases = [
        ("Impossible equation", QuadraticEquation(0, 0, 5)),
        ("Identity", QuadraticEquation(0, 0, 0)),
        ("Very small coefficients", QuadraticEquation(1e-16, 1, 1)),
        ("Negative discriminant", QuadraticEquation(1, 1, 1)),
        ("Double root", QuadraticEquation(1, -4, 4)),
    ]
    
    for description, eq in special_cases:
        print(f"\n{description}: {eq}")
        
        try:
            solution = solver.solve(eq)
            
            if solution.roots:
                print(f"  Roots: {[f'{r:.6f}' for r in solution.roots]}")
            else:
                print(f"  Result: {solution.method_used}")
                
        except Exception as e:
            print(f"  Error: {e}")


def visualization_example():
    """Example of results visualization"""
    print("\nEXAMPLE 6: Results Visualization")
    print("-" * 40)
    
    # Equation to visualize: x² + 4x + 1 = 0
    eq = QuadraticEquation(1, 4, 1)
    solver = CatalanSolver()
    solution = solver.solve(eq, verbose=True)
    
    if not solution.roots:
        print("No real roots to visualize.")
        return
    
    # Prepare data for plot
    x_vals = np.linspace(-6, 2, 1000)
    y_vals = eq.a * x_vals**2 + eq.b * x_vals + eq.c
    
    # Create plot
    plt.figure(figsize=(10, 6))
    
    # Plot parabola
    plt.plot(x_vals, y_vals, 'b-', linewidth=2, label=f'{eq.a}x² + {eq.b}x + {eq.c}')
    
    # Mark roots
    for i, root in enumerate(solution.roots):
        plt.plot(root, 0, 'ro', markersize=8, label=f'x_{i+1} = {root:.4f}')
    
    # Mark axes
    plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    plt.axvline(x=0, color='k', linestyle='-', alpha=0.3)
    
    # Configure plot
    plt.grid(True, alpha=0.3)
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title(f'Plot of equation {eq}\nMethod used: {solution.method_used}')
    plt.legend()
    
    # Adjust y-axis limits
    y_min, y_max = min(y_vals), max(y_vals)
    margin = (y_max - y_min) * 0.1
    plt.ylim(y_min - margin, y_max + margin)
    
    plt.tight_layout()
    
    # Save or show
    try:
        plt.savefig('quadratic_equation_plot.png', dpi=300, bbox_inches='tight')
        print("Plot saved as 'quadratic_equation_plot.png'")
    except:
        print("Could not save plot")
    
    plt.show()


def catalan_series_visualization():
    """Visualize Catalan series convergence"""
    print("\nEXAMPLE 7: Catalan Convergence Visualization")
    print("-" * 52)
    
    # Parameters for equation x² + 4x + 1 = 0
    A = 1/16  # ac/b² = (1*1)/(4²)
    solver = CatalanSolver()
    
    # Calculate series terms
    terms = []
    partial_sums = []
    catalan_numbers = []
    
    partial_sum = 0
    for n in range(15):
        catalan_n = solver.catalan_number(n)
        term = catalan_n * (A ** n)
        partial_sum += term
        
        terms.append(term)
        partial_sums.append(partial_sum)
        catalan_numbers.append(catalan_n)
    
    # Exact solution for comparison
    u_exact = (1 - np.sqrt(1 - 4*A)) / (2*A)
    
    # Create plots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    
    # Plot 1: Catalan numbers
    ax1.bar(range(len(catalan_numbers)), catalan_numbers, alpha=0.7, color='skyblue')
    ax1.set_xlabel('n')
    ax1.set_ylabel('C(n)')
    ax1.set_title('Catalan Numbers')
    ax1.set_yscale('log')
    
    # Plot 2: Series terms
    ax2.bar(range(len(terms)), terms, alpha=0.7, color='lightgreen')
    ax2.set_xlabel('n')
    ax2.set_ylabel('C(n) × A^n')
    ax2.set_title('Series Terms')
    ax2.set_yscale('log')
    
    # Plot 3: Convergence
    ax3.plot(partial_sums, 'bo-', markersize=4, label='Catalan Series')
    ax3.axhline(y=u_exact, color='r', linestyle='--', label=f'Exact value: {u_exact:.6f}')
    ax3.set_xlabel('Number of terms')
    ax3.set_ylabel('Partial sum')
    ax3.set_title('Series Convergence')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Approximation error
    errors = [abs(ps - u_exact) for ps in partial_sums]
    ax4.semilogy(errors, 'ro-', markersize=4)
    ax4.set_xlabel('Number of terms')
    ax4.set_ylabel('Absolute error')
    ax4.set_title('Approximation Error')
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    try:
        plt.savefig('catalan_convergence.png', dpi=300, bbox_inches='tight')
        print("Convergence plot saved as 'catalan_convergence.png'")
    except:
        print("Could not save plot")
    
    plt.show()
    
    # Show data numerically
    print("\nConvergence Data:")
    print("n  | C(n) | Term     | Sum      | Error")
    print("-" * 40)
    for i in range(min(10, len(terms))):
        print(f"{i:2d} | {catalan_numbers[i]:4d} | {terms[i]:.6f} | {partial_sums[i]:.6f} | {errors[i]:.2e}")


def advanced_analysis_example():
    """Advanced analysis example with multiple parameters"""
    print("\nEXAMPLE 8: Advanced Analysis")
    print("-" * 40)
    
    solver = CatalanSolver()
    
    # Analyze how A parameter affects convergence
    test_equations = [
        (QuadraticEquation(1, 16, 1), "A = 1/256 ≈ 0.004"),
        (QuadraticEquation(1, 8, 1), "A = 1/64 ≈ 0.016"),
        (QuadraticEquation(1, 4, 1), "A = 1/16 = 0.0625"),
        (QuadraticEquation(1, 2.5, 1), "A = 1/6.25 = 0.16"),
        (QuadraticEquation(1, 2, 1), "A = 1/4 = 0.25"),
    ]
    
    print("Analysis of convergence vs. parameter A:")
    print("Equation               | A value | Terms | Error     | Method")
    print("-" * 65)
    
    for eq, description in test_equations:
        A = (eq.a * eq.c) / (eq.b**2)
        solution = solver.solve(eq)
        
        method_short = "Catalan" if solution.method_used == "Catalan series" else "Standard"
        terms_str = str(solution.terms_used) if solution.terms_used else "N/A"
        error_str = f"{solution.error:.2e}" if solution.error else "N/A"
        
        print(f"{str(eq):22s} | {A:7.4f} | {terms_str:5s} | {error_str:9s} | {method_short}")


def educational_example():
    """Educational example showing mathematical connections"""
    print("\nEXAMPLE 9: Educational Insights")
    print("-" * 40)
    
    print("Mathematical connections demonstrated by this solver:")
    print()
    
    # Show Catalan numbers in different contexts
    print("1. CATALAN NUMBERS IN COMBINATORICS:")
    solver = CatalanSolver()
    
    contexts = [
        ("Ways to parenthesize n+1 factors", "((ab)c) vs (a(bc))"),
        ("Binary tree structures", "Different tree topologies"),
        ("Dyck paths", "Lattice paths not crossing diagonal"),
        ("Triangulations", "Ways to divide polygons"),
        ("Now: Quadratic equations!", "Series expansion method")
    ]
    
    print("n | C(n) | Context")
    print("-" * 40)
    for n in range(5):
        cn = solver.catalan_number(n)
        context = contexts[n] if n < len(contexts) else ("More applications...", "")
        print(f"{n} | {cn:4d} | {context[0]}")
    
    print("\n2. MATHEMATICAL TRANSFORMATION:")
    eq = QuadraticEquation(1, 4, 1)
    A = (eq.a * eq.c) / (eq.b**2)
    
    print(f"Original equation: {eq}")
    print(f"Parameter A = ac/b² = {A}")
    print(f"Variable change: u = -(b/c)x = -4x")
    print(f"Transformed: 1 - u + Au² = 0")
    print(f"Series solution: u = Σ C(n)A^n")
    print()
    
    print("3. CONVERGENCE BEHAVIOR:")
    solution = solver.solve(eq, verbose=False)
    if solution.method_used == "Catalan series":
        print(f"Converged in {solution.terms_used} terms")
        print(f"Final error: {solution.error:.2e}")
        print(f"This shows how small A leads to fast convergence!")


def main():
    """Main function that runs all examples"""
    print("QUADRATIC EQUATION SOLVER USAGE EXAMPLES")
    print("=" * 60)
    print("Demonstrating the use of Catalan numbers for solving second-degree equations")
    print()
    
    try:
        # Run basic examples
        basic_usage_example()
        batch_solving_example()
        convergence_analysis_example()
        performance_comparison_example()
        error_handling_example()
        advanced_analysis_example()
        educational_example()
        
        # Examples with visualization (require matplotlib)
        try:
            import matplotlib.pyplot as plt
            import numpy as np
            
            print("\nRunning visualization examples...")
            visualization_example()
            catalan_series_visualization()
            
        except ImportError:
            print("\nNote: matplotlib not available. Skipping visualization examples.")
            print("To see plots, install: pip install matplotlib numpy")
        
    except Exception as e:
        print(f"Error during execution: {e}")
        print("Check if all dependencies are installed.")
    
    print("\n" + "="*60)
    print("Examples completed! Check documentation for more details.")


if __name__ == "__main__":
    main()