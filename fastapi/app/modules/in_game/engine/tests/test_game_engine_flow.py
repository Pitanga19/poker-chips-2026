from app.modules.in_game.engine.game_engine import GameEngine
from app.modules.in_game.engine.managers.action_manager import ActionType

def test_full_hand_flow(game_state_3p):
    engine = GameEngine(game_state_3p)
    
    engine.start(dealer_position=0)
    
    engine.action(ActionType.CALL)
    engine.action(ActionType.CALL)
    engine.action(ActionType.CHECK)
    
    # termina ronda
    engine.action(ActionType.CHECK)
    engine.action(ActionType.CHECK)
    engine.action(ActionType.CHECK)
    
    # no debe romper
    engine.next_hand()
