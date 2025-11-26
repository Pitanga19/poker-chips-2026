from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.session import get_db
from app.db.tables.rooms.schemas import RoomRead, RoomCreate, RoomOptional
from app.db.tables.rooms import crud
from app.core.schemas import DeleteResponse

router = APIRouter(
    prefix='/rooms',
    tags=['Rooms'],
)

@router.post('/', response_model=RoomRead, status_code=201)
async def create_room_endpoint(data: RoomCreate, db: AsyncSession=Depends(get_db)) -> RoomRead:
    return await crud.create(data, db)

@router.get('/by-id/{id}', response_model=RoomRead, status_code=200)
async def get_by_id_endpoint(id: int, db: AsyncSession=Depends(get_db)) -> RoomRead | None:
    return await crud.get_by_id(id, db)

@router.get('/by-hoster-id/{hoster_id}', response_model=List[RoomRead], status_code=200)
async def get_by_hoster_id_endpoint(hoster_id: int, db: AsyncSession=Depends(get_db)) -> List[RoomRead]:
    return await crud.get_by_hoster_id(hoster_id, db)

@router.get('/', response_model=List[RoomRead], status_code=200)
async def get_all_endpoint(db: AsyncSession=Depends(get_db)) -> List[RoomRead]:
    return await crud.get_all(db)

@router.patch('/{id}', response_model=RoomRead, status_code=200)
async def update_endpoint(id: int, data: RoomOptional, db: AsyncSession=Depends(get_db)) -> RoomRead | None:
    return await crud.update(id, data, db)

@router.delete('/{id}', response_model=DeleteResponse, status_code=200)
async def delete_endpoint(id: int, db: AsyncSession=Depends(get_db)) -> None:
    await crud.delete(id, db)
    return {'msg': 'Sala eliminada correctamente'}
