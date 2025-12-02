from pydantic import BaseModel, Field
from typing import Annotated, Optional

class TableBase(BaseModel):
    room_id: Annotated[int, Field(..., gt=0)]
    
    model_config = {
        'from_attributes': True,
    }

class TableCreate(TableBase):
    pass

class TableOptional(BaseModel):
    room_id: Annotated[Optional[int], Field(gt=0)] = None

class TableRead(TableBase):
    id: Annotated[int, Field(..., gt=0)]
