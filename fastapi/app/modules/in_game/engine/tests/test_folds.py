from app.db.tables.hands.schemas import HandStreet
from app.modules.in_game.engine.flow.hand_flow import HandFlow
from app.modules.in_game.engine.flow.bet_round_flow import BetRoundFlow
from app.modules.in_game.engine.managers.action_manager import ActionType
from app.modules.in_game.engine.utils.enums import HandResult

def test_bet_fold_fold_autowin(game_state_3p):
    gs = game_state_3p
    
    HandFlow.start(gs, dealer_position=0)
    
    BetRoundFlow.after_action(gs, ActionType.BET, 20)
    BetRoundFlow.after_action(gs, ActionType.FOLD)
    BetRoundFlow.after_action(gs, ActionType.FOLD)
    
    BetRoundFlow.finish(gs)
    result = HandFlow.after_bet_round(gs)
    
    assert result == HandResult.AUTO_WIN
    
    HandFlow.finish(gs)
    assert gs.hand.street == HandStreet.WINNER_SELECTION
