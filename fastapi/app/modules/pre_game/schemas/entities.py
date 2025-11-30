from pydantic import Field
from typing import Optional, List, Annotated
from app.db.tables.users.schemas import UserRead
from app.db.tables.players.schemas import PlayerRead
from app.db.tables.seats.schemas import SeatRead
from app.db.tables.tables.schemas import TableRead
from app.db.tables.rooms.schemas import RoomRead
from app.db.tables.room_settings.schemas import RoomSettingsRead

class UserOut(UserRead):
    # id, username
    pass

class PlayerOut(PlayerRead):
    # id, user_id, room_id, stack
    user: UserOut

class SeatOut(SeatRead):
    # id, table_id, player_id, vacate, position
    player: Optional[PlayerOut] = None

class TableOut(TableRead):
    # id, room_id
    seats: List[SeatOut] = Field(default_factory=list)

class RoomSettingsOut(RoomSettingsRead):
    # id, room_id, use_default_buy_in, buy_in, big_blind, small_blind, min_stack_bb, max_stack_bb
    pass

class RoomOut(RoomRead):
    # id, hoster_id, code
    hoster: UserOut
    room_settings: Optional[RoomSettingsOut] = None
    tables: List[TableOut] = Field(default_factory=list)
    players: List[PlayerOut] = Field(default_factory=list)

class RoomPublicData(RoomRead):
    # id, hoster_id, code
    hoster: UserOut
    room_settings: Optional[RoomSettingsOut] = None
    tables_number: Annotated[int, Field(...)]
    players_number: Annotated[int, Field(...)]
