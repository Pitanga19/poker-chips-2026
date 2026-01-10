from app.core.exceptions import ValidationException, NotFoundException
from app.modules.sessions.api.services import GameService
from app.modules.sessions.api.schemas import GameStartResponse
from app.modules.lobbies.core.utils import generate_lobby_code
from app.modules.lobbies.core.states import LobbyState
from app.modules.lobbies.core.repository import LobbyRepository
from app.modules.lobbies.api.mapper import LobbyMapper
from app.modules.lobbies.api.schemas import (
    LobbyCreateRequest,
    LobbyCreateResponse,
    LobbyJoinRequest,
    LobbyJoinResponse,
    GetLobbyResponse,
    LobbyUpdateRequest,
    LobbyUpdateResponse,
)

class LobbyService:
    @staticmethod
    def _get_existing_lobby(lobby_id: str) -> LobbyState:
        lobby = LobbyRepository.get(lobby_id)
        
        if lobby is None:
            raise NotFoundException(f'Lobby {lobby_id} no encontrado.')
        
        return lobby
    
    @staticmethod
    def create(request: LobbyCreateRequest) -> LobbyCreateResponse:
        while True:
            lobby_id = generate_lobby_code()
            if LobbyRepository.get(lobby_id) is None:
                break
        
        if request.table_size < 2:
            raise ValidationException('La mesa debe tener al menos 2 asientos.')
        
        if request.big_blind_value < 2:
            raise ValidationException('La ciega grande debe ser al menos de 2 fichas.')
        
        if request.initial_stack < 20*request.big_blind_value:
            raise ValidationException('El saldo inicial debe ser al menos de 20 ciegas grandes.')
        
        if request.self_position not in range(1, request.table_size + 1):
            raise ValidationException(
                'La posición del jugador debe estar entre 1 y la cantidad de asientos.'
            )
        
        lobby = LobbyMapper.request_to_lobby_state(lobby_id, request)
        LobbyRepository.save(lobby)
        
        return LobbyMapper.lobby_to_create_response(lobby)
    
    @staticmethod
    def join(lobby_id: str, request: LobbyJoinRequest) -> LobbyJoinResponse:
        lobby = LobbyService._get_existing_lobby(lobby_id)
        
        lobby_join_result = LobbyMapper.request_to_join_lobby(lobby, request.user)
        LobbyRepository.save(lobby_join_result.lobby)
        
        return LobbyMapper.lobby_to_join_response(lobby_join_result)
    
    @staticmethod
    def get(lobby_id) -> GetLobbyResponse:
        lobby = LobbyService._get_existing_lobby(lobby_id)
        return LobbyMapper.lobby_to_get_response(lobby)
    
    @staticmethod
    def update(lobby_id: str, request: LobbyUpdateRequest) -> LobbyUpdateResponse:
        lobby = LobbyService._get_existing_lobby(lobby_id)
        
        settings = lobby.settings
        
        if request.table_size is not None:
            if request.table_size < 2:
                raise ValidationException('La mesa debe tener al menos 2 asientos.')
            if request.table_size < max(lobby.occupied_positions):
                raise ValidationException(
                    f'La mesa debe tener al menos {max(lobby.occupied_positions)} asientos.'
                )
            settings.table_size = request.table_size
        
        if request.big_blind_value is not None:
            if request.big_blind_value < 2:
                raise ValidationException('La ciega grande debe ser al menos de 2 fichas.')
            if request.big_blind_value >= settings.initial_stack // 20:
                raise ValidationException(
                    f'Los jugadores no pueden quedar con menos de 20 ciegas grandes.'
                )
            settings.big_blind_value = request.big_blind_value
        
        if request.initial_stack is not None:
            if request.initial_stack < settings.big_blind_value * 20:
                raise ValidationException(
                    'El saldo inicial debe ser al menos de 20 ciegas grandes.'
                )
            settings.initial_stack = request.initial_stack
            for p in settings.players:
                p.stack = request.initial_stack
        
        if request.dealer_position is not None:
            if request.dealer_position not in lobby.occupied_positions:
                raise ValidationException(
                    'La posición del dealer debe estar entre los asientos ocupados.'
                )
            settings.dealer_position = request.dealer_position
        
        LobbyRepository.save(lobby)
        
        return LobbyMapper.lobby_to_create_response(lobby)
    
    @staticmethod
    def delete(lobby_id: str) -> None:
        LobbyService._get_existing_lobby(lobby_id)
        LobbyRepository.delete(lobby_id)
    
    @staticmethod
    def start_game(lobby_id: str) -> GameStartResponse:
        lobby = LobbyService._get_existing_lobby(lobby_id)
        game_start_request = LobbyMapper.lobby_to_game_start_request(lobby)
        
        if len(lobby.settings.table_size) > 10:
            raise ValidationException(
                'La cantidad de asientos en una mesa no puede ser mayor a 10.'
            )
        
        if len(lobby.settings.players) < 2:
            raise ValidationException(
                'Debe haber al menos 2 jugadores en la mesa para iniciar el juego.'
            )
        
        LobbyRepository.delete(lobby_id)
        return GameService.start(game_start_request)
