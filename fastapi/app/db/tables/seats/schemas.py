from pydantic import BaseModel, Field
from typing import Annotated, Optional

class SeatBase(BaseModel):
    table_id: Annotated[int, Field(..., gt=0)]
    player_id: Annotated[Optional[int], Field(gt=0)] = None
    vacate: bool = True
    position: Annotated[int, Field(..., ge=0)]
    
    model_config = {
        'from_attributes': True,
    }

class SeatCreate(SeatBase):
    pass

class SeatOptional(BaseModel):
    table_id: Annotated[Optional[int], Field(gt=0)] = None
    player_id: Annotated[Optional[int], Field(gt=0)] = None
    vacate: Optional[bool] = None
    position: Annotated[Optional[int], Field(ge=0)] = None

class SeatRead(SeatBase):
    id: Annotated[int, Field(..., gt=0)]
