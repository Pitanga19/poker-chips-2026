from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.db.session import get_db
from app.db.utils import crud_helper as helper
from app.db.tables.rooms.crud import room_crud as crud
from app.db.tables.rooms.schemas import RoomRead, RoomCreate, RoomOptional
from app.core.schemas import DeleteResponse

router = APIRouter(prefix='/rooms',tags=['Rooms'])

@router.post('/', response_model=RoomRead, status_code=201)
async def create_room_endpoint(data: RoomCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create(data, db)

@router.get('/by-id/{id}', response_model=RoomRead)
async def get_by_id_endpoint(id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_by_id(id, db)

@router.get('/filtered', response_model=List[RoomRead])
async def get_filtered_endpoint(
    search: str,
    db: AsyncSession = Depends(get_db)
):
    search_fields = helper.parse_search_fields(search)
    return await crud.get_filtered(search_fields, db)

@router.get('/', response_model=List[RoomRead])
async def get_all_endpoint(db: AsyncSession = Depends(get_db)):
    return await crud.get_all(db)

@router.patch('/{id}', response_model=RoomRead)
async def update_endpoint(id: int, data: RoomOptional, db: AsyncSession = Depends(get_db)):
    return await crud.update(id, data, db)

@router.delete('/{id}', response_model=DeleteResponse)
async def delete_endpoint(id: int, db: AsyncSession = Depends(get_db)):
    await crud.delete(id, db)
    return {'msg': 'Sala eliminada correctamente'}
