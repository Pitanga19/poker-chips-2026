from enum import Enum

class ActionType(str, Enum):
    CHECK = "check"
    CALL = "call"
    BET = "bet"
    RAISE = "raise"
    ALL_IN = "all-in"
    FOLD = "fold"