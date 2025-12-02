
from enum import Enum
from pydantic import BaseModel, Field
from typing import Annotated, Optional

class PotState(str, Enum):
    OPEN = 'open'
    CLOSED = 'closed'
    FINISHED = 'finished'

class PotBase(BaseModel):
    hand_id: Annotated[int, Field(..., gt=0)]
    state: PotState = PotState.OPEN
    size: Annotated[int, Field(ge=0)] = 0
    
    model_config = {
        'from_attributes': True,
    }

class PotCreate(PotBase):
    pass

class PotOptional(BaseModel):
    hand_id: Annotated[Optional[int], Field(gt=0)] = None
    state: Optional[PotState] = None
    size: Annotated[Optional[int], Field(ge=0)] = None

class PotRead(PotBase):
    id: Annotated[int, Field(gt=0)]
