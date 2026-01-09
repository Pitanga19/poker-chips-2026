from typing import Optional
from app.core.exceptions import ValidationException
from app.modules.sessions.engine.game_states import GameState, PlayerState
from app.modules.sessions.engine.utils.turn_utils import get_first_to_act_position, get_next_can_act_position

class TurnStageFlow:
    # Maneja el orden de turno de los jugadores
    
    @staticmethod
    def get_first_player_to_act(game_state: GameState) -> Optional[PlayerState]:
        players_by_position = game_state.players_by_position
        players = game_state.players
        hand = game_state.hand
        
        # Obtener posición del primer jugador en actuar
        ftap = get_first_to_act_position(hand, players)
        
        # Si no hay nadie por jugar: fin de ronda automáticamente
        if ftap is None:
            return None
        
        # Retorna el primer jugador en actuar
        return players_by_position[ftap]
    
    @staticmethod
    def get_next_player_to_act(game_state: GameState) -> Optional[PlayerState]:
        """
        Retorna el siguiente jugador en actuar
        Retorna None si no hay siguiente jugador, se debe finalizar la ronda
        """
        
        # Si current_player es None, es un error de flujo (no de usuario)
        if game_state.current_player is None:
            raise ValidationException('No hay current_player en turno activo')
        
        cpp = game_state.current_player.position
        players = game_state.players
        
        # Obtener posición del siguiente jugador que puede actuar
        ncap = get_next_can_act_position(cpp, players)
        
        # Si no queda nadie: fin de ronda
        if ncap is None:
            return None
        
        # Retorna el siguiente jugador que puede actuar
        return game_state.players_by_position[ncap]
