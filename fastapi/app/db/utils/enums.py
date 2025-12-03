from enum import Enum

class ActionType(str, Enum):
    PUT_SB = "put-sb"
    PUT_BB = "put-bb"
    CHECK = "check"
    CALL = "call"
    BET = "bet"
    RAISE = "raise"
    ALL_IN = "all-in"
    FOLD = "fold"