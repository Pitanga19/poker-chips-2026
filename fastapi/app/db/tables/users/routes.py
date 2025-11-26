from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.session import get_db
from app.db.tables.users.schemas import UserRead, UserCreate, UserOptional
from app.db.tables.users import crud
from app.core.schemas import DeleteResponse

router = APIRouter(
    prefix='/users',
    tags=['Users'],
)

@router.post('/', response_model=UserRead, status_code=201)
async def create_user_endpoint(data: UserCreate, db: AsyncSession=Depends(get_db)) -> UserRead:
    return await crud.create(data, db)

@router.get('/by-id/{id}', response_model=UserRead, status_code=200)
async def get_by_id_endpoint(id: int, db: AsyncSession=Depends(get_db)) -> UserRead | None:
    return await crud.get_by_id(id, db)

@router.get('/by-username/{username}', response_model=UserRead, status_code=200)
async def get_by_username_endpoint(username: str, db: AsyncSession=Depends(get_db)) -> UserRead | None:
    return await crud.get_by_username(username, db)

@router.get('/', response_model=List[UserRead], status_code=200)
async def get_all_endpoint(db: AsyncSession=Depends(get_db)) -> List[UserRead]:
    return await crud.get_all(db)

@router.patch('/{id}', response_model=UserRead, status_code=200)
async def update_endpoint(id: int, data: UserOptional, db: AsyncSession=Depends(get_db)) -> UserRead | None:
    return await crud.update(id, data, db)

@router.delete('/{id}', response_model=DeleteResponse, status_code=200)
async def delete_endpoint(id: int, db: AsyncSession=Depends(get_db)) -> None:
    await crud.delete(id, db)
    return {'msg': 'Usuario eliminado correctamente'}
