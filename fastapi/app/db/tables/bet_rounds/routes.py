from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.session import get_db
from app.db.utils import crud_helper as helper
from app.db.tables.bet_rounds.crud import bet_round_crud as crud
from app.db.tables.bet_rounds.schemas import BetRoundRead, BetRoundCreate, BetRoundOptional
from app.core.schemas import DeleteResponse

router = APIRouter(prefix='/bet_rounds',tags=['BetRounds'])

@router.post('/', response_model=BetRoundRead, status_code=201)
async def create_bet_round_endpoint(data: BetRoundCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create(data, db)

@router.get('/by-id/{id}', response_model=BetRoundRead)
async def get_by_id_endpoint(id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_by_id(id, db)

@router.get('/filtered', response_model=List[BetRoundRead])
async def get_filtered_endpoint(
    search: str,
    db: AsyncSession = Depends(get_db)
):
    search_fields = helper.parse_search_fields(search)
    return await crud.get_filtered(search_fields, db)

@router.get('/', response_model=List[BetRoundRead])
async def get_all_endpoint(db: AsyncSession = Depends(get_db)):
    return await crud.get_all(db)

@router.patch('/{id}', response_model=BetRoundRead)
async def update_endpoint(id: int, data: BetRoundOptional, db: AsyncSession = Depends(get_db)):
    return await crud.update(id, data, db)

@router.delete('/{id}', response_model=DeleteResponse)
async def delete_endpoint(id: int, db: AsyncSession = Depends(get_db)):
    await crud.delete(id, db)
    return {'msg': 'Ronda de apuestas eliminada correctamente'}
