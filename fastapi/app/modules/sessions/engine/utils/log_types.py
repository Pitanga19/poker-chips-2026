from dataclasses import dataclass
from typing import Optional, List, Any
from enum import Enum
from app.db.utils.enums import ActionType
from app.db.tables.hands.schemas import HandStreet

class ActionLogType(str, Enum):
    START_HAND = 'start-hand'
    START_BET_ROUND = 'start-bet-round'
    POST_SMALL_BLIND = 'post-small-blind'
    POST_BIG_BLIND = 'post-big-blind'
    PLAYER_ACTION = 'player-action'
    END_BET_ROUND = 'end-bet-round'
    AUTO_WIN = 'auto-win'
    SHOWDOWN = 'showdown'
    DISTRIBUTE_POTS = 'distribute-pots'
    END_HAND = 'end-hand'

@dataclass
class PlayerActionLog:
    player_id: int
    action_type: ActionType
    amount: Optional[int] = None

@dataclass
class PotDistributionLog:
    pot_id: int
    winner_ids: List[int]
    amount_per_winner: int

@dataclass
class ActionLogEntry:
    sequence: int
    hand_id: int
    street: HandStreet
    type: ActionLogType
    payload: Any
