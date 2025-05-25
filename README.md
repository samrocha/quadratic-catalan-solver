# Quadratic Equation Solver with Catalan Numbers

An alternative quadratic equation solver that uses Catalan number series. Inspired by the paper:

Wildberger, N. J., & Rubine, D. (2025). A Hyper-Catalan Series Solution to Polynomial Equations, and the Geode. The American Mathematical Monthly, 132(5), 383–402. [https://doi.org/10.1080/00029890.2025.2460966](https://doi.org/10.1080/00029890.2025.2460966)

## 📋 Table of Contents

- [Overview](#-overview)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Catalan Numbers Method](#-catalan-numbers-method)
- [API Documentation](#-api-documentation)
- [Advanced Examples](#-advanced-examples)
- [Testing](#-testing)
- [Contributing](#-contributing)
- [License](#-license)

## 🎯 Overview

This project implements an innovative method for solving quadratic equations of the form `ax² + bx + c = 0` using infinite series based on **Catalan numbers**.

### Key Features

- ✅ **Alternative Method**: Uses Catalan numbers when `|A| ≤ 1/4` (where `A = ac/b²`)
- ✅ **High Precision**: Fine control of convergence tolerance
- ✅ **Special Cases**: Robust handling of linear equations and degenerate cases
- ✅ **Performance**: Fast convergence for small A values
- ✅ **Validation**: Comprehensive unit test suite
- ✅ **Visualization**: Convergence plots and visual analysis

### What are Catalan Numbers?

Catalan numbers form the sequence: **1, 1, 2, 5, 14, 42, 132, 429, ...**

They appear in various combinatorial problems:

- Ways to parenthesize expressions
- Grid paths that don't cross diagonals
- Binary trees
- Polygon triangulations

## 🚀 Installation

### Basic Dependencies

```bash
# Essential dependencies
pip install numpy

# For visualizations (optional)
pip install matplotlib

# For testing (optional)
pip install pytest
```text

### Direct Usage

```python
# Copy project files
# quadratic_catalan_solver.py - Main module
# usage_examples.py - Usage examples
# test_quadratic_catalan_solver.py - Unit tests
```

## ⚡ Quick Start

```python
from quadratic_catalan_solver import QuadraticEquation, CatalanSolver

# Create solver
solver = CatalanSolver(tolerance=1e-10)

# Solve equation x² + 4x + 1 = 0
equation = QuadraticEquation(a=1, b=4, c=1)
solution = solver.solve(equation, verbose=True)

# Access results
print(f"Roots: {solution.roots}")
print(f"Method: {solution.method_used}")
if solution.terms_used:
    print(f"Series terms: {solution.terms_used}")
```

## 📊 Catalan Numbers Method

### Applicability Conditions

The method is applied when:

- `|A| ≤ 1/4`, where `A = ac/b²`
- All coefficients are non-zero
- The equation is genuinely quadratic

### Mathematical Transformation

1. **Original equation**: `ax² + bx + c = 0`
2. **Parameter**: `A = ac/b²`
3. **Variable change**: `u = -(b/c)x`
4. **Transformed form**: `1 - u + Au² = 0`
5. **Catalan series**: `u = Σ C(n) × A^n`

### Convergence Algorithm

```python
u_series = 0
for n in range(max_terms):
    catalan_n = catalan_number(n)
    term = catalan_n * (A ** n)
    u_series += term
    
    error = abs(u_series - u_exact)
    if error < tolerance:
        break
```

## 📚 API Documentation

### Class `QuadraticEquation`

Represents a quadratic equation.

```python
QuadraticEquation(a: float, b: float, c: float)
```

**Parameters:**

- `a`: Coefficient of x²
- `b`: Coefficient of x
- `c`: Constant term

### Class `CatalanSolver`

Main solver class.

```python
CatalanSolver(tolerance: float = 1e-10)
```

**Main Methods:**

#### `solve(equation, verbose=False)`

Solves the equation using the most appropriate method.

**Parameters:**

- `equation`: Instance of `QuadraticEquation`
- `verbose`: If True, shows process details

**Returns:** `Solution` object with:

- `roots`: List of found roots
- `method_used`: Method used
- `terms_used`: Number of terms (if applicable)
- `error`: Approximation error (if applicable)

#### `catalan_number(n)`

Calculates the nth Catalan number.

**Parameters:**

- `n`: Index (n ≥ 0)

**Returns:** Catalan number C(n)

### Class `Solution`

Contains solution results.

```python
@dataclass
class Solution:
    roots: List[float]
    method_used: str
    terms_used: Optional[int] = None
    error: Optional[float] = None
```

## 🔍 Advanced Examples

### Convergence Analysis

```python
# Different tolerances
tolerances = [1e-4, 1e-8, 1e-12]
equation = QuadraticEquation(1, 6, 1)

for tol in tolerances:
    solver = CatalanSolver(tolerance=tol)
    solution = solver.solve(equation)
    print(f"Tolerance {tol}: {solution.terms_used} terms")
```

### Batch Solving

```python
equations = [
    QuadraticEquation(1, 4, 1),
    QuadraticEquation(2, 6, 1),
    QuadraticEquation(1, 2, 2),
]

solver = CatalanSolver()
results = []

for eq in equations:
    solution = solver.solve(eq)
    results.append({
        'equation': str(eq),
        'roots': solution.roots,
        'method': solution.method_used
    })
```

### Convergence Visualization

```python
import matplotlib.pyplot as plt
import numpy as np

# Visualize series convergence
A = 1/16  # Equation parameter
terms = []
partial_sums = []

solver = CatalanSolver()
partial_sum = 0

for n in range(15):
    catalan_n = solver.catalan_number(n)
    term = catalan_n * (A ** n)
    partial_sum += term
    
    terms.append(term)
    partial_sums.append(partial_sum)

# Plot convergence
plt.plot(partial_sums, 'bo-')
plt.xlabel('Number of terms')
plt.ylabel('Partial sum')
plt.title('Catalan Series Convergence')
plt.grid(True)
plt.show()
```

## 🧪 Testing

### Run Tests

```bash
# All tests
python test_quadratic_solver.py

# Specific tests with pytest
pytest test_quadratic_solver.py::TestCatalanSolver -v

# Tests with coverage
pytest --cov=quadratic_solver test_quadratic_solver.py
```

### Test Categories

1. **Catalan Numbers**: Verifies correct calculations
2. **Special Cases**: Linear equations, zero coefficients
3. **Catalan Method**: Convergence and precision
4. **Integration**: Solution verification
5. **Edge Cases**: Very small/large coefficients

### Test Example

```python
def test_catalan_method_favorable_case(self, solver):
    # x² + 4x + 1 = 0 (A = 1/16 = 0.0625 ≤ 0.25)
    eq = QuadraticEquation(1, 4, 1)
    solution = solver.solve(eq)
    
    assert solution.method_used == "Catalan series"
    assert solution.terms_used is not None
    assert solution.error < solver.tolerance
```

## 📈 Performance

### Typical Benchmarks

| Method | Equations/s | Precision | Applicable Cases |
|--------|-------------|-----------|------------------|
| Catalan | ~1000/s | 1e-12 | \|A\| ≤ 1/4 |
| Standard | ~5000/s | 1e-15 | All cases |

### When to Use Each Method

**Use Catalan Method when:**

- `|A| ≤ 1/4` (necessary condition)
- Controlled precision is important
- Educational/mathematical analysis
- Avoiding numerical issues with small discriminants

**Use Standard Method when:**

- `|A| > 1/4`
- Maximum performance is priority
- Simple implementation is sufficient

## 🎓 Educational Aspects

### Mathematical Connections

This project illustrates connections between:

- **Algebra**: Quadratic equations
- **Combinatorics**: Catalan numbers
- **Analysis**: Infinite series
- **Programming**: Numerical algorithms

### Pedagogical Value

- Demonstrates alternative solution methods
- Connects different areas of mathematics
- Teaches numerical precision control
- Illustrates series convergence

## 🔧 Code Structure

### File Organization

``` text
quadratic_catalan_solver/
├── quadratic_solver.py      # Main module
├── test_quadratic_solver.py # Unit tests
├── usage_examples.py        # Usage examples
├── README.md               # Documentation
└── requirements.txt        # Dependencies
```

### Design Principles

1. **Encapsulation**: Well-defined classes
2. **Separation of Concerns**: Each class has specific function
3. **Extensibility**: Easy to add new methods
4. **Testability**: Easily testable code
5. **Documentation**: Clear comments and docstrings

## 🚨 Limitations and Considerations

### Catalan Method Limitations

- ❌ Only works when `|A| ≤ 1/4`
- ❌ Requires calculating multiple terms
- ❌ Slower than traditional quadratic formula

### Unique Advantages

- ✅ Deep mathematical insights
- ✅ Fine precision control
- ✅ Connection to combinatorics
- ✅ Numerically stable for small A

## 🤝 Contributing

### How to Contribute

1. **Fork** the repository
2. **Create** a branch for your feature
3. **Implement** improvements or fixes
4. **Add** appropriate tests
5. **Update** documentation
6. **Submit** a Pull Request

### Areas for Contribution

- Performance optimizations
- New solution methods
- More visualizations
- Additional documentation
- Bug fixes

## 📄 License

This project is distributed under the MIT License. See the `LICENSE` file for details.

## 📞 Support

For questions, suggestions, or issues:

- Open an **Issue** in the repository
- Consult the **complete documentation**
- Run the provided **examples**

---

### Developed with ❤️ to demonstrate the beauty of computational mathematics
