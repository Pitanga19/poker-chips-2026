from app.db.utils.base_crud import BaseCRUD
from app.db.tables.rooms.model import Room
from app.db.tables.rooms.schemas import RoomCreate, RoomOptional
from app.db.tables.users.crud import user_crud

class RoomCRUD(BaseCRUD[Room, RoomCreate, RoomOptional]):
    async def validate_create(self, data: RoomCreate, db):
        await user_crud.get_by_id(data.hoster_id, db)
    
    async def validate_update(self, id: int, data: RoomOptional, db):
        if data.hoster_id:
            await user_crud.get_by_id(data.hoster_id, db)

room_crud = RoomCRUD(Room, RoomCreate, RoomOptional)
