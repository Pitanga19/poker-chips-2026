from pydantic import BaseModel, Field
from typing import Annotated, Optional

class RoomBase(BaseModel):
    hoster_id: Annotated[int, Field(..., gt=0)]
    
    model_config = {
        'from_attributes': True,
    }

class RoomCreate(RoomBase):
    code: Annotated[Optional[str], Field(min_length=4, max_length=4)] = None
    pass

class RoomOptional(BaseModel):
    hoster_id: Annotated[Optional[int], Field(gt=0)] = None
    code: Annotated[Optional[str], Field(min_length=4, max_length=4)] = None

class RoomRead(RoomBase):
    id: Annotated[int, Field(..., gt=0)]
    code: Annotated[str, Field(..., min_length=4, max_length=4)]
