from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.db.tables.room_settings.schemas import RoomSettingsBase, RoomSettingsOptional
from app.modules.auth.dependencies import get_current_user
from app.modules.pre_game.management import services as management_services
from app.modules.pre_game.schemas.api import (
    CreateRoomResponse, UpdateRoomSettingsResponse,
    CreateTableBody, CreateTableResponse,
    CreateSeatBody, CreateSeatResponse,
    UpdateStackBody, UpdateStackResponse,
)

router = APIRouter(prefix='/pre-game/management', tags=['Pre Game'])

@router.post('/rooms', response_model=CreateRoomResponse)
async def create_room_endpoint(
    room_pre_game_settings_data: RoomSettingsBase,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Usuario crea una sala"""
    return await management_services.create_room(
        user_id=current_user.id,
        room_pre_game_settings_data=room_pre_game_settings_data,
        db=db
    )

@router.patch('/rooms/{room_id}/settings', response_model=UpdateRoomSettingsResponse)
async def update_room_settings_endpoint(
    room_id: int,
    room_settings_update_data: RoomSettingsOptional,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """ Actualizar configuración de sala por hoster """
    return await management_services.update_room_settings(
        hoster_id=current_user.id,
        room_id=room_id,
        room_settings_update_data=room_settings_update_data,
        db=db,
    )

@router.post('/rooms/{room_id}/tables', response_model=CreateTableResponse)
async def create_table_endpoint(
    room_id: int,
    create_table_body: CreateTableBody,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """ Crear mesa y sus asientos """
    return await management_services.create_table(
        hoster_id=current_user.id,
        room_id=room_id,
        create_table_body=create_table_body,
        db=db
    )

@router.delete('/rooms/{room_id}/tables/{table_id}', response_model=dict)
async def delete_table_endpoint(
    room_id: int,
    table_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """ Eliminar mesa """
    await management_services.delete_table(
        hoster_id=current_user.id,
        room_id=room_id,
        table_id=table_id,
        db=db
    )
    return {'msg': 'Mesa eliminada'}

@router.post('/rooms/{room_id}/tables/{table_id}/seats', response_model=CreateSeatResponse)
async def create_seat_endpoint(
    room_id: int,
    table_id: int,
    create_seat_body: CreateSeatBody,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """ Crear un asiento en una mesa """
    return await management_services.create_seat(
        hoster_id=current_user.id,
        room_id=room_id,
        table_id=table_id,
        create_seat_body=create_seat_body,
        db=db
    )

@router.delete('/rooms/{room_id}/tables/{table_id}/seats/{seat_id}', response_model=dict)
async def delete_seat_endpoint(
    room_id: int,
    table_id: int,
    seat_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """ Eliminar asiento """
    await management_services.delete_seat(
        hoster_id=current_user.id,
        room_id=room_id,
        table_id=table_id,
        seat_id=seat_id,
        db=db
    )
    return {'msg': 'Asiento eliminado'}

@router.patch('/rooms/{room_id}/players/{player_id}/stack', response_model=UpdateStackResponse)
async def update_stack_endpoint(
    room_id: int,
    player_id: int,
    update_stack_body: UpdateStackBody,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """ Actualizar stack de jugador """
    return await management_services.update_stack(
        hoster_id=current_user.id,
        room_id=room_id,
        player_id=player_id,
        update_stack_body=update_stack_body,
        db=db
    )
