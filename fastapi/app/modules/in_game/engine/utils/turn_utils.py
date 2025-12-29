from typing import Optional, List
from app.core.exceptions import ValidationException
from app.db.tables.hands.schemas import HandStreet
from app.modules.in_game.engine.game_states import PlayerState, TurnState, HandState

def generate_turn(
    player: PlayerState,
    amount: Optional[int] = None,
) -> TurnState:
    # Genera un TurnState basado en la última acción del jugador
    return TurnState(
        player_id=player.id,
        player_position=player.position,
        action=player.last_action,
        amount=amount,
    )

def get_start_position_for_round(hand: HandState) -> int:
    """
    Obtiene la posición desde la cual se busca el primero en actuar
    
    - En PRE_FLOP, es la posición del big blind
    - En otras calles, es la posición del dealer
    """
    if hand.street == HandStreet.PRE_FLOP:
        return hand.big_blind_position
    
    return hand.dealer_position

def get_first_to_act_position(
    hand: HandState,
    players: List[PlayerState],
) -> Optional[int]:
    """
    Obtiene la posición del primer jugador que debe actuar en la ronda actual
    """
    if sum(1 for p in players if p.can_act) < 2:
        return None
    
    start_position = get_start_position_for_round(hand)
    sorted_players = sorted(players, key=lambda p: p.position)
    
    start_index = next(
        (i for i, p in enumerate(sorted_players) if p.position == start_position),
        None,
    )
    
    if start_index is None:
        raise ValidationException('Posición de inicio inválida')
    
    for p in (
        sorted_players[start_index + 1 :]
        + sorted_players[: start_index + 1]
    ):
        if p.can_act and p.last_action is None:
            return p.position
    
    return None

def get_can_act_positions(players: List[PlayerState]) -> List[int]:
    """
    Obtiene las posiciones de los jugadores que pueden actuar en la ronda actual
    Asume players ordenados por posición de mesa
    """
    return [p.position for p in players if p.can_act]

def get_next_can_act_position(
    current_position: int,
    players: List[PlayerState],
) -> Optional[int]:
    """
    Obtiene la siguiente posición que puede actuar después de la posición actual
    en la lista de jugadores que pueden actuar
    """
    can_act_positions = get_can_act_positions(players)
    
    if not can_act_positions:
        return None
    
    # Buscar circularmente desde la posición actual
    sorted_positions = sorted(can_act_positions)
    
    for pos in sorted_positions:
        if pos > current_position:
            return pos
    
    # wrap around
    return sorted_positions[0]
