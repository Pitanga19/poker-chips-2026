from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.session import get_db
from app.db.tables.tables.schemas import TableRead, TableCreate, TableOptional
from app.db.tables.tables import crud
from app.core.schemas import DeleteResponse

router = APIRouter(
    prefix='/tables',
    tags=['Tables'],
)

@router.post('/', response_model=TableRead, status_code=201)
async def create_table_endpoint(data: TableCreate, db: AsyncSession=Depends(get_db)) -> TableRead:
    return await crud.create(data, db)

@router.get('/by-id/{id}', response_model=TableRead, status_code=200)
async def get_by_id_endpoint(id: int, db: AsyncSession=Depends(get_db)) -> TableRead | None:
    return await crud.get_by_id(id, db)

@router.get('/by-room-id/{room_id}', response_model=List[TableRead], status_code=200)
async def get_by_room_id_endpoint(room_id: int, db: AsyncSession=Depends(get_db)) -> List[TableRead]:
    return await crud.get_by_room_id(room_id, db)

@router.get('/', response_model=List[TableRead], status_code=200)
async def get_all_endpoint(db: AsyncSession=Depends(get_db)) -> List[TableRead]:
    return await crud.get_all(db)

@router.patch('/{id}', response_model=TableRead, status_code=200)
async def update_endpoint(id: int, data: TableOptional, db: AsyncSession=Depends(get_db)) -> TableRead | None:
    return await crud.update(id, data, db)

@router.delete('/{id}', response_model=DeleteResponse, status_code=200)
async def delete_endpoint(id: int, db: AsyncSession=Depends(get_db)) -> None:
    await crud.delete(id, db)
    return {'msg': 'Mesa eliminada correctamente'}
