from app.db.utils.enums import ActionType
from app.modules.in_game.engine.game_states import BetRoundState, GameState
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
    
    - Todos los jugadores activos han igualado la apuesta máxima
    - Todos los jugadores activos han checkeado (si la apuesta máxima es 0)
    - Queda 1 o ningún jugador activo
    """
    active = [
        p for p in game_state.players
        if p.id in game_state.pots[-1].players_in_pot
    ]
    
    # Terminar si queda 1 o ningún jugador activo
    if len(active) <= 1:
        return True
    
    max_bet = game_state.bet_round.current_max_bet
    
    # Terminar si todos checkearon
    if max_bet == 0:
        everyone_checked = all(p.last_action == ActionType.CHECK for p in active)
        return everyone_checked
    
    else:
        # Verificar que todos los jugadores activos (excepto los all-in) hayan igualado la apuesta máxima
        active_not_all_in = [p for p in active if p.last_action != ActionType.ALL_IN]
        active_not_all_in_called = all(p.betting_stack == max_bet for p in active_not_all_in)
        
        # Continuar si todavía debe actuar el big blind en pre-flop
        if game_state.hand.street == HandStreet.PRE_FLOP:
            bbp = game_state.hand.big_blind_position
            big_blind_player = game_state.players_by_position[bbp]
            bb_last_action = big_blind_player.last_action
            return active_not_all_in_called and bb_last_action != ActionType.PUT_BB
        
        # Terminar si todos igualaron la apuesta máxima
        return active_not_all_in_called