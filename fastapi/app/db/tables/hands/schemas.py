from enum import Enum
from pydantic import BaseModel, Field
from typing import Annotated, Optional

class HandStreet(str, Enum):
    PRE_FLOP = 'pre-flop'
    FLOP = 'flop'
    TURN = 'turn'
    RIVER = 'river'
    WINNER_SELECTION = 'winner-selection'
    FINISHED = 'finished'

class HandBase(BaseModel):
    game_id: Annotated[int, Field(..., gt=0)]
    current_bet_round_id: Annotated[Optional[int], Field(gt=0)] = None
    street: HandStreet = HandStreet.PRE_FLOP
    dealer_position: Annotated[int, Field(ge=0, le=12)]
    need_small_blind: bool = True
    need_big_blind: bool = True
    
    model_config = {
        'from_attributes': True,
    }

class HandCreate(HandBase):
    pass

class HandOptional(BaseModel):
    game_id: Annotated[Optional[int], Field(gt=0)] = None
    current_bet_round_id: Annotated[Optional[int], Field(gt=0)] = None
    street: Optional[HandStreet] = None
    dealer_position: Annotated[Optional[int], Field(ge=0, le=12)] = None
    need_small_blind: Optional[bool] = None
    need_big_blind: Optional[bool] = None

class HandRead(HandBase):
    id: Annotated[int, Field(gt=0)]
