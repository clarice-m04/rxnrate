from sympy import symbols, Function, Symbol
"""
    Builds ODEs for a single reaction and includes initial concentrations.
    Handles symbolic/string or numeric rate constants and initial values.
    
    Arguments:
        reactants: List of reactant species (e.g., ['A', 'B']).
        products: List of product species (e.g., ['C']).
        k: Rate constant, can be a string or a numeric value.
        t: SymPy symbol for time (to be prettier).
        initial_conditions: dictionary mapping species to initial concentrations (string or numeric).
    
    Returns:
        A dictionary with keys:
            'odes': symbolic ODEs
            'initial_conditions': symbolic or numeric initial values
            'species': list of symbolic concentration functions
    """

def build_simple_reaction_odes_flexible(
    reactants: list[str], 
    products: list[str], 
    k,  # can be a string (like k_1, k_2 i.e. symbolic) or a number (float/int)
    t: Symbol, 
    initial_conditions: dict[str, float]  # values can be strings (like a_0, b_0 etc i.e. symbolic) or numeric (float)
):
    
    # Handle string/symbolic or numeric rate constant
    k_sym = symbols(k) if isinstance(k, str) else k

    # All species in the reaction
    all_species = sorted(set(reactants + products))
    conc_funcs = {s: Function(s)(t) for s in all_species}
    
    # Build rate expression
    rate = k_sym
    for r in reactants:
        rate *= conc_funcs[r]

    # Build ODEs
    odes = {}
    for s in all_species:
        if s in reactants:
            odes[s] = -rate
        elif s in products:
            odes[s] = rate
        else:
            odes[s] = 0

    # Handle symbolic or numeric initial values
    init_vals = {}
    for s in all_species:
        val = initial_conditions.get(s, 0.0)
        init_vals[s] = symbols(val) if isinstance(val, str) else val

    return {
        "odes": odes,
        "initial_conditions": init_vals,
        "species": [conc_funcs[s] for s in all_species]
    }

# Example usage with mixed symbolic or string/numeric input: flex is what makes it be both
initials_flex = {'A': 'a_0', 'B': 2.0, 'C': 0.0}
flex_odes = build_simple_reaction_odes_flexible(['A', 'B'], ['C'], 'k1', t, initials_flex)
flex_odes