from pydantic import BaseModel, Field
from typing import Annotated, Optional

class RoomSettingsBase(BaseModel):
    use_default_buy_in: bool = False
    buy_in: Annotated[Optional[int], Field(gt=0)] = None
    big_blind_value: Annotated[int, Field(..., gt=0)]
    min_stack_bb: Annotated[int, Field(..., gt=0)]
    max_stack_bb: Annotated[Optional[int], Field(gt=0)] = None
    
    model_config = {
        'from_attributes': True,
    }

class RoomSettingsCreate(RoomSettingsBase):
    room_id: Annotated[int, Field(..., gt=0)]
    small_blind_value: Annotated[int, Field(..., gt=0)]

class RoomSettingsOptional(BaseModel):
    room_id: Annotated[Optional[int], Field(gt=0)] = None
    use_default_buy_in: Optional[bool] = None
    buy_in: Annotated[Optional[int], Field(gt=0)] = None
    big_blind_value: Annotated[Optional[int], Field(gt=0)] = None
    small_blind_value: Annotated[Optional[int], Field(gt=0)] = None
    min_stack_bb: Annotated[Optional[int], Field(gt=0)] = None
    max_stack_bb: Annotated[Optional[int], Field(gt=0)] = None

class RoomSettingsRead(RoomSettingsBase):
    id: Annotated[int, Field(..., gt=0)]
    room_id: Annotated[int, Field(..., gt=0)]
    small_blind_value: Annotated[int, Field(..., gt=0)]
