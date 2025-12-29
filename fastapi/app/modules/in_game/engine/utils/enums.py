from enum import Enum

class BetRoundResult(Enum):
    NEXT_TURN = 'next-turn'
    FINISHED = 'finished'

class HandResult(Enum):
    NEXT_STREET = 'next-street'
    SHOWDOWN = 'showdown'
    AUTO_WIN = 'auto-win'
