from pydantic import BaseModel, Field
from enum import Enum
from typing import Annotated, List, Optional

class CreateRoomResponse(BaseModel):
    hoster_id: Annotated[int, Field(..., gt=0)]
    player_id: Annotated[int, Field(..., gt=0)]
    room_id: Annotated[int, Field(..., gt=0)]
    room_code: Annotated[str, Field(..., min_length=4, max_length=4)]

class JoinRoomResponse(BaseModel):
    room_id: Annotated[int, Field(..., gt=0)]
    user_id: Annotated[int, Field(..., gt=0)]
    player_id: Annotated[int, Field(..., gt=0)]

class UpdateRoomSettingsResponse(BaseModel):
    hoster_id: Annotated[int, Field(..., gt=0)]
    room_id: Annotated[int, Field(..., gt=0)]
    room_settings_id: Annotated[int, Field(..., gt=0)]

class UpdateStackOperation(str, Enum):
    SET = 'set'
    ADD = 'add'
    SUB = 'sub'

class UpdateStackBody(BaseModel):
    operation: UpdateStackOperation
    amount: Annotated[int, Field(gt=0)]

class UpdateStackResponse(BaseModel):
    hoster_id: Annotated[int, Field(..., gt=0)]
    room_id: Annotated[int, Field(..., gt=0)]
    user_id: Annotated[int, Field(..., gt=0)]
    player_id: Annotated[int, Field(..., gt=0)]
    new_stack: Annotated[int, Field(..., gt=0)]

class ChipsPurchaseBody(BaseModel):
    amount: Annotated[int, Field(gt=0)]

class ChipsPurchaseResponse(BaseModel):
    user_id: Annotated[int, Field(..., gt=0)]
    player_id: Annotated[int, Field(..., gt=0)]
    new_stack: Annotated[int, Field(..., gt=0)]

class CreateTableBody(BaseModel):
    seats_number: Annotated[int, Field(..., gt=1, le=12)]

class CreateTableResponse(BaseModel):
    hoster_id: Annotated[int, Field(..., gt=0)]
    room_id: Annotated[int, Field(..., gt=0)]
    table_id: Annotated[int, Field(..., gt=0)]
    seats_id_list: List[Annotated[int, Field(..., gt=0)]]

class JoinTableBody(BaseModel):
    position: Annotated[Optional[int], Field(ge=1, le=12)] = None

class JoinTableResponse(BaseModel):
    room_id: Annotated[int, Field(..., gt=0)]
    user_id: Annotated[int, Field(..., gt=0)]
    player_id: Annotated[int, Field(..., gt=0)]
    seat_id: Annotated[int, Field(..., gt=0)]
    position: Annotated[int, Field(..., ge=1, le=12)]

class ChangeSeatBody(BaseModel):
    new_position: Annotated[int, Field(..., ge=1, le=12)]

class ChangeSeatResponse(BaseModel):
    room_id: Annotated[int, Field(..., gt=0)]
    user_id: Annotated[int, Field(..., gt=0)]
    player_id: Annotated[int, Field(..., gt=0)]
    new_seat_id: Annotated[int, Field(..., gt=0)]
    new_position: Annotated[int, Field(..., ge=1, le=12)]

class CreateSeatBody(BaseModel):
    position: Annotated[int, Field(..., ge=1, le=12)]

class CreateSeatResponse(BaseModel):
    hoster_id: Annotated[int, Field(..., gt=0)]
    room_id: Annotated[int, Field(..., gt=0)]
    table_id: Annotated[int, Field(..., gt=0)]
    seat_id: Annotated[int, Field(..., gt=0)]
