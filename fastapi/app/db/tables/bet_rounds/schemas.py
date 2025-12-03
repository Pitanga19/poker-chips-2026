from pydantic import BaseModel, Field
from typing import Annotated, Optional

class BetRoundBase(BaseModel):
    hand_id: Annotated[int, Field(..., gt=0)]
    last_turn_id: Annotated[Optional[int], Field(gt=0)] = None
    current_turn_position: Annotated[Optional[int], Field(ge=0)] = None
    current_max_bet: Annotated[int, Field(ge=0)] = 0
    current_min_raise: Annotated[int, Field(ge=0)] = 0
    
    model_config = {
        'from_attributes': True,
    }

class BetRoundCreate(BetRoundBase):
    pass

class BetRoundOptional(BaseModel):
    hand_id: Annotated[Optional[int], Field(gt=0)] = None
    last_turn_id: Annotated[Optional[int], Field(gt=0)] = None
    current_turn_position: Annotated[Optional[int], Field(ge=0)] = None
    current_max_bet: Annotated[Optional[int], Field(ge=0)] = None
    current_min_raise: Annotated[Optional[int], Field(ge=0)] = None

class BetRoundRead(BetRoundBase):
    id: Annotated[int, Field(gt=0)]
