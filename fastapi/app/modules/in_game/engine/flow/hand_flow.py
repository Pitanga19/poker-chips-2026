from typing import Optional, List
from app.core.exceptions import ValidationException
from app.db.tables.hands.schemas import HandStreet
from app.modules.in_game.engine.game_states import GameState
from app.modules.in_game.engine.flow.bet_round_flow import BetRoundFlow
from app.modules.in_game.engine.managers.action_manager import ActionManager
from app.modules.in_game.engine.managers.showdown_manager import ShowdownManager, ShowdownPotWinners
from app.modules.in_game.engine.utils.enums import HandResult
from app.modules.in_game.engine.utils.player_reset import hand_players_reset
from app.modules.in_game.engine.utils.pot_utils import add_can_act_players_to_pot
from app.modules.in_game.engine.utils.hand_utils import (
    handle_dealer_selection,
    hand_state_reset,
)

class HandFlow:
    """
    HandFlow maneja la dinámica de una mano completa
    
    Responsabilidades:
    - Seleccionar / avanzar dealer
    - Resetear estados de mano
    - Iniciar y avanzar calles (preflop → flop → turn → river)
    - Decidir cuándo una mano termina automáticamente
    - Delegar resolución final al ShowdownManager
    
    No:
    - Valida acciones
    - Decide ganadores
    - Maneja lógica de apuestas finas
    """
    
    @staticmethod
    def start(
        game_state: GameState,
        dealer_position: Optional[int] = None,
    ) -> None:
        """
        Inicia una nueva mano.
        
        Dealer:
        - Si se recibe dealer_position → se usa (primera mano manual)
        - Si NO se recibe:
            - Si no hay dealer previo → se elige uno al azar entre can_act
            - Si hay dealer previo → se avanza al siguiente elegible
        
        Flujo:
        - Resetear estado de mano
        - Seleccionar dealer
        - Postear ciegas
        - Iniciar ronda de apuestas preflop
        """
        
        # Reset completo de los jugadores para una nueva mano
        hand_players_reset(game_state.players, game_state.hand.big_blind_value)
        
        # Reset completo del estado de mano
        hand_state_reset(game_state.hand, game_state.players)
        
        # Selección / avance de dealer (helper puro)
        handle_dealer_selection(game_state.hand, dealer_position)
        
        # Agregar los jugadores que pueden actuar al main pot
        add_can_act_players_to_pot(game_state.pots[0], game_state.players)
        
        # Posteo de ciegas (no definido acá, solo llamado)
        ActionManager.post_blinds(game_state)
        
        # Iniciar primera ronda de apuestas
        BetRoundFlow.start(game_state)
    
    @staticmethod
    def after_bet_round(game_state: GameState) -> HandResult:
        """
        Se llama cuando una ronda de apuestas finaliza.
        
        Decide:
        - Si la mano termina automáticamente
        - Si corresponde showdown
        - O si se avanza a la siguiente calle
        """
        
        if not game_state.pots:
            raise ValidationException('No existen pots al finalizar la ronda')
        
        # Solo importa el último pot, los anteriores ya están cerrados (side-pots por all-in)
        last_pot = game_state.pots[-1]
        
        # Caso 1: último pot tiene un solo jugador → mano finalizada automáticamente
        if len(last_pot.players_in_pot) == 1:
            return HandResult.AUTO_WIN
        
        # Caso 2: se terminó el river → showdown
        if game_state.hand.street == HandStreet.RIVER:
            return HandResult.SHOWDOWN
        
        # Caso 3: avanzar calle e iniciar nueva ronda
        return HandResult.NEXT_STREET
    
    @staticmethod
    def finish(game_state: GameState) -> None:
        """
        Finaliza la mano
        
        Responsabilidades:
        - Resolver ganadores (manual o automático)
        - Distribuir premios
        - Dejar el estado listo para la próxima mano
        
        Importante:
        - NO mueve el dealer
        - NO inicia la siguiente mano
        
        NOTA: Cuando AUTO_WIN y SHOWDOWN diverjan, refactorizar con match
        """
        
        # Indicar street de selección de ganadores
        game_state.hand.street = HandStreet.WINNER_SELECTION
        
        # Obtener información de showdown para la UI
        showdown_info = ShowdownManager.get_showdown_info(game_state)
        
        # Si todos los pots tienen un solo jugador, la resolución es automática
        auto_resolve = all(
            len(info.players_in_pot) == 1 for info in showdown_info
        )
        
        if auto_resolve:
            showdown_pot_winners: List[ShowdownPotWinners] = []
            # Seteo automático de ganadores
            for i, info in enumerate(showdown_info):
                pot = game_state.pots[i]
                pot.pot_winners = info.players_in_pot
                showdown_pot_winners.append(
                    ShowdownPotWinners(pot_index=i, pot_winners_ids=info.players_in_pot)
                )
            
            # Distribución directa
            ShowdownManager.resolve(game_state, showdown_pot_winners)
            return
        
        # Caso interactivo:
        # La UI debe:
        # 1. Mostrar showdown_info
        # 2. Enviar winners por pot
        #
        # HandFlow NO continúa automáticamente desde acá
        # Se espera una llamada explícita a ShowdownManager.resolve(...)
        return
