from enum import Enum

class BetRoundResult(str, Enum):
    NEXT_TURN = 'next-turn'
    FINISHED = 'finished'

class HandResult(str, Enum):
    NEXT_STREET = 'next-street'
    SHOWDOWN = 'showdown'
    AUTO_WIN = 'auto-win'
