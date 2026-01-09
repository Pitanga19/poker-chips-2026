from app.db.utils.enums import ActionType
from app.modules.sessions.engine.game_states import BetRoundState, GameState
from app.db.tables.hands.schemas import HandStreet

def bet_round_state_reset(bet_round: BetRoundState) -> None:
    bet_round.current_turn_position = None
    bet_round.current_max_bet = 0
    bet_round.last_valid_bet = 0
    bet_round.last_raise_amount = 0
    bet_round.last_raiser_position = None
    bet_round.has_voluntary_bet = False

def bet_round_finished(game_state: GameState) -> bool:
    """
    Evaluar condiciones para terminar la ronda de apuestas actual
    Se toma como referencia los jugadores que pueden actuar en el pot actual
    - Todos los jugadores han checkeado (si la apuesta máxima es 0)
    - Todos los jugadores han igualado la apuesta máxima
    - Queda 1 o ningún jugador activo
    """
    active_players = game_state.active_players
    
    # Terminar si queda 1 o ningún jugador activo
    if len(active_players) <= 1:
        return True
    
    can_act_players = game_state.can_act_players
    max_bet = game_state.bet_round.current_max_bet
    
    # Si no hubo apuestas...
    if max_bet == 0:
        # Evaluar que todos hayan actuado
        everyone_has_act = all(p.has_act for p in can_act_players)
        return everyone_has_act
    
    # Si hubo apuestas...
    else:
        # Verificar que todos los jugadores activos que puedan hayan igualado
        can_call_players = [p for p in active_players if p.total_stack >= max_bet]
        can_call_called = all(p.betting_stack == max_bet for p in can_call_players)
        
        # Verificar que todos los jugadores activos que no lleguen a igualar hayan apostado todo
        cannot_call_players = [p for p in active_players if p.total_stack < max_bet]
        cannot_call_all_in = all(p.stack == 0 for p in cannot_call_players)
        
        # Todos los jugadores apostaron el máximo posible para igualar la apuesta
        everyone_try_called = can_call_called and cannot_call_all_in
        
        # Continuar si todavía debe actuar el big blind en pre-flop
        if game_state.hand.street == HandStreet.PRE_FLOP:
            bbp = game_state.hand.big_blind_position
            big_blind_player = game_state.players_by_position[bbp]
            bb_last_action = big_blind_player.last_action
            return everyone_try_called and bb_last_action != ActionType.PUT_BB
        
        # Terminar si todos intentaron igualar la apuesta máxima
        return everyone_try_called