from dataclasses import dataclass
from typing import List
from app.core.exceptions import ValidationException
from app.modules.sessions.engine.game_states import GameState
from app.modules.sessions.engine.managers.pot_manager import PotManager, PayoutDescription

@dataclass
class ShowdownPotInfo:
    # Información que se expone al usuario/UI para resolver el showdown.
    pot_index: int
    pot_size: int
    players_in_pot: List[int]  # player_ids

@dataclass
class ShowdownPotWinners:
    pot_index: int
    pot_winners_ids: List[int]

class ShowdownManager:
    """
    Responsabilidades:
    - Exponer información de pots y jugadores elegibles
    - Validar ganadores enviados por el usuario
    - Delegar la distribución de premios al PotManager
    
    Asume que:
    - Los pots ya están correctamente construidos (side-pots incluidos)
    - No hay más acciones posibles (fin de mano)
    - La UI provee ganadores válidos, pero el engine valida igual
    """
    
    @staticmethod
    def get_showdown_info(game_state: GameState) -> List[ShowdownPotInfo]:
        """
        Devuelve los pots con los jugadores que pueden ganarlos.
        Esto se usa para que la UI muestre opciones válidas.
        """
        showdown_info: List[ShowdownPotInfo] = []
        
        for i, pot in enumerate(game_state.pots):
            showdown_info.append(
                ShowdownPotInfo(
                    pot_index=i,
                    pot_size=pot.size,
                    players_in_pot=pot.players_in_pot,
                )
            )
        
        return showdown_info
    
    @staticmethod
    def resolve(
        game_state: GameState,
        pots_winners: List[ShowdownPotWinners],
    ) -> List[PayoutDescription]:
        """
        Valida y asigna los ganadores por pot, luego distribuye premios.
        
        Asume que:
        - pot_winners cubre todos los pots existentes
        - los winners provienen de opciones ofrecidas por el engine
        """
        
        pots = game_state.pots
        
        # Verificar que se definieron ganadores para todos los pots
        if len(pots_winners) != len(pots):
            raise ValidationException('No se definieron ganadores para todos los pots')
        
        for pw in pots_winners:
            pot_index = pw.pot_index
            winners = pw.pot_winners_ids
            
            # Pot válido
            if pot_index < 0 or pot_index >= len(pots):
                raise ValidationException(f'Pot inválido: {pot_index}')
            
            pot = pots[pot_index]
            
            if not winners:
                raise ValidationException(
                    f'El pot {pot_index} no tiene ganadores definidos'
                )
            
            allowed_ids = set(pot.players_in_pot)
            
            # Validar que todos los winners pertenecen al pot
            for wid in winners:
                if wid not in allowed_ids:
                    raise ValidationException(
                        f'Jugador {wid} no pertenece al pot {pot_index}'
                    )
            
            # Asignar ganadores al pot
            pot.pot_winners = winners
        
        # Delegar distribución final al PotManager
        return PotManager.distribute_pots(game_state)
