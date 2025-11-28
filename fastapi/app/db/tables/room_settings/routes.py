from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.session import get_db
from app.db.utils import crud_helper as helper
from app.db.tables.room_settings.crud import room_settings_crud as crud
from app.db.tables.room_settings.schemas import RoomSettingsRead, RoomSettingsCreate, RoomSettingsOptional
from app.core.schemas import DeleteResponse

router = APIRouter(prefix='/room_settings',tags=['RoomSettings'])

@router.post('/', response_model=RoomSettingsRead, status_code=201)
async def create_room_settings_endpoint(data: RoomSettingsCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create(data, db)

@router.get('/by-id/{id}', response_model=RoomSettingsRead)
async def get_by_id_endpoint(id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_by_id(id, db)

@router.get('/filtered', response_model=List[RoomSettingsRead])
async def get_filtered_endpoint(
    search: str,
    db: AsyncSession = Depends(get_db)
):
    search_fields = helper.parse_search_fields(search)
    return await crud.get_filtered(search_fields, db)

@router.get('/', response_model=List[RoomSettingsRead])
async def get_all_endpoint(db: AsyncSession = Depends(get_db)):
    return await crud.get_all(db)

@router.patch('/{id}', response_model=RoomSettingsRead)
async def update_endpoint(id: int, data: RoomSettingsOptional, db: AsyncSession = Depends(get_db)):
    return await crud.update(id, data, db)

@router.delete('/{settings_id}', response_model=DeleteResponse)
async def delete_room_settings(
    settings_id: int,
    db: AsyncSession = Depends(get_db)
):
    await crud.delete(settings_id, db)
    return {'msg': 'Configuración de sala eliminada correctamente'}
