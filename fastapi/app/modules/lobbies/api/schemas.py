from pydantic import BaseModel, Field
from typing import Optional, List

class LobbyPlayerInfo(BaseModel):
    id: int = Field(..., description='ID del jugador')
    username: str = Field(..., description='Nombre de usuario del jugador')
    position: int = Field(..., description='Posición del jugador en la mesa')
    stack: int = Field(..., description='Saldo del jugador')

class UserInfo(BaseModel):
    id: int = Field(..., description='ID del usuario')
    username: str = Field(..., description='Nombre de usuario único')

class GameSettings(BaseModel):
    hoster_id: int = Field(..., description='ID del usuario que creó la sala')
    players: List[LobbyPlayerInfo] = Field(..., description='Jugadores en la sala')
    initial_stack: int = Field(..., description='Saldo inicial de cada jugador')
    table_size: int = Field(..., description='Cantidad de asientos de la mesa')
    small_blind_value: int = Field(..., description='Valor de la ciega pequeña para la mano')
    big_blind_value: int = Field(..., description='Valor de la ciega grande para la mano')
    dealer_position: Optional[int] = Field(
        default=None,
        description='Posición del dealer para la nueva mano. Al azar si no se proporciona.',
    )

class LobbyFullData(GameSettings):
    lobby_id: str = Field(..., description='ID único de la sala')

class LobbyCreateRequest(BaseModel):
    hoster_info: UserInfo = Field(..., description='Información del usuario que creó la sala')
    table_size: int = Field(..., description='Cantidad de asientos de la mesa')
    big_blind_value: int = Field(..., description='Valor de la ciega grande para la mano')
    initial_stack: int = Field(..., description='Saldo inicial de cada jugador')
    self_position: Optional[int] = Field(..., description='Posición del jugador en la mesa')

class LobbyCreateResponse(LobbyFullData):
    pass

class LobbyJoinRequest(BaseModel):
    user: UserInfo = Field(..., description='Información del usuario que quiere unirse')

class LobbyJoinResponse(LobbyFullData):
    joined_player: LobbyPlayerInfo = Field(..., description='Información del jugador que se unió')

class GetLobbyResponse(LobbyFullData):
    pass

class LobbyUpdateRequest(BaseModel):
    table_size: Optional[int] = Field(default=None, description='Cantidad de asientos de la mesa')
    big_blind_value: Optional[int] = Field(
        default=None, description='Valor de la ciega grande para la mano'
    )
    initial_stack: Optional[int] = Field(
        default=None, description='Saldo inicial de cada jugador'
    )
    dealer_position: Optional[int] = Field(
        default=None,
        description='Posición del dealer para la nueva mano. Al azar si no se proporciona.',
    )

class LobbyUpdateResponse(LobbyFullData):
    pass