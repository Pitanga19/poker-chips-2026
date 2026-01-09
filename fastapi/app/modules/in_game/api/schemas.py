from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID
from app.db.utils.enums import ActionType
from app.db.tables.hands.schemas import HandStreet
from app.modules.in_game.engine.utils.enums import BetRoundResult

# Esquemas Pydantic copiados de los dataclasses usados en la lógica del motor de juego
class ActionDescriptorView(BaseModel):
    type: ActionType = Field(..., description='Tipo de acción disponible')
    min_amount: Optional[int] = Field(
        None, description='Cantidad mínima para la acción, si aplica'
    )
    max_amount: Optional[int] = Field(
        None, description='Cantidad máxima para la acción, si aplica'
    )

class PotInfoView(BaseModel):
    pot_index: int = Field(..., description='Índice del pot')
    pot_size: int = Field(..., description='Tamaño del pot')
    players_in_pot: List[int] = Field(..., description='IDs de los jugadores en el pot')

class ShowdownPotWinnersView(BaseModel):
    pot_index: int = Field(..., description='Índice del pot')
    pot_winners_ids: List[int] = Field(..., description='IDs de los jugadores ganadores del pot')

class PayoutDescriptionView(BaseModel):
    player_id: int = Field(..., description='ID del jugador')
    amount_won: int = Field(..., description='Cantidad ganada por el jugador')

class ToCreatePlayerInfo(BaseModel):
    id: int = Field(..., description='ID del jugador')
    username: str = Field(..., description='Nombre de usuario del jugador')
    position: int = Field(..., description='Posición del jugador en la mesa')
    stack: int = Field(..., description='Saldo del jugador')

class InGamePlayerInfo(ToCreatePlayerInfo):
    betting_stack: int = Field(
        ..., description='Cantidad apostada en la mano actual por el jugador'
    )
    is_active: bool = Field(..., description='Indica si el jugador está activo en la mano')

class LastActionView(BaseModel):
    player: InGamePlayerInfo = Field(..., description='Información del jugador que hizo la acción')
    action: ActionType = Field(..., description='Tipo de acción realizada')
    amount: Optional[int] = Field(None, description='Cantidad asociada a la acción, si aplica')

class BetRoundResultView(BaseModel):
    status: BetRoundResult = Field(..., description='Resultado después de realizar la acción')
    prev_street: HandStreet = Field(..., description='Calle de la mano antes de la acción')
    new_street: HandStreet = Field(..., description='Calle actual de la mano, después de la acción')

# Esquemas para las solicitudes y respuestas de la API
class GameStartRequest(BaseModel):
    table_size: int = Field(..., description='Cantidad de asientos de la mesa')
    players: List[ToCreatePlayerInfo] = Field(
        ..., description='Lista de jugadores que participarán en la mano'
    )
    small_blind_value: int = Field(..., description='Valor de la ciega pequeña para la mano')
    big_blind_value: int = Field(..., description='Valor de la ciega grande para la mano')
    dealer_position: Optional[int] = Field(
        None,
        description='Posición del dealer para la nueva mano. Al azar si no se proporciona.'
    )

class GameStartResponse(BaseModel):
    game_id: UUID = Field(..., description='ID único del juego iniciado')
    table_size: int = Field(..., description='Cantidad de asientos de la mesa')
    street: HandStreet = Field(..., description='Calle actual de la mano')
    dealer_id: int = Field(..., description='ID del jugador que es el dealer')
    small_blind_id: int = Field(..., description='ID del jugador que puso la ciega pequeña')
    big_blind_id: int = Field(..., description='ID del jugador que puso la ciega grande')
    current_player_id: int = Field(..., description='ID del jugador actual')
    players: List[InGamePlayerInfo] = Field(
        ..., description='Información de los jugadores en la mano'
    )
    pots: List[PotInfoView] = Field(..., description='Pots actuales en la mano')

class GameRenderResponse(GameStartResponse):
    waiting_for_action: bool = Field(..., description='Indica si se está esperando una acción')
    is_showdown: bool = Field(..., description='Indica si se está en el showdown')
    last_action: Optional[LastActionView] = Field(
        None, description='Última acción realizada en la mano'
    )

class AvailableActionsResponse(BaseModel):
    player: InGamePlayerInfo = Field(..., description='Información del jugador actual')
    actions: List[ActionDescriptorView] = Field(
        ..., description='Lista de acciones disponibles para el jugador actual'
    )

class PlayerActionRequest(BaseModel):
    player_id: int = Field(..., description='ID del jugador que está realizando la acción')
    action: ActionType = Field(..., description='Tipo de acción que el jugador desea realizar')
    amount: Optional[int] = Field(None, description='Cantidad asociada a la acción, si aplica')

class PlayerActionResponse(BaseModel):
    bet_round_result: BetRoundResultView = Field(
        ..., description='Resultado de la ronda de apuestas tras la acción'
    )
    last_action: LastActionView = Field(..., description='Última acción realizada en la mano')
    pots: List[PotInfoView] = Field(..., description='Pots actuales en la mano')
    next_available_actions: Optional[AvailableActionsResponse] = Field(
        default=None, description='Acciones disponibles después de realizar la acción'
    )

class ShowdownInfoResponse(BaseModel):
    pots_to_resolve: List[PotInfoView] = Field(..., description='Pots a resolver')

class ShowdownResolveRequest(BaseModel):
    pots_winners: List[ShowdownPotWinnersView] = Field(
        ..., description='Lista de ganadores por pot para resolver el showdown'
    )

class ShowdownResolveResponse(BaseModel):
    payout_descriptions: List[PayoutDescriptionView] = Field(
        ..., description='Descripciones de los pagos realizados a los jugadores'
    )
