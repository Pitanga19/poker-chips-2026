from typing import Dict
from app.modules.lobbies.core.states import LobbyState

class LobbyRepository:
    _lobbies: Dict[str, LobbyState] = {}
    
    @classmethod
    def save(cls, lobby_state: LobbyState) -> None:
        cls._lobbies[lobby_state.id] = lobby_state
    
    @classmethod
    def get(cls, lobby_id: str) -> LobbyState:
        return cls._lobbies.get(lobby_id)
    
    @classmethod
    def delete(cls, lobby_id: str) -> None:
        cls._lobbies.pop(lobby_id, None)
