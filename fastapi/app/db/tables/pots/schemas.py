from pydantic import BaseModel, Field
from typing import Annotated, Optional

class PotBase(BaseModel):
    hand_id: Annotated[int, Field(..., gt=0)]
    is_active: Annotated[bool, Field(...)]= True
    is_current: Annotated[bool, Field(...)]= True
    size: Annotated[int, Field(ge=0)] = 0
    
    model_config = {
        'from_attributes': True,
    }

class PotCreate(PotBase):
    pass

class PotOptional(BaseModel):
    hand_id: Annotated[Optional[int], Field(gt=0)] = None
    is_active:Optional[bool] = None
    is_current:Optional[bool] = None
    size: Annotated[Optional[int], Field(ge=0)] = None

class PotRead(PotBase):
    id: Annotated[int, Field(gt=0)]
