from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.session import get_db
from app.db.utils import crud_helper as helper
from app.db.tables.pot_players.crud import pot_player_crud as crud
from app.db.tables.pot_players.schemas import PotPlayerRead, PotPlayerCreate
from app.core.schemas import DeleteResponse

router = APIRouter(prefix='/pot_players',tags=['PotPlayers'])

@router.post('/', response_model=PotPlayerRead, status_code=201)
async def create_pot_player_endpoint(data: PotPlayerCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create(data, db)

@router.get('/by-id/{id}', response_model=PotPlayerRead)
async def get_by_id_endpoint(id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_by_id(id, db)

@router.get('/filtered', response_model=List[PotPlayerRead])
async def get_filtered_endpoint(
    search: str,
    db: AsyncSession = Depends(get_db)
):
    search_fields = helper.parse_search_fields(search)
    return await crud.get_filtered(search_fields, db)

@router.get('/', response_model=List[PotPlayerRead])
async def get_all_endpoint(db: AsyncSession = Depends(get_db)):
    return await crud.get_all(db)

@router.delete('/{id}', response_model=DeleteResponse)
async def delete_endpoint(id: int, db: AsyncSession = Depends(get_db)):
    await crud.delete(id, db)
    return {'msg': 'Pozo-Jugador eliminado correctamente'}
