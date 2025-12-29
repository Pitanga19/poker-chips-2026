from app.modules.in_game.engine.flow.hand_flow import HandFlow
from app.modules.in_game.engine.flow.bet_round_flow import BetRoundFlow
from app.modules.in_game.engine.managers.action_manager import ActionType
from app.modules.in_game.engine.utils.enums import HandResult

def test_bet_fold_fold_autowin(game_state_3p):
    gs = game_state_3p
    small_blind_value = gs.hand.small_blind_value
    big_blind_value = gs.hand.big_blind_value
    
    HandFlow.start(gs, dealer_position=0)
    
    winner_initial_stack = gs.players_by_position[gs.bet_round.current_turn_position].stack
    BetRoundFlow.after_action(gs, ActionType.BET, 20)
    BetRoundFlow.after_action(gs, ActionType.FOLD)
    BetRoundFlow.after_action(gs, ActionType.FOLD)
    
    BetRoundFlow.finish(gs)
    result = HandFlow.after_bet_round(gs)
    
    assert result == HandResult.AUTO_WIN
    
    HandFlow.finish(gs)
    
    winner = max(gs.players, key=lambda p: p.stack)
    assert winner.stack == winner_initial_stack + small_blind_value + big_blind_value
