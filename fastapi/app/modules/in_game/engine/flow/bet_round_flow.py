from typing import Optional
from app.db.utils.enums import ActionType
from app.modules.in_game.engine.game_states import GameState
from app.modules.in_game.engine.flow.turn_flow import TurnStageFlow
from app.modules.in_game.engine.managers.action_manager import ActionManager
from app.modules.in_game.engine.managers.pot_manager import PotManager
from app.modules.in_game.engine.utils.enums import BetRoundResult
from app.modules.in_game.engine.utils.player_reset import bet_round_players_state_reset
from app.modules.in_game.engine.utils.bet_round_utils import (
    bet_round_state_reset,
    bet_round_finished,
)

class BetRoundFlow:
    """
    Maneja la dinámica de una ronda de apuestas completa
    No valida acciones ni decide ganadores
    Una ronda termina cuando no hay siguiente jugador que pueda actuar
    """
    
    @staticmethod
    def start(game_state: GameState) -> None:        
        # Obtener el primer jugador que debe actuar
        first_player = TurnStageFlow.get_first_player_to_act(game_state)
        
        # Si no hay ningún jugador devuelve None para terminarla directamente
        if first_player is None:
            game_state.bet_round.current_turn_position = None
            return
        
        game_state.bet_round.current_turn_position = first_player.position
    
    @staticmethod
    def after_action(game_state: GameState, action: ActionType, amount: Optional[int] = None) -> BetRoundResult:
        ActionManager.apply_action(game_state, action, amount)
        
        if bet_round_finished(game_state):
            game_state.bet_round.current_turn_position = None
            return BetRoundResult.FINISHED
        
        next_player = TurnStageFlow.get_next_player_to_act(game_state)
        
        if next_player is None:
            game_state.bet_round.current_turn_position = None
            return BetRoundResult.FINISHED
        
        game_state.bet_round.current_turn_position = next_player.position
        return BetRoundResult.NEXT_TURN
    
    @staticmethod
    def finish(game_state: GameState) -> None:
        # Primero recolecta las apuestas
        PotManager.collect_bets_into_pots(game_state)
        
        # Por último los reset de valores de estado
        bet_round_state_reset(game_state.bet_round)
        bet_round_players_state_reset(game_state.players)
