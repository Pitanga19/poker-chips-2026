from app.db.tables.hands.schemas import HandStreet
from app.modules.sessions.engine.game_states import HandState

orderly_hands_street = [
    HandStreet.PRE_FLOP,
    HandStreet.FLOP,
    HandStreet.TURN,
    HandStreet.RIVER,
    HandStreet.WINNER_SELECTION,
    HandStreet.FINISHED,
]

def get_next_street(street: HandStreet) -> HandStreet:
    # Obtiene la siguiente calle en orden
    current_index = orderly_hands_street.index(street)
    
    if current_index == len(orderly_hands_street) - 1:
        return street
    
    return orderly_hands_street[current_index + 1]

def advance_hand_street(hand: HandState) -> None:
    # Avanza la calle del estado de la mano a la siguiente
    hand.street = get_next_street(hand.street)
