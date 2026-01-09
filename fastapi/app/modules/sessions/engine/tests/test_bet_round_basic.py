from app.modules.sessions.engine.flow.hand_flow import HandFlow
from app.modules.sessions.engine.flow.bet_round_flow import BetRoundFlow
from app.modules.sessions.engine.managers.action_manager import ActionType
from app.modules.sessions.engine.utils.enums import BetRoundResult, HandResult
from app.modules.sessions.engine.tests.test_invariants import assert_invariants

def test_check_check_check(game_state_3p):
    gs = game_state_3p
    initial = sum(p.stack for p in gs.players)
    
    HandFlow.start(gs, dealer_position=0)
    
    assert BetRoundFlow.after_action(gs, ActionType.CALL) == BetRoundResult.NEXT_TURN
    assert BetRoundFlow.after_action(gs, ActionType.CALL) == BetRoundResult.NEXT_TURN
    assert BetRoundFlow.after_action(gs, ActionType.CHECK) == BetRoundResult.FINISHED
    
    BetRoundFlow.finish(gs)
    result = HandFlow.after_bet_round(gs)
    
    assert result == HandResult.NEXT_STREET
    
    assert_invariants(gs, initial)
