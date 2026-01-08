from dataclasses import dataclass
from typing import List, Optional
from app.core.exceptions import ValidationException
from app.db.utils.enums import ActionType
from app.modules.in_game.engine.game_states import GameState, PlayerState
from app.modules.in_game.engine.utils.turn_utils import generate_turn
from app.modules.in_game.engine.utils.pot_utils import bet_chips

@dataclass
class ActionDescriptor:
    type: ActionType
    min_amount: Optional[int] = None
    max_amount: Optional[int] = None

class ActionManager:
    # Maneja las acciones que puede realizar un jugador.
    
    @staticmethod
    def get_available_actions(game_state: GameState) -> List[ActionDescriptor]:
        """
        Asume que:
        - Existe current_player
        - current_player.is_active == True
        - El estado de bet_round es consistente
        - Todos los jugadores tienen al menos 1bb en su stack
        """
        actions: List[ActionDescriptor] = []
        bet_round = game_state.bet_round
        player = game_state.current_player
        
        to_call = game_state.to_call
        big_blind_value = game_state.hand.big_blind_value
        current_max_bet = bet_round.current_max_bet
        has_chips_to_call = game_state.has_chips_to_call
        min_total_bet_to_raise = game_state.min_total_bet_to_raise
        has_chips_to_raise = game_state.has_chips_to_raise
        
        # Caso 1: Sin apuestas
        if current_max_bet == 0:
            actions.append(ActionDescriptor(ActionType.CHECK))
            if player.stack >= big_blind_value:
                actions.append(ActionDescriptor(
                    ActionType.BET,
                    min_amount=big_blind_value,
                    max_amount=player.stack,
                ))
            actions.append(ActionDescriptor(ActionType.ALL_IN))
            return actions
        
        # Caso 2: Con apuestas - BB sin actuar
        if to_call == 0:
            actions.append(ActionDescriptor(ActionType.CHECK))
            if has_chips_to_raise:
                actions.append(ActionDescriptor(
                    ActionType.RAISE,
                    min_amount=min_total_bet_to_raise,
                    max_amount=player.total_stack,
                ))
            else:
                actions.append(ActionDescriptor(ActionType.ALL_IN))
            return actions
        
        # Caso 3: Con apuestas - Debe igualar
        actions.append(ActionDescriptor(ActionType.FOLD))
        
        if has_chips_to_call:
            actions.append(ActionDescriptor(ActionType.CALL))
        else:
            actions.append(ActionDescriptor(ActionType.ALL_IN))
            return actions
        
        if has_chips_to_raise:
            actions.append(ActionDescriptor(
                ActionType.RAISE,
                min_amount=min_total_bet_to_raise,
                max_amount=player.total_stack,
            ))
        else:
            actions.append(ActionDescriptor(ActionType.ALL_IN))
        return actions
    
    @staticmethod
    def apply_action(
        game_state: GameState, action: ActionType, amount: Optional[int] = None
    ) -> None:
        """
        Aplica la acción recibida a los estados de juego
        
        Asume que:
        - Esta acción viene de get_available_actions()
        - Amount es válido para la acción (si aplica)
        """
        player: PlayerState
        
        match action:
            case ActionType.FOLD:
                player = ActionManager._fold(game_state)
            case ActionType.CHECK:
                player = ActionManager._check(game_state)
            case ActionType.CALL:
                player = ActionManager._call(game_state)
            case ActionType.BET:
                player = ActionManager._bet(game_state, amount)
            case ActionType.RAISE:
                player = ActionManager._raise(game_state, amount)
            case ActionType.ALL_IN:
                player = ActionManager._all_in(game_state)
            case _:
                raise ValidationException(f'Acción inválida: {action}')
        
        game_state.last_turn = generate_turn(player, amount)
    
    @staticmethod
    def post_blinds(game_state: GameState) -> None:
        """
        Publica las ciegas obligatorias al inicio de una mano.
        
        Asume que:
        - hand.dealer_position ya está definido
        - bet_round fue reseteado previamente
        - current_player se resuelve a partir de current_turn_position
        
        Deja el bet_round en estado válido para iniciar el preflop.
        """
        hand = game_state.hand
        bet_round = game_state.bet_round
        
        bet_round.current_turn_position = hand.small_blind_position
        ActionManager._put_small_blind(game_state)
        
        bet_round.current_turn_position = hand.big_blind_position
        big_blind_player = ActionManager._put_big_blind(game_state)
        
        game_state.last_turn = generate_turn(big_blind_player, hand.big_blind_value)
    
    @staticmethod
    def _put_small_blind(game_state: GameState) -> PlayerState:
        # No modifica bet_round: solo descuenta fichas y registra la acción
        player = game_state.current_player
        small_blind_value = game_state.hand.small_blind_value
        
        bet_chips(player, small_blind_value)
        player.last_action = ActionType.PUT_SB
        
        return player
    
    @staticmethod
    def _put_big_blind(game_state: GameState) -> PlayerState:
        # Define la apuesta viva inicial de la ronda
        player = game_state.current_player
        bet_round = game_state.bet_round
        big_blind_value = game_state.hand.big_blind_value
        
        bet_round.current_max_bet = big_blind_value
        bet_round.last_valid_bet = big_blind_value
        bet_round.last_raise_amount = big_blind_value
        bet_round.last_raiser_position = player.position
        bet_round.has_voluntary_bet = False
        
        bet_chips(player, big_blind_value)
        player.last_action = ActionType.PUT_BB
        
        return player
    
    @staticmethod
    def _fold(game_state: GameState) -> PlayerState:
        player = game_state.current_player
        
        player.is_active = False
        player.last_action = ActionType.FOLD
        
        for pot in game_state.pots:
            if player.id in pot.players_in_pot:
                pot.players_in_pot.remove(player.id)
        
        return player
    
    @staticmethod
    def _check(game_state: GameState) -> PlayerState:
        player = game_state.current_player
        
        player.last_action = ActionType.CHECK
        
        return player
    
    @staticmethod
    def _call(game_state: GameState) -> PlayerState:
        player = game_state.current_player
        to_call = game_state.to_call
        
        bet_chips(player, to_call)
        player.last_action = ActionType.CALL
        
        return player
    
    @staticmethod # Recibe amount: Cantidad total que el jugador dejará en la mesa
    def _bet(game_state: GameState, amount: int) -> PlayerState:
        player = game_state.current_player
        bet_round = game_state.bet_round
        big_blind_value = game_state.hand.big_blind_value
        
        if amount < big_blind_value:
            raise ValidationException(
                f'La apuesta mínima es {big_blind_value}'
            )
        
        bet_chips(player, amount)
        player.last_action = ActionType.BET
        
        bet_round.current_max_bet = amount
        bet_round.last_valid_bet = amount
        bet_round.last_raise_amount = amount
        bet_round.last_raiser_position = player.position
        bet_round.has_voluntary_bet = True
        
        return player
    
    @staticmethod # Recibe final_amount: Cantidad total que el jugador dejará en la mesa
    def _raise(game_state: GameState, final_amount: int) -> PlayerState:
        player = game_state.current_player
        bet_round = game_state.bet_round
        
        # incremento real sobre lo ya apostado
        raise_amount = final_amount - bet_round.last_valid_bet
        
        # lo que le falta al jugador para raisear
        player_to_raise_amount = final_amount - player.betting_stack
        total_min_raise = bet_round.last_valid_bet + bet_round.last_raise_amount
        
        if final_amount < total_min_raise:
            raise ValidationException(
                f'La subida mínima es {total_min_raise}'
            )
        
        bet_chips(player, player_to_raise_amount)
        player.last_action = ActionType.RAISE
        
        bet_round.current_max_bet = final_amount
        bet_round.last_valid_bet = final_amount
        bet_round.last_raise_amount = raise_amount
        bet_round.last_raiser_position = player.position
        bet_round.has_voluntary_bet = True
        
        return player
    
    @staticmethod
    def _all_in(game_state: GameState) -> PlayerState:
        player = game_state.current_player
        total_bet = player.stack + player.betting_stack
        bet_round = game_state.bet_round
        
        if total_bet > bet_round.current_max_bet:
            min_total_raise = bet_round.current_max_bet + bet_round.last_raise_amount
            
            if total_bet >= min_total_raise:
                raise_amount = total_bet - bet_round.current_max_bet
                
                bet_round.last_raise_amount = raise_amount
                bet_round.last_valid_bet = total_bet
                bet_round.last_raiser_position = player.position
            
            bet_round.current_max_bet = total_bet
            bet_round.has_voluntary_bet = True
        
        bet_chips(player, player.stack)
        player.last_action = ActionType.ALL_IN
        
        return player
