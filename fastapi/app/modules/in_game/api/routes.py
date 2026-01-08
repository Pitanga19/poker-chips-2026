from fastapi import APIRouter
from uuid import UUID
from app.modules.in_game.api.services import GameService
from app.modules.in_game.api.schemas import (
    GameStartRequest,
    GameStartResponse,
    GameRenderResponse,
    AvailableActionsResponse,
    PlayerActionRequest,
    PlayerActionResponse,
    ShowdownInfoResponse,
    ShowdownResolveRequest,
    ShowdownResolveResponse,
)

router = APIRouter(prefix='/sessions', tags=['Play'])

# Iniciar un nuevo juego
@router.post('', response_model=GameStartResponse, status_code=201)
def start_game_endpoint(request: GameStartRequest) -> GameStartResponse:
    return GameService.start(request)

# Obtener acciones disponibles para el jugador actual
@router.get('/{game_id}/actions', response_model=AvailableActionsResponse)
def available_actions_endpoint(game_id: UUID) -> AvailableActionsResponse:
    return GameService.available_actions(game_id)

# Realizar una acción en la mano
@router.post('/{game_id}/actions', response_model=PlayerActionResponse)
def player_action_endpoint(
    game_id: UUID, request: PlayerActionRequest
) -> PlayerActionResponse:
    return GameService.player_action(game_id, request)

# Obtener información del showdown
@router.get('/{game_id}/showdown', response_model=ShowdownInfoResponse)
def get_showdown_info_endpoint(game_id: UUID) -> ShowdownInfoResponse:
    return GameService.get_showdown_info(game_id)

# Resolver el showdown
@router.post('/{game_id}/showdown', response_model=ShowdownResolveResponse)
def showdown_resolve_endpoint(
    game_id: UUID, request: ShowdownResolveRequest
) -> ShowdownResolveResponse:
    return GameService.showdown_resolve(game_id, request)

# Iniciar la siguiente mano
@router.post('/{game_id}/next-hand', response_model=GameStartResponse)
def next_hand_endpoint(game_id: UUID) -> GameStartResponse:
    return GameService.next_hand(game_id)
