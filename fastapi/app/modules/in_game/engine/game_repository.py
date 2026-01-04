from uuid import UUID
from typing import Dict
from app.core.exceptions import NotFoundException
from app.modules.in_game.engine.game_states import GameState

class GameRepository:
    _games: Dict[UUID, GameState] = {}
    
    @classmethod
    def save(cls, game_state: GameState) -> None:
        cls._games[game_state.id] = game_state
    
    @classmethod
    def get(cls, game_id: UUID) -> GameState:
        try:
            return cls._games[game_id]
        except KeyError:
            raise NotFoundException(f'Juego {game_id} no encontrado')
    
    @classmethod
    def delete(cls, game_id: UUID) -> None:
        cls._games.pop(game_id, None)
