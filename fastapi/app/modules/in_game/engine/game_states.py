from dataclasses import dataclass, field
from typing import List, Optional, Dict
from uuid import UUID
# Action: 'put-sb', 'put-bb', 'check', 'call', 'bet', 'raise', 'all-in', 'must-all-in', 'fold'
from app.db.utils.enums import ActionType
# Street: 'pre-flop', 'flop', 'turn', 'river', 'winner-selection', 'finished'
from app.db.tables.hands.schemas import HandStreet
from app.modules.in_game.engine.utils.position_utils import get_next_position
from app.modules.in_game.engine.utils.log_types import ActionLogEntry

@dataclass
class PlayerState:
    id: int
    username: str
    position: int
    stack: int # Saber si tiene para seguir jugando
    
    betting_stack: int = 0 # Comparar con current_max_bet
    can_act: bool = True # Saber si hay que pedirle acción ('all-in', 'fold' -> can_act=False)
    last_action: Optional[ActionType] = None # Saber si está fold / all-in
    
    @property
    def total_stack(self) -> int:
        return self.stack + self.betting_stack

@dataclass
class PotState:
    size: int
    players_in_pot: List[int] # Lista de IDs
    pot_winners: List[int] # Lista de IDs

@dataclass
class TurnState:
    player_id: int
    player_position: int
    action: ActionType
    
    amount: Optional[int] = None

@dataclass
class BetRoundState:
    current_max_bet: int = 0 # Apuesta a igualar en esta ronda
    current_turn_position: Optional[int] = None # Se define en base al dealer_position
    
    last_valid_bet: int = 0 # Última apuesta válida
    last_raise_amount: int = 0 # Monto a subir sobre la última apuesta válida
    last_raiser_position: Optional[int] = None # Se define cuando alguien apuesta
    
    has_voluntary_bet: bool = False # Indica si el agresor hizo una apuesta voluntaria

@dataclass
class HandState:
    street: HandStreet
    small_blind_value: int
    big_blind_value: int
    
    can_act_positions: List[int] = field(default_factory=list) # Posiciones que juegan
    dealer_position: Optional[int] = None # Posición del dealer
    
    @property
    def small_blind_position(self) -> Optional[int]:
        if self.dealer_position is None:
            return None
        return get_next_position(self.dealer_position, self.can_act_positions)
    
    @property
    def big_blind_position(self) -> Optional[int]:
        if self.dealer_position is None:
            return None
        return get_next_position(self.small_blind_position, self.can_act_positions)

@dataclass
class GameState:
    id: UUID
    players: List[PlayerState]
    pots: List[PotState]
    hand: HandState
    bet_round: BetRoundState
    
    action_logs: List[ActionLogEntry] = field(default_factory=list)
    next_log_sequence: int = 1
    
    last_turn: Optional[TurnState] = None
    
    players_by_id: Dict[int, PlayerState] = field(init=False)
    players_by_position: Dict[int, PlayerState] = field(init=False)
    
    def __post_init__(self):
        self.rebuild_player_indexes()
    
    def rebuild_player_indexes(self):
        self.players_by_id = {p.id: p for p in self.players}
        self.players_by_position = {p.position: p for p in self.players}
    
    @property
    def current_player(self) -> PlayerState:
        ctp = self.bet_round.current_turn_position
        return self.players_by_position[ctp]
    
    @property
    def to_call(self) -> int:
        return max(0, self.bet_round.current_max_bet - self.current_player.betting_stack)
    
    @property
    def has_chips_to_call(self) -> bool:
        return self.current_player.stack >= self.to_call
    
    @property
    def min_total_bet_to_raise(self) -> int:
        return self.bet_round.current_max_bet + self.bet_round.last_raise_amount
    
    @property
    def to_raise(self) -> int:
        return max(0, self.min_total_bet_to_raise - self.current_player.betting_stack)
    
    @property
    def has_chips_to_raise(self) -> bool:
        return self.current_player.stack >= self.to_raise
