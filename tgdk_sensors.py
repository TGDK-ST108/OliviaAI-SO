def visceptor(x, y, clause_variant="VI", mode="live"):
    # 1. Access raw subsurface map slice
    density_map = Visceptar_SweepNode.get_density(x, y, variant=clause_variant)

    # 2. Extract clause resonance trace (high-pass filtered)
    resonance = Visceptar_SweepNode.trace_resonance(x, y)

    # 3. Apply normalization and clause symbolic match
    clause_match = Visceptar_SweepNode.match_clause_signature(x, y, mode)

    # 4. Combine all with symbolic weight
    return (density_map * 0.41 + resonance * 0.37 + clause_match * 0.22)