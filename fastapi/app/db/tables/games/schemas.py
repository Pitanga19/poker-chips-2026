from pydantic import BaseModel, Field
from typing import Annotated, Optional

class GameBase(BaseModel):
    table_id: Annotated[int, Field(..., gt=0)]
    current_hand_id: Annotated[Optional[int], Field(gt=0)] = None
    is_active: bool = True
    
    model_config = {
        'from_attributes': True,
    }

class GameCreate(GameBase):
    pass

class GameOptional(BaseModel):
    table_id: Annotated[Optional[int], Field(gt=0)] = None
    current_hand_id: Annotated[Optional[int], Field(gt=0)] = None
    is_active: Optional[bool] = None

class GameRead(GameBase):
    id: Annotated[int, Field(gt=0)]
