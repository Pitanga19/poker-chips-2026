from typing import Optional
from app.modules.lobbies.core.states import (
    UserData,
    LobbyPlayerState,
    ToCreateLobbyData,
    GameSettings,
    LobbyState,
    LobbyJoinResult,
)

class LobbyManager:
    @staticmethod
    def create(data: ToCreateLobbyData) -> LobbyState:
        hoster = LobbyPlayerState(
            id=data.hoster_id,
            username=data.hoster_username,
            position=data.self_position,
            stack=data.initial_stack,
        )
        game_settings = GameSettings(
            hoster_id=data.hoster_id,
            players=[hoster],
            initial_stack=data.initial_stack,
            table_size=data.table_size,
            big_blind_value=data.big_blind_value,
        )
        
        return LobbyState(
            id=data.lobby_id,
            settings=game_settings,
        )
    
    @staticmethod
    def join(lobby: LobbyState, user: UserData, position: Optional[int]=None) -> LobbyJoinResult:
        if position is None:
            position = lobby.random_free_position
        
        player = LobbyPlayerState(
            id=user.id,
            username=user.username,
            position=position,
            stack=lobby.settings.initial_stack,
        )
        
        lobby.settings.players.append(player)
        
        return LobbyJoinResult(
            player=player,
            lobby=lobby,
        )
