from typing import Optional
from app.modules.sessions.api.schemas import GameStartRequest, ToCreatePlayerInfo
from app.modules.lobbies.core.manager import LobbyManager
from app.modules.lobbies.core.states import (
    UserData,
    ToCreateLobbyData,
    LobbyState,
    LobbyJoinResult,
)
from app.modules.lobbies.api.schemas import (
    UserInfo,
    LobbyPlayerInfo,
    LobbyFullData,
    LobbyCreateRequest,
    LobbyCreateResponse,
    LobbyJoinResponse,
)

class LobbyMapper:
    @staticmethod
    def _lobby_to_full_data_response(lobby: LobbyState) -> LobbyFullData:
        return LobbyFullData(
            lobby_id=lobby.id,
            hoster_id=lobby.settings.hoster_id,
            players=[
                LobbyPlayerInfo(
                    id=p.id,
                    username=p.username,
                    position=p.position,
                    stack=p.stack,
                )
                for p in lobby.settings.players
            ],
            initial_stack=lobby.settings.initial_stack,
            table_size=lobby.settings.table_size,
            small_blind_value=lobby.settings.small_blind_value,
            big_blind_value=lobby.settings.big_blind_value,
            dealer_position=lobby.settings.dealer_position,
        )
    
    @staticmethod
    def request_to_lobby_state(lobby_id: str, request: LobbyCreateRequest) -> LobbyState:
        create_data = ToCreateLobbyData(
            lobby_id=lobby_id,
            hoster_id=request.hoster_info.id,
            hoster_username=request.hoster_info.username,
            initial_stack=request.initial_stack,
            self_position=request.self_position,
            table_size=request.table_size,
            big_blind_value=request.big_blind_value,
        )
        return LobbyManager.create(create_data)
    
    def lobby_to_create_response(lobby: LobbyState) -> LobbyCreateResponse:
        return LobbyMapper._lobby_to_full_data_response(lobby)
    
    def request_to_join_lobby(
        lobby: LobbyState, user: UserInfo, position: Optional[int]=None
    ) -> LobbyJoinResult:
        user_data = UserData(
            id=user.id,
            username=user.username,
        )
        return LobbyManager.join(lobby, user_data, position)
    
    def lobby_to_join_response(join_result: LobbyJoinResult) -> LobbyJoinResponse:
        lobby = join_result.lobby
        settings = lobby.settings
        players = [
            LobbyPlayerInfo(
                id=p.id,
                username=p.username,
                position=p.position,
                stack=p.stack,
            )
            for p in settings.players
        ]
        joined_player = LobbyPlayerInfo(
            id=join_result.player.id,
            username=join_result.player.username,
            position=join_result.player.position,
            stack=join_result.player.stack,
        )
        
        return LobbyJoinResponse(
            hoster_id=settings.hoster_id,
            players=players,
            initial_stack=settings.initial_stack,
            table_size=settings.table_size,
            small_blind_value=settings.small_blind_value,
            big_blind_value=settings.big_blind_value,
            dealer_position=settings.dealer_position,
            lobby_id=lobby.id,
            joined_player=joined_player,
        )
    
    def lobby_to_get_response(lobby: LobbyState) -> LobbyCreateResponse:
        return LobbyMapper._lobby_to_full_data_response(lobby)
    
    def lobby_to_update_response(lobby: LobbyState) -> LobbyCreateResponse:
        return LobbyMapper._lobby_to_full_data_response(lobby)
    
    def lobby_to_game_start_request(lobby: LobbyState) -> GameStartRequest:
        settings = lobby.settings
        players = [
            ToCreatePlayerInfo(
                id=p.id,
                username=p.username,
                position=p.position,
                stack=p.stack,
            )
            for p in settings.players
        ]
        
        return GameStartRequest(
            table_size=settings.table_size,
            players=players,
            small_blind_value=settings.small_blind_value,
            big_blind_value=settings.big_blind_value,
            dealer_position=settings.dealer_position,
        )