from pydantic import BaseModel, Field
from typing import Annotated, Optional

class TurnBase(BaseModel):
    bet_round_id: Annotated[int, Field(..., gt=0)]
    player_id: Annotated[int, Field(..., gt=0)]
    action: Annotated[Optional[int], Field(gt=0)] = None
    amount: Annotated[Optional[int], Field(ge=0)] = None
    
    model_config = {
        'from_attributes': True,
    }

class TurnCreate(TurnBase):
    pass

class TurnOptional(BaseModel):
    bet_round_id: Annotated[Optional[int], Field(gt=0)] = None
    player_id: Annotated[Optional[int], Field(gt=0)] = None
    action: Annotated[Optional[int], Field(gt=0)] = None
    amount: Annotated[Optional[int], Field(ge=0)] = None

class TurnRead(TurnBase):
    id: Annotated[int, Field(gt=0)]
