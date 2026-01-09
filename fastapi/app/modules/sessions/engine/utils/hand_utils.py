from typing import List, Optional
from app.db.tables.hands.schemas import HandStreet
from app.modules.sessions.engine.game_states import HandState, PlayerState
from app.modules.sessions.engine.utils.position_utils import (
    get_random_position,
    get_next_position,
)

def handle_dealer_selection(
    hand: HandState,
    dealer_position: Optional[int] = None,
) -> None:
    """
    Maneja la selección del dealer para la mano actual
    
    - Si se proporciona dealer_position, se establece directamente
    - Si no se proporciona y no hay dealer asignado, se selecciona uno aleatorio
    - Si ya había un dealer, se avanza al siguiente en la lista de posiciones que pueden actuar
    """
    if dealer_position is not None:
        hand.dealer_position = dealer_position
        return
    
    if hand.dealer_position is None:
        hand.dealer_position = get_random_position(hand.active_positions)
        return
    
    hand.dealer_position = get_next_position(
        hand.dealer_position,
        hand.active_positions,
    )

def hand_state_reset(
    hand: HandState,
    players: List[PlayerState],
) -> None:
    """
    Resetea los valores del estado de la mano para iniciar una nueva
    """
    hand.street = HandStreet.PRE_FLOP
    hand.active_positions = [p.position for p in players if p.is_active]
