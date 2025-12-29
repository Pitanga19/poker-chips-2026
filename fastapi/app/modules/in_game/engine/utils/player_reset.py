from typing import List
from app.modules.in_game.engine.game_states import PlayerState, PotState

def reset_players_betting_stack(players: List[PlayerState]) -> None:
    # Resetea el betting_stack de los jugadores a 0
    for p in players:
        p.betting_stack = 0

def reset_players_last_action(players: List[PlayerState]) -> None:
    # Resetea la última acción de los jugadores a None
    for p in players:
        p.last_action = None

def reset_players_can_act(players: List[PlayerState], big_blind_value: int) -> None:
    """
    Resetea can_act basado en si el jugador tiene stack >= big_blind_value
    Se debe utilizar únicamente al iniciar una nueva mano
    """
    for p in players:
        p.can_act = p.stack >= big_blind_value

def bet_round_players_state_reset(players: List[PlayerState]) -> None:
    """
    Resetea los estados de los jugadores para una nueva ronda de apuestas
    
    - betting_stack a 0
    - last_action a None
    """
    reset_players_betting_stack(players)
    reset_players_last_action(players)

def hand_players_reset(players: List[PlayerState], big_blind_value: int) -> None:
    """
    Resetea los estados de los jugadores para una nueva mano
    
    - Resetea el estado de la ronda de apuestas
    - Resetea can_act basado en stack >= big_blind_value
    """
    bet_round_players_state_reset(players)
    reset_players_can_act(players, big_blind_value)

def set_players_can_act_from_last_pot(
    players: List[PlayerState],
    pots: List[PotState],
) -> None:
    last_pot_players = set(pots[-1].players_in_pot)
    for p in players:
        p.can_act = p.id in last_pot_players and p.stack > 0
