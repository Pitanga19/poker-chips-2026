from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.modules.auth.dependencies import get_current_user
from app.modules.pre_game.gets.services import (
    # players
    get_player_me_by_room_id,
    get_player_by_seat_id,
    get_players_by_room_id,
    get_players_by_table_id,
    # seats
    get_seat_by_id,
    get_seat_by_player_id,
    get_seats_by_table_id,
    get_free_seats_by_table_id,
    # tables
    get_table_by_id,
    get_tables_by_room_id,
    # room settings
    get_room_settings_by_room_id,
    # rooms
    get_room_by_id,
    get_rooms_by_user_id,
    get_rooms_by_hoster_id,
    get_room_public_data_by_code,
)

router = APIRouter(prefix='/pre-game', tags=['Pre Game'])

# ---------------------- PLAYERS ----------------------
@router.get('/rooms/{room_id}/players/me')
async def get_player_me_endpoint(
    room_id: int,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await get_player_me_by_room_id(current_user.id, room_id, db)

@router.get('/rooms/{room_id}/seats/{seat_id}/players')
async def get_player_by_seat_endpoint(
    seat_id: int,
    room_id: int,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await get_player_by_seat_id(current_user.id, room_id, seat_id, db)

@router.get('/rooms/{room_id}/players')
async def get_players_by_room_endpoint(
    room_id: int,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await get_players_by_room_id(current_user.id, room_id, db)

@router.get('/rooms/{room_id}/tables/{table_id}/players')
async def get_players_by_table_endpoint(
    table_id: int,
    room_id: int,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await get_players_by_table_id(current_user.id, room_id, table_id, db)

# ---------------------- SEATS ----------------------
@router.get('/rooms/{room_id}/seats/{seat_id}')
async def get_seat_by_id_endpoint(
    seat_id: int,
    room_id: int,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await get_seat_by_id(current_user.id, room_id, seat_id, db)

@router.get('/rooms/{room_id}/seats/player/{player_id}')
async def get_seat_by_player_endpoint(
    player_id: int,
    room_id: int,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await get_seat_by_player_id(current_user.id, room_id, player_id, db)

@router.get('/rooms/{room_id}/tables/{table_id}/seats')
async def get_seats_by_table_endpoint(
    table_id: int,
    room_id: int,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await get_seats_by_table_id(current_user.id, room_id, table_id, db)

@router.get('/rooms/{room_id}/tables/{table_id}/seats/free')
async def get_free_seats_by_table_endpoint(
    table_id: int,
    room_id: int,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await get_free_seats_by_table_id(current_user.id, room_id, table_id, db)

# ---------------------- TABLES ----------------------
@router.get('/rooms/{room_id}/tables/{table_id}')
async def get_table_by_id_endpoint(
    table_id: int,
    room_id: int,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await get_table_by_id(current_user.id, room_id, table_id, db)

@router.get('/rooms/{room_id}/tables')
async def get_tables_by_room_endpoint(
    room_id: int,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await get_tables_by_room_id(current_user.id, room_id, db)

# ---------------------- ROOM SETTINGS ----------------------
@router.get('/rooms/{room_id}/settings')
async def get_room_settings_endpoint(
    room_id: int,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await get_room_settings_by_room_id(current_user.id, room_id, db)

# ---------------------- ROOM ----------------------
@router.get('/rooms/{room_id}')
async def get_room_by_id_endpoint(
    room_id: int,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await get_room_by_id(current_user.id, room_id, db)

@router.get('/rooms/me/all')
async def get_rooms_by_user_endpoint(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await get_rooms_by_user_id(current_user.id, db)

@router.get('/rooms/me/hosted')
async def get_rooms_by_hoster_endpoint(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await get_rooms_by_hoster_id(current_user.id, db)

@router.get('/rooms/public/{room_code}')
async def get_room_public_data_endpoint(
    room_code: str,
    db: AsyncSession = Depends(get_db)
):
    return await get_room_public_data_by_code(room_code, db)
