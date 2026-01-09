from typing import Any
from app.modules.sessions.engine.utils.log_types import ActionLogType, ActionLogEntry
from app.modules.sessions.engine.game_states import GameState

def _append_log(
    game_state: GameState,
    *,
    type: ActionLogType,
    payload: Any = None,
) -> None:
    game_state.action_logs.append(
        ActionLogEntry(
            sequence=game_state.next_log_sequence,
            hand_id=game_state.hand.id,
            street=game_state.hand.street,
            type=type,
            payload=payload,
        )
    )
    game_state.next_log_sequence += 1
