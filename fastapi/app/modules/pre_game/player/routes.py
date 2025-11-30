from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.modules.auth.dependencies import get_current_user
from app.modules.pre_game.player import services as player_services
from app.modules.pre_game.schemas.api import (
    JoinRoomResponse, ChipsPurchaseBody, ChipsPurchaseResponse, JoinTableBody, JoinTableResponse, ChangeSeatBody, ChangeSeatResponse
)

router = APIRouter(prefix='/pre-game', tags=['Pre Game'])

@router.post('/rooms/{room_id}/players', response_model=JoinRoomResponse)
async def join_room_endpoint(
    room_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """ Usuario se une a sala existente """
    return await player_services.join_room(
        user_id=current_user.id,
        room_id=room_id,
        db=db
    )

@router.delete('/rooms/{room_id}/players', response_model=dict)
async def leave_room_endpoint(
    room_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """ Usuario abandona sala """
    await player_services.leave_room(
        user_id=current_user.id,
        room_id=room_id,
        db=db
    )
    return {'msg': 'Usuario salió de la sala'}

@router.post('/rooms/{room_id}/chips-purchase', response_model=ChipsPurchaseResponse)
async def chips_purchase_endpoint(
    room_id: int,
    chips_purchase_body: ChipsPurchaseBody,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """ Jugador compra fichas dentro de la sala """
    return await player_services.chips_purchase(
        user_id=current_user.id,
        room_id=room_id,
        chips_purchase_body=chips_purchase_body,
        db=db
    )

@router.post('/rooms/{room_id}/tables/{table_id}/players', response_model=JoinTableResponse)
async def join_table_endpoint(
    room_id: int,
    table_id: int,
    join_table_body: JoinTableBody,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """ Jugador se sienta en una mesa """
    return await player_services.join_table(
        user_id=current_user.id,
        room_id=room_id,
        table_id=table_id,
        join_table_body=join_table_body,
        db=db,
    )

@router.delete('/rooms/{room_id}/tables/{table_id}/players', response_model=dict)
async def leave_table_endpoint(
    room_id: int,
    table_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """ Jugador se levanta de la mesa """
    await player_services.leave_table(
        user_id=current_user.id,
        room_id=room_id,
        table_id=table_id,
        db=db
    )
    return {'msg': 'Jugador se levantó de la mesa'}

@router.post('/rooms/{room_id}/tables/{table_id}/change-seat', response_model=ChangeSeatResponse)
async def change_seat_endpoint(
    room_id: int,
    table_id: int,
    change_seat_body: ChangeSeatBody,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """ Jugador cambia asiento dentro de la misma mesa """
    return await player_services.change_seat(
        user_id=current_user.id,
        room_id=room_id,
        table_id=table_id,
        change_seat_body=change_seat_body,
        db=db
    )
