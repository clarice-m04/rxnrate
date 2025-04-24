import sympy as sp
t = sp.symbols('t')
s = sp.symbols('s')

def calculate_laplace_transforms(reagents, products, k, initial_concentrations):
    """
    Calculates the Laplace transforms for the reactants and products.
    
    reagents: List of reactant names (e.g., ['A', 'B'])
    products: List of product names (e.g., ['C', 'D'])
    k: Rate constant
    initial_concentrations: Dictionary with initial concentrations for each species
    
    Returns:
        A dictionary containing the Laplace transforms for all reactants and products.
    """
    # Define symbolic concentrations
    concentrations = {name: sp.Function(name)(t) for name in reagents + products}
    
    # Compute the Laplace transforms for the reactants
    reactant_laplace = {}
    for reagent in reagents:
        # L{A(t)} = A_0 / (s + k)
        reactant_laplace[reagent] = initial_concentrations[reagent] / (s + k)
    
    # Now calculate the Laplace transforms for the products
    product_laplace = {}
    rate_reactants = 0
    for reagent in reagents:
        rate_reactants += concentrations[reagents[0]] * concentrations[reagents[1]]
    
    # Use the previously calculated Laplace transforms of A and B in the product calculation
    for product in products:
        if product == products[0] or product == products[1]:
            # For products, assume they form from the reactants in a simple way
            # Simplified as A(s) * B(s) / s for product formation
            product_laplace[product] = (reactant_laplace[reagents[0]] * reactant_laplace[reagents[1]]) / s
    
    # Combine both dictionaries (reactant_laplace and product_laplace)
    combined_laplace = {**reactant_laplace, **product_laplace}
    
    return combined_laplace

def simplify_inverse_laplace(expr):
    """
    Simplifies the inverse Laplace transform by replacing Heaviside(t) with 1
    and performing any necessary simplifications.
    """
    # Replace Heaviside(t) with 1
    simplified_expr = expr.subs(sp.Heaviside(t), 1)
    simplified_expr = sp.simplify(simplified_expr)
    return simplified_expr


# Function to calculate the inverse Laplace transforms of the provided Laplace transforms
def inverse_laplace_transform(laplace_results):
    """
    Calculates the inverse Laplace transform for each given Laplace result.
    
    laplace_results: A dictionary containing Laplace transforms of species
    
    Returns:
        A dictionary containing the inverse Laplace transforms of the species.
    """
    inverse_results = {}
    
    for species, laplace_expr in laplace_results.items():
        # Calculate the inverse Laplace transform using sympy's inverse_laplace_transform function
        inverse_expr = sp.inverse_laplace_transform(laplace_expr, s, t)
        
        # Simplify the result by replacing Heaviside(t) with 1
        inverse_results[species] = simplify_inverse_laplace(inverse_expr)
    
    return inverse_results


# Example usage:
reagents = ['A', 'B', 'E']
products = ['C', 'D']
k = 4.0
initial_concentrations = {'A': 1.0, 'B': 1.0, 'C': 0.0, 'D': 0.0, 'E': 3.0}

# Calculate Laplace transforms
lp_transforms = calculate_laplace_transforms(reagents, products, k, initial_concentrations)

# Output combined Laplace transforms
print("Combined Laplace transforms:")
for species, laplace_expr in lp_transforms.items():
    print(f"{species}(s): {laplace_expr}")

# Calculate the inverse Laplace transforms
inverse_results = inverse_laplace_transform(lp_transforms)

# Output inverse Laplace transforms
print("\nInverse Laplace transforms:")
for species, inverse_expr in inverse_results.items():
    print(f"Inverse Laplace transform of {species}(s): {inverse_expr}")
