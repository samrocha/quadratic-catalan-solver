import math

def catalan_number(n):
    """Calcula o n-ésimo número de Catalan"""
    if n == 0:
        return 1
    result = 1
    for i in range(n):
        result = result * (2 * n - i) // (i + 1)
    return result // (n + 1)

def demo_catalan_method():
    """
    Demonstração do método de Catalan para resolver x² + 4x + 1 = 0
    
    Passos do método:
    1. Calcular A = ac/b² = (1×1)/(4²) = 1/16 = 0.0625
    2. Como |A| ≤ 1/4, podemos usar a série de Catalan
    3. Transformar para u = -(b/c)x = -4x
    4. Resolver 1 - u + Au² = 0 usando u = Σ C(n)A^n
    5. Converter de volta para x
    """
    
    # Coeficientes da equação x² + 4x + 1 = 0
    a, b, c = 1, 4, 1
    
    print("RESOLVENDO x² + 4x + 1 = 0 COM NÚMEROS DE CATALAN")
    print("=" * 55)
    
    # Passo 1: Calcular A
    A = (a * c) / (b * b)
    print(f"Passo 1: A = ac/b² = ({a}×{c})/({b}²) = {A}")
    print(f"Como |A| = {abs(A)} ≤ 0.25, podemos usar o método!")
    print()
    
    # Passo 2: Solução exata para comparação
    u_exact = (1 - math.sqrt(1 - 4*A)) / (2*A)
    print(f"Solução exata: u = (1 - √(1-4A))/(2A) = {u_exact:.10f}")
    print()
    
    # Passo 3: Série de Catalan
    print("SÉRIE DE CATALAN: u = C₀A⁰ + C₁A¹ + C₂A² + C₃A³ + ...")
    print()
    print("n  | C(n) |    A^n    | C(n)×A^n  |  Soma    |   Erro")
    print("-" * 55)
    
    u_series = 0
    tolerance = 1e-10
    
    for n in range(15):  # Máximo 15 termos
        catalan_n = catalan_number(n)
        a_power_n = A ** n
        term = catalan_n * a_power_n
        u_series += term
        
        error = abs(u_series - u_exact)
        
        print(f"{n:2d} | {catalan_n:4d} | {a_power_n:9.7f} | {term:9.7f} | {u_series:8.6f} | {error:.2e}")
        
        if error < tolerance:
            print(f"\nConvergiu com {n+1} termos!")
            break
    
    # Passo 4: Converter de volta para x
    # Da transformação u = -(b/c)x, temos x = -(c/b)u
    x_solution = -(c/b) * u_series
    print(f"\nSolução: x = -(c/b)×u = -({c}/{b})×{u_series:.8f} = {x_solution:.8f}")
    
    # Verificação
    verification = a * x_solution**2 + b * x_solution + c
    print(f"Verificação: {a}×({x_solution:.6f})² + {b}×({x_solution:.6f}) + {c} = {verification:.2e}")
    
    # Segunda raiz pela relação de Vieta: x₁×x₂ = c/a
    x2 = c / (a * x_solution)
    print(f"Segunda raiz: x₂ = c/(a×x₁) = {c}/({a}×{x_solution:.6f}) = {x2:.8f}")
    
    # Comparação com fórmula quadrática padrão
    print(f"\nCOMPARAÇÃO COM FÓRMULA QUADRÁTICA:")
    discriminant = b*b - 4*a*c
    x1_standard = (-b + math.sqrt(discriminant)) / (2*a)
    x2_standard = (-b - math.sqrt(discriminant)) / (2*a)
    print(f"Fórmula padrão: x₁ = {x1_standard:.8f}, x₂ = {x2_standard:.8f}")
    print(f"Método Catalan: x₁ = {x_solution:.8f}, x₂ = {x2:.8f}")
    
    print(f"\nDiferença x₁: {abs(x_solution - x1_standard):.2e}")
    print(f"Diferença x₂: {abs(x2 - x2_standard):.2e}")

def show_catalan_numbers():
    """Mostra os primeiros números de Catalan e suas aplicações"""
    print("\nNÚMEROS DE CATALAN - Uma Sequência Fascinante")
    print("=" * 50)
    
    print("Os primeiros números de Catalan:")
    for n in range(10):
        cn = catalan_number(n)
        print(f"C({n}) = {cn}")
    
    print("\nAplicações dos números de Catalan:")
    print("• Número de formas de colocar parênteses: ((ab)c) vs (a(bc))")
    print("• Caminhos em grade que não cruzam a diagonal")
    print("• Número de árvores binárias com n+1 folhas")
    print("• Triangulações de polígonos convexos")
    print("• E agora: resolução de equações quadráticas!")

# Executar demonstração
demo_catalan_method()
show_catalan_numbers()