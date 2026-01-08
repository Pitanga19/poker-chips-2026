from typing import List, Optional
from app.core.exceptions import ValidationException
from app.modules.in_game.engine.game_states import PlayerState, PotState

def bet_chips(player: PlayerState, amount: int) -> None:
    # Apuesta fichas del stack al betting_stack si hay suficientes
    if amount > player.stack:
        raise ValidationException('Fichas insuficientes')
    
    player.stack -= amount
    player.betting_stack += amount

def return_bet_chips(player: PlayerState) -> None:
    # Devuelve las fichas apostadas al stack
    player.stack += player.betting_stack
    player.betting_stack = 0

def add_pot_to_list(pots: List[PotState], players: List[PlayerState]) -> None:
    # Agrega un nuevo pot a la lista de pots con los jugadores dados
    pots.append(
        PotState(
            size=0,
            players_in_pot=[p.id for p in players],
            pot_winners=[],
        )
    )

def reset_pot_list(pots: List[PotState]) -> None:
    # Resetea la lista de pots a un solo pot vacío
    pots.clear()
    add_pot_to_list(pots, [])

def transfer_to_pot(
    player: PlayerState,
    pot: PotState,
    amount: Optional[int] = None,
) -> None:
    """
    Transfiere fichas del betting_stack de cada jugador al pot
    
    - Si no se especifica amount, transfiere todo el betting_stack
    - Lanza ValidationException si amount > betting_stack
    """
    if amount is None:
        amount = player.betting_stack
    
    if amount > player.betting_stack:
        raise ValidationException('Fichas insuficientes')
    
    player.betting_stack -= amount
    pot.size += amount

def collect_to_pot(
    players: List[PlayerState],
    pot: PotState,
    amount: Optional[int] = None,
) -> None:
    """
    Recolecta fichas del betting_stack de cada jugador al pot
    Si no se especifica amount, recolecta todo el betting_stack
    """
    for p in players:
        transfer_to_pot(p, pot, amount)

def add_active_players_to_pot(pot: PotState, players: List[PlayerState]) -> None:
    # Agrega los IDs de los jugadores activos al pot.players_in_pot
    pot.players_in_pot.extend([p.id for p in players if p.is_active])
