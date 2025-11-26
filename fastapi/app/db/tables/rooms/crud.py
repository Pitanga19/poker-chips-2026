from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.db.utils import crud_helper as utils
from app.db.tables.rooms.model import Room
from app.db.tables.rooms.schemas import *
from app.db.tables.users.crud import get_by_id as get_user_by_id

async def create(data: RoomCreate, db: AsyncSession) -> Room:
    # Validar existencias ...
    await get_user_by_id(data.hoster_id, db) # Verificar que el hoster exista
    
    room = Room(
        hoster_id=data.hoster_id,
    )
    
    db.add(room)
    return await utils.commit_and_refresh(room, db)

async def get_by_id(id: int, db: AsyncSession) -> Room | None:
    stmt = select(Room).where(Room.id == id)
    should_exist = True
    search_fields = [utils.SearchField(field='id', value=id)]
    return await utils.get_validated(stmt, should_exist, search_fields, db)

async def get_by_hoster_id(hoster_id: int, db: AsyncSession) -> List[Room]:
    stmt = select(Room).where(Room.hoster_id == hoster_id)
    return await utils.get_many(stmt, db)

async def get_all(db: AsyncSession) -> List[Room]:
    return await utils.get_all(Room, db)

async def update(id: int, data: RoomOptional, db: AsyncSession) -> Room | None:
    room = await get_by_id(id, db)
    updates = data.model_dump(exclude_unset=True)
    
    utils.update_fields(room, updates)    
    return await utils.commit_and_refresh(room, db)

async def delete(id: int, db: AsyncSession) -> None:
    room = await get_by_id(id, db)
    await utils.delete(room, db)
