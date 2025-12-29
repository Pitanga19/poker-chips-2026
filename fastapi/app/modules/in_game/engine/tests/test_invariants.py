def assert_invariants(game_state, initial_chips):
    total_players = sum(p.stack + p.betting_stack for p in game_state.players)
    total_pots = sum(pot.size for pot in game_state.pots)
    
    assert total_players + total_pots == initial_chips
    
    for p in game_state.players:
        assert p.stack >= 0
        assert p.betting_stack >= 0
