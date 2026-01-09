from app.modules.sessions.engine.managers.showdown_manager import ShowdownManager, ShowdownPotWinners

def test_showdown_distribution(game_state_3p):
    gs = game_state_3p
    
    pot = gs.pots[0]
    pot.size = 100
    pot.players_in_pot = [1, 2]
    
    payouts = ShowdownManager.resolve(
        gs,
        [ShowdownPotWinners(pot_index=0, pot_winners_ids=[1, 2])]
    )
    
    assert sum(p.amount_won for p in payouts) == 100
