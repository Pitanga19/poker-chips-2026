import pytest
from app.db.tables.hands.schemas import HandStreet
from app.modules.in_game.engine.game_states import (
    GameState,
    PlayerState,
    HandState,
    BetRoundState,
    PotState,
)

@pytest.fixture
def players_3_equal():
    return [
        PlayerState(id=1, username='p1', position=0, stack=100),
        PlayerState(id=2, username='p2', position=1, stack=100),
        PlayerState(id=3, username='p3', position=2, stack=100),
    ]

@pytest.fixture
def players_4_varied():
    return [
        PlayerState(id=1, username='p1', position=0, stack=200),
        PlayerState(id=2, username='p2', position=1, stack=150),
        PlayerState(id=3, username='p3', position=2, stack=80),
        PlayerState(id=4, username='p4', position=3, stack=40),
    ]

@pytest.fixture
def base_hand():
    return HandState(
        street=HandStreet.PRE_FLOP,
        small_blind_value=5,
        big_blind_value=10,
    )

@pytest.fixture
def base_bet_round():
    return BetRoundState()

@pytest.fixture
def base_pot():
    return PotState(size=0, players_in_pot=[], pot_winners=[])

@pytest.fixture
def game_state_3p(players_3_equal, base_hand, base_bet_round, base_pot):
    return GameState(
        players=players_3_equal,
        pots=[base_pot],
        hand=base_hand,
        bet_round=base_bet_round,
    )

@pytest.fixture
def game_state_4p(players_4_varied, base_hand, base_bet_round, base_pot):
    return GameState(
        players=players_4_varied,
        pots=[base_pot],
        hand=base_hand,
        bet_round=base_bet_round,
    )
