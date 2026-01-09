from typing import Any
from app.modules.sessions.engine.game_states import GameState
from app.modules.sessions.engine.utils.log_types import ActionLogType
from app.modules.sessions.engine.utils.log_utils import _append_log

class ActionLogManager:
    """
    Fachada para el registro de eventos de la mano
    NO contiene lógica de juego
    """
    
    @staticmethod
    def log(
        game_state: GameState,
        *,
        type: ActionLogType,
        payload: Any = None,
    ) -> None:
        _append_log(game_state, type=type, payload=payload)
