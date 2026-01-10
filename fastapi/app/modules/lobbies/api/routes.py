from fastapi import APIRouter
from app.modules.sessions.api.schemas import GameStartResponse
from app.modules.lobbies.api.services import LobbyService
from app.modules.lobbies.api.schemas import (
    LobbyCreateRequest,
    LobbyCreateResponse,
    LobbyJoinRequest,
    LobbyJoinResponse,
    GetLobbyResponse,
    LobbyUpdateRequest,
    LobbyUpdateResponse,
)

router = APIRouter(prefix='/lobbies', tags=['Lobbies'])

@router.post('', response_model=LobbyCreateResponse, status_code=201)
def create_lobby_endpoint(request: LobbyCreateRequest) -> LobbyCreateResponse:
    return LobbyService.create(request)

@router.post('/{lobby_id}/join', response_model=LobbyJoinResponse)
def join_lobby_endpoint(lobby_id: str, request: LobbyJoinRequest) -> LobbyJoinResponse:
    return LobbyService.join(lobby_id, request)

@router.get('/{lobby_id}', response_model=GetLobbyResponse)
def get_lobby_endpoint(lobby_id: str) -> GetLobbyResponse:
    return LobbyService.get(lobby_id)

@router.patch('/{lobby_id}', response_model=LobbyUpdateResponse)
def update_lobby_endpoint(lobby_id: str, request: LobbyUpdateRequest) -> LobbyUpdateResponse:
    return LobbyService.update(lobby_id, request)

@router.delete('/{lobby_id}', status_code=204)
def delete_lobby_endpoint(lobby_id: str):
    LobbyService.delete(lobby_id)

@router.post('/{lobby_id}/start', response_model=GameStartResponse)
def start_game_endpoint(lobby_id: str) -> GameStartResponse:
    return LobbyService.start_game(lobby_id)
