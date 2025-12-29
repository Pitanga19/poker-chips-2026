from dataclasses import dataclass
from random import randint
from typing import List
from app.core.exceptions import ValidationException
from app.db.utils.enums import ActionType
from app.modules.in_game.engine.game_states import GameState
from app.modules.in_game.engine.utils.pot_utils import (
    return_bet_chips,
    collect_to_pot,
    add_pot_to_list,
)

@dataclass
class PayoutDescription:
    player_id: int
    amount_won: int

class PotManager:
    """
    Funciones para:
    - recolectar betting_stack de cada jugador a los pots (incluye side-pots)
    - distribuir payouts a base de pot.pot_winners (lista de player ids por pot)
    """
    
    @staticmethod
    def collect_bets_into_pots(game_state: GameState) -> None:
        """
        Asume que:
        - Existe al menos un pot inicial
        - El último pot es el activo
        - betting_stack refleja correctamente lo apostado en la ronda
        """
        players = game_state.players
        pots = game_state.pots  # referencia directa
        
        # Recolectar apuestas de jugadores foldeados antes de crear side-pots
        folded_with_betting_stack = [
            p for p in players
            if p.last_action == ActionType.FOLD and p.betting_stack > 0
        ]
        collect_to_pot(folded_with_betting_stack, pots[-1])
        
        betting_players = [p for p in players if p.betting_stack > 0]
        betting_players.sort(key=lambda p: p.betting_stack)
        
        while len(betting_players) > 1:
            # Todos apostaron lo mismo
            if betting_players[0].betting_stack == betting_players[-1].betting_stack:
                # pots[-1] es el pot activo
                collect_to_pot(betting_players, pots[-1])
                break
            
            # Side-pot
            min_amount = betting_players[0].betting_stack
            
            betting_players = collect_to_pot(
                betting_players,
                pots[-1],
                min_amount
            )
            
            if len(betting_players) > 1:
                add_pot_to_list(pots, betting_players)  # muta la lista
        
        # Devolver betting_stack si queda un solo jugador
        if len(betting_players) == 1:
            return_bet_chips(betting_players[0])
    
    @staticmethod
    def distribute_pots(game_state: GameState) -> List[PayoutDescription]:        
        """
        Distribuye los pots según pot.pot_winners. Cada pot.pot_winners debe ser una lista de IDs
        ganadores (1 o más en caso de empate). Retorna lista de PayoutDescription
        Nota: en caso de empate dividir proporcionalmente por numero de winners (entero division)
        y distribuir reminder al azar
        """
        pots = game_state.pots
        payouts: List[PayoutDescription] = []
        players_by_id = game_state.players_by_id
        
        for pot in pots:
            if not pot.pot_winners:
                raise ValidationException('No se definieron ganadores para este pozo')
            
            per_winner = pot.size // len(pot.pot_winners)
            remainder = pot.size - per_winner * len(pot.pot_winners)
            
            for wid in pot.pot_winners:
                to_add = per_winner
                found = False
                
                for p in payouts:
                    if p.player_id == wid:
                        p.amount_won += to_add
                        found = True
                        break
                
                if not found:
                    payouts.append(PayoutDescription(player_id=wid, amount_won=to_add))
                
                # Agregar la suma ganada al stack del jugador
                players_by_id[wid].stack += to_add
            
            # Distribuir remainder al azar
            while remainder > 0:
                random_wid = pot.pot_winners[randint(0, len(pot.pot_winners) - 1)]
                
                for p in payouts:
                    if p.player_id == random_wid:
                        p.amount_won += 1
                        break
                
                players_by_id[random_wid].stack += 1
                remainder -= 1
        
        return payouts
