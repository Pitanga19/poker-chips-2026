from pydantic import BaseModel, Field
from typing import Annotated, Optional

class PlayerBase(BaseModel):
    user_id: Annotated[int, Field(..., gt=0)]
    room_id: Annotated[int, Field(..., gt=0)]
    stack: Annotated[int, Field(ge=0)] = 0
    betting_stack: Annotated[int, Field(ge=0)] = 0
    last_action_id: Annotated[Optional[int], Field(gt=0)] = None
    
    model_config = {
        'from_attributes': True,
    }

class PlayerCreate(PlayerBase):
    pass

class PlayerOptional(BaseModel):
    user_id: Annotated[Optional[int], Field(gt=0)] = None
    room_id: Annotated[Optional[int], Field(gt=0)] = None
    stack: Annotated[Optional[int], Field(ge=0)] = None
    betting_stack: Annotated[Optional[int], Field(ge=0)] = None
    last_action_id: Annotated[Optional[int], Field(gt=0)] = None

class PlayerRead(PlayerBase):
    id: Annotated[int, Field(..., gt=0)]
