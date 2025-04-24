from sympy import symbols, Function, Symbol, Eq, Derivative, dsolve, integrate, simplify

def solve_reaction_system(
    reactants: list[str], 
    products: list[str], 
    k,  # symbolic or numeric rate constant
    t: Symbol, 
    initial_conditions: dict[str, float]
):
    """
    Solves a system of reactions automatically:
    1. Builds ODEs for the reaction
    2. Solves using Laplace Transforms
    3. Computes necessary integrals (e.g., for reactions like A + B -> C)
    
    Args:
        reactants: List of reactant species (e.g., ['A', 'B']).
        products: List of product species (e.g., ['C']).
        k: Rate constant, can be a symbolic string or numeric value.
        t: SymPy symbol for time.
        initial_conditions: dictionary of initial concentrations.
    
    Returns:
        A dictionary with:
            - 'solutions': Solved ODEs for each species
            - 'integrals': Evaluated integrals for the reaction
    """
    
    # Handle rate constant (symbolic or numeric)
    k_sym = symbols(k) if isinstance(k, str) else k

    # Define all species (reactants + products)
    all_species = sorted(set(reactants + products))
    conc_funcs = {s: Function(s)(t) for s in all_species}

    # Build the rate law: rate = k * A * B (for a generic reaction A + B -> C)
    rate = k_sym
    for r in reactants:
        rate *= conc_funcs[r]

    # Build ODEs (rate of change of concentration)
    odes = {}
    for s in all_species:
        if s in reactants:
            odes[s] = -rate  # Consumption of reactants
        elif s in products:
            odes[s] = rate  # Formation of products
        else:
            odes[s] = 0  # Other species (not part of the reaction)

    # Handle initial concentrations (symbolic or numeric)
    init_vals = {}
    for s in all_species:
        val = initial_conditions.get(s, 0.0)
        init_vals[s] = symbols(val) if isinstance(val, str) else val

    # Step 1: Solve ODEs using Laplace transforms
    solutions = {}
    for func in conc_funcs.values():
        name = str(func.func)
        eq = Eq(Derivative(func, t), odes[name])  # Create the ODE
        ics = {func.subs(t, 0): init_vals[name]}  # Initial condition for t=0
        sol = dsolve(eq, func, ics=ics, method='laplace')  # Solve the ODE
        solutions[func] = sol.rhs  # Store the solution

    # Step 2: Compute integrals (e.g., ∫ A(t) * B(t) dt)
    integrals = {}
    for i, func_1 in enumerate(conc_funcs.values()):
        for func_2 in list(conc_funcs.values())[i + 1:]:
            # Compute integral if both species appear in the reaction
            A_t = solutions[func_1]
            B_t = solutions[func_2]
            integrand = k_sym * A_t * B_t  # Rate * A(t) * B(t)
            integral_expr = integrate(integrand, (t, 0, t))  # ∫ A(t)B(t) dt if necessary
            integrals[(str(func_1.func), str(func_2.func))] = simplify(integral_expr)

    return {
        "solutions": solutions,
        "integrals": integrals
    }

