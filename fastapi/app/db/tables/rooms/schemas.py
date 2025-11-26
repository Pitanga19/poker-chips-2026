from pydantic import BaseModel, Field
from typing import Annotated, Optional

class RoomBase(BaseModel):
    hoster_id:  Annotated[int, Field(..., gt=0)]
    
    model_config = {
        'from_attributes': True,
    }

class RoomCreate(RoomBase):
    hoster_id:  Annotated[int, Field(..., gt=0)]

class RoomRead(RoomBase):
    id: Annotated[int, Field(..., gt=0)]

class RoomOptional(BaseModel):
    hoster_id: Annotated[Optional[int], Field(gt=0)] = None
