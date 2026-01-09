from app.modules.sessions.engine.flow.hand_flow import HandFlow
from app.modules.sessions.engine.flow.bet_round_flow import BetRoundFlow
from app.modules.sessions.engine.managers.action_manager import ActionType

def test_multi_side_pots(game_state_4p):
    gs = game_state_4p
    
    HandFlow.start(gs, dealer_position=1)
    
    BetRoundFlow.after_action(gs, ActionType.BET, 100)
    BetRoundFlow.after_action(gs, ActionType.CALL)
    BetRoundFlow.after_action(gs, ActionType.ALL_IN)
    BetRoundFlow.after_action(gs, ActionType.ALL_IN)
    
    BetRoundFlow.finish(gs)
    
    assert len(gs.pots) == 3
    
    assert gs.pots[0].size == 40 * 4
    assert gs.pots[1].size == 40 * 3
    assert gs.pots[2].size == 20 * 2
