from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.db.session import get_db
from app.db.utils import crud_helper as helper
from app.db.tables.tables.crud import table_crud as crud
from app.db.tables.tables.schemas import TableRead, TableCreate, TableOptional
from app.core.schemas import DeleteResponse

router = APIRouter(prefix='/tables',tags=['Tables'])

@router.post('/', response_model=TableRead, status_code=201)
async def create_table_endpoint(data: TableCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create(data, db)

@router.get('/by-id/{id}', response_model=TableRead)
async def get_by_id_endpoint(id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_by_id(id, db)

@router.get('/filtered', response_model=List[TableRead])
async def get_filtered_endpoint(
    search: str,
    db: AsyncSession = Depends(get_db)
):
    search_fields = helper.parse_search_fields(search)
    return await crud.get_filtered(search_fields, db)

@router.get('/', response_model=List[TableRead])
async def get_all_endpoint(db: AsyncSession = Depends(get_db)):
    return await crud.get_all(db)

@router.patch('/{id}', response_model=TableRead)
async def update_endpoint(id: int, data: TableOptional, db: AsyncSession = Depends(get_db)):
    return await crud.update(id, data, db)

@router.delete('/{id}', response_model=DeleteResponse)
async def delete_endpoint(id: int, db: AsyncSession = Depends(get_db)):
    await crud.delete(id, db)
    return {'msg': 'Mesa eliminada correctamente'}
