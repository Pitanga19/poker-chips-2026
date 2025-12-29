from app.modules.in_game.engine.flow.hand_flow import HandFlow
from app.modules.in_game.engine.flow.bet_round_flow import BetRoundFlow
from app.modules.in_game.engine.managers.action_manager import ActionType

def test_simple_side_pot(game_state_3p):
    gs = game_state_3p
    
    # Ajustar stacks
    gs.players_by_position[0].stack = 100
    gs.players_by_position[1].stack = 30
    gs.players_by_position[2].stack = 100
    
    HandFlow.start(gs, dealer_position=0)
    
    BetRoundFlow.after_action(gs, ActionType.BET, 50)
    BetRoundFlow.after_action(gs, ActionType.ALL_IN)
    BetRoundFlow.after_action(gs, ActionType.CALL)
    
    BetRoundFlow.finish(gs)
    
    assert len(gs.pots) == 2
    
    main_pot = gs.pots[0]
    side_pot = gs.pots[1]
    
    assert main_pot.size == 30 * 3
    assert side_pot.size == (50 - 30) * 2
