from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.db.utils import crud_helper as utils
from app.db.tables.tables.model import Table
from app.db.tables.tables.schemas import *
from app.db.tables.rooms.crud import get_by_id as get_room_by_id

async def create(data: TableCreate, db: AsyncSession) -> Table:
    # Validar existencias ...
    await get_room_by_id(data.room_id, db) # Verificar que la sala exista
    
    table = Table(
        room_id=data.room_id,
    )
    
    db.add(table)
    return await utils.commit_and_refresh(table, db)

async def get_by_id(id: int, db: AsyncSession) -> Table | None:
    stmt = select(Table).where(Table.id == id)
    should_exist = True
    search_fields = [utils.SearchField(field='id', value=id)]
    return await utils.get_validated(stmt, should_exist, search_fields, db)

async def get_by_room_id(room_id: int, db: AsyncSession) -> List[Table]:
    stmt = select(Table).where(Table.room_id == room_id)
    return await utils.get_many(stmt, db)

async def get_all(db: AsyncSession) -> List[Table]:
    return await utils.get_all(Table, db)

async def update(id: int, data: TableOptional, db: AsyncSession) -> Table | None:
    table = await get_by_id(id, db)
    updates = data.model_dump(exclude_unset=True)
    
    utils.update_fields(table, updates)    
    return await utils.commit_and_refresh(table, db)

async def delete(id: int, db: AsyncSession) -> None:
    table = await get_by_id(id, db)
    await utils.delete(table, db)
