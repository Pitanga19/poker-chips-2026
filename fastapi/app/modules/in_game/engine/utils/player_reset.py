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

def reset_active_players(players: List[PlayerState], big_blind_value: int) -> None:
    """
    Resetea is_active de los jugadores basado en si el jugador tiene stack >= big_blind_value
    Se debe utilizar únicamente al iniciar una nueva mano
    """
    for p in players:
        p.is_active = p.stack >= big_blind_value

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
    - Resetea is_active basado en stack >= big_blind_value
    """
    bet_round_players_state_reset(players)
    reset_active_players(players, big_blind_value)
