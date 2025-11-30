from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload
from app.core.exceptions import ValidationException, NotFoundException
from app.db.tables.players.model import Player
from app.db.tables.players.crud import player_crud
from app.db.tables.seats.model import Seat
from app.db.tables.tables.model import Table
from app.db.tables.rooms.model import Room
from app.db.tables.rooms.crud import room_crud
from app.db.tables.room_settings.model import RoomSettings
from app.db.utils.crud_helper import SearchField
from app.modules.pre_game.schemas.entities import (
    UserOut, PlayerOut, SeatOut, TableOut, RoomSettingsOut, RoomOut, RoomPublicData
)

# ---------------------- PLAYERS ----------------------
async def get_player_me_by_room_id(user_id: int, room_id: int, db: AsyncSession) -> PlayerOut:
    """ Obtener jugador por id de usuario """
    # Validar que el usuario pertenezca a la sala
    await _validate_user_in_room(user_id, room_id, db)
    
    stmt = (
        select(Player)
        .options(selectinload(Player.user))
        .where(
            Player.user_id == user_id,
            Player.room_id == room_id
        )
    )
    result = await db.execute(stmt)
    
    try:
        player: Player = result.scalar_one()
    except NoResultFound:
        raise NotFoundException(f'El usuario {user_id} no pertenece a la sala {room_id}')
    
    return PlayerOut.model_validate(player)

async def get_player_by_seat_id(
    user_id: int,
    room_id: int,
    seat_id: int,
    db: AsyncSession
) -> PlayerOut:
    """ Obtener jugador por id de asiento """
    # Validar que el usuario pertenezca a la sala
    await _validate_user_in_room(user_id, room_id, db)
    
    stmt = select(Seat).options(
        selectinload(Seat.player).selectinload(Player.user)
    ).where(Seat.id == seat_id)
    result = await db.execute(stmt)
    
    try:
        seat: Seat = result.scalar_one()
    except NoResultFound:
        raise NotFoundException(f'No se encontró un jugador en el asiento id {seat_id}')
    
    if not seat.player:
        raise ValidationException(f'No hay jugador en el asiento id {seat_id}')
    return PlayerOut.model_validate(seat.player)

async def get_players_by_room_id(user_id: int, room_id: int, db: AsyncSession) -> List[PlayerOut]:
    """ Obtener jugadores por id de sala """
    # Validar que el usuario pertenezca a la sala
    await _validate_user_in_room(user_id, room_id, db)
    stmt = select(Player).options(
        selectinload(Player.user)
    ).where(Player.room_id == room_id)
    result = await db.execute(stmt)
    players: List[Player] = result.scalars().all()
    return [PlayerOut.model_validate(p) for p in players]

async def get_players_by_table_id(
    user_id: int,
    room_id: int,
    table_id: int,
    db: AsyncSession
) -> List[PlayerOut]:
    """ Obtener jugadores por id de mesa """
    # Validar que el usuario pertenezca a la sala
    await _validate_user_in_room(user_id, room_id, db)
    stmt = select(Seat).options(
        selectinload(Seat.player).selectinload(Player.user)
    ).where(Seat.table_id == table_id, Seat.player_id.isnot(None))
    result = await db.execute(stmt)
    seats: List[Seat] = result.scalars().all()
    return [PlayerOut.model_validate(seat.player) for seat in seats if seat.player is not None]

# ---------------------- SEATS ----------------------

async def get_seat_by_id(user_id: int, room_id: int, seat_id: int, db: AsyncSession) -> SeatOut:
    """ Obtener asiento por id de asiento """
    # Validar que el usuario pertenezca a la sala
    await _validate_user_in_room(user_id, room_id, db)
    stmt = select(Seat).options(
        selectinload(Seat.player).selectinload(Player.user)
    ).where(Seat.id == seat_id)
    result = await db.execute(stmt)
    
    try:
        seat: Seat = result.scalar_one()
    except NoResultFound:
        raise NotFoundException(f'No se encontró el asiento con id {seat_id}')
    
    return SeatOut.model_validate(seat)

async def get_seat_by_player_id(
    user_id: int,
    room_id: int,
    player_id: int,
    db: AsyncSession
) -> SeatOut:
    """ Obtener asiento por id de jugador """
    # Validar que el usuario pertenezca a la sala
    await _validate_user_in_room(user_id, room_id, db)
    stmt = select(Seat).options(
        selectinload(Seat.player).selectinload(Player.user)
    ).where(Seat.player_id == player_id)
    result = await db.execute(stmt)
    
    try:
        seat: Seat = result.scalar_one()
    except NoResultFound:
        raise NotFoundException(f'No se encontró un asiento con el jugador id {player_id}')
    
    return SeatOut.model_validate(seat)

async def get_seats_by_table_id(
    user_id: int,
    room_id: int,
    table_id: int,
    db: AsyncSession
) -> List[SeatOut]:
    """ Obtener asientos por id de mesa """
    # Validar que el usuario pertenezca a la sala
    await _validate_user_in_room(user_id, room_id, db)
    stmt = select(Seat).options(
        selectinload(Seat.player).selectinload(Player.user)
    ).where(Seat.table_id == table_id)
    result = await db.execute(stmt)
    seats: List[Seat] = result.scalars().all()
    return [SeatOut.model_validate(s) for s in seats]

async def get_free_seats_by_table_id(
    user_id: int,
    room_id: int,
    table_id: int,
    db: AsyncSession
) -> List[SeatOut]:
    """ Obtener asientos libres por id de mesa """
    # Validar que el usuario pertenezca a la sala
    await _validate_user_in_room(user_id, room_id, db)
    stmt = select(Seat).options(
        selectinload(Seat.player).selectinload(Player.user)
    ).where(Seat.table_id == table_id, Seat.player_id.is_(None))
    result = await db.execute(stmt)
    seats: List[Seat] = result.scalars().all()
    return [SeatOut.model_validate(s) for s in seats]

# ---------------------- TABLES ----------------------

async def get_table_by_id(
    user_id: int,
    room_id: int,
    table_id: int,
    db: AsyncSession
) -> TableOut:
    """ Obtener mesa por id de mesa """
    # Validar que el usuario pertenezca a la sala
    await _validate_user_in_room(user_id, room_id, db)
    stmt = select(Table).options(
        selectinload(Table.seats).selectinload(Seat.player).selectinload(Player.user)
    ).where(Table.id == table_id)
    result = await db.execute(stmt)
    
    try:
        table: Table = result.scalar_one()
    except NoResultFound:
        raise NotFoundException(f'No se encontró la mesa con id {table_id}')
    
    return TableOut.model_validate(table)

async def get_tables_by_room_id(user_id: int, room_id: int, db: AsyncSession) -> List[TableOut]:
    """ Obtener mesas por id de sala """
    # Validar que el usuario pertenezca a la sala
    await _validate_user_in_room(user_id, room_id, db)
    stmt = select(Table).options(
        selectinload(Table.seats).selectinload(Seat.player).selectinload(Player.user)
    ).where(Table.room_id == room_id)
    result = await db.execute(stmt)
    tables: List[Table] = result.scalars().all()
    return [TableOut.model_validate(t) for t in tables]

# ---------------------- ROOM SETTINGS ----------------------

async def get_room_settings_by_room_id(
    user_id: int,
    room_id: int,
    db: AsyncSession
) -> RoomSettingsOut:
    """ Obtener configuración de sala por id de sala """
    # Validar que el usuario pertenezca a la sala
    await _validate_user_in_room(user_id, room_id, db)
    stmt = select(RoomSettings).options(
        selectinload(RoomSettings.room)
    ).where(RoomSettings.room_id == room_id)
    result = await db.execute(stmt)
    
    try:
        settings: RoomSettings = result.scalar_one()
    except NoResultFound:
        raise NotFoundException(f'No se encontró configuración para la sala con id {room_id}')
    
    return RoomSettingsOut.model_validate(settings)

# ---------------------- ROOMS ----------------------

async def get_room_by_id(user_id: int, room_id: int, db: AsyncSession) -> RoomOut:
    """ Obtener sala por id de sala """
    # Validar que el usuario pertenezca a la sala
    await _validate_user_in_room(user_id, room_id, db)
    stmt = select(Room).options(
        selectinload(Room.hoster),
        selectinload(Room.players).selectinload(Player.user),
        selectinload(Room.tables).selectinload(Table.seats).selectinload(Seat.player).selectinload(Player.user),
        selectinload(Room.room_settings)
    ).where(Room.id == room_id)
    result = await db.execute(stmt)
    
    try:
        room: Room = result.scalar_one()
    except NoResultFound:
        raise NotFoundException(f'No se encontró la sala con id {room_id}')
    
    return RoomOut.model_validate(room)

async def get_rooms_by_user_id(user_id: int, db: AsyncSession) -> List[RoomOut]:
    """ Obtener todas las salas donde el usuario participa (como hoster o jugador) """
    # Subquery para obtener room_ids donde el usuario es jugador
    player_rooms_subq = (
        select(Player.room_id)
        .where(Player.user_id == user_id)
        .subquery()
    )
    
    stmt = (
        select(Room)
        .options(
            selectinload(Room.hoster),
            selectinload(Room.players).selectinload(Player.user),
            selectinload(Room.tables)
                .selectinload(Table.seats)
                .selectinload(Seat.player)
                .selectinload(Player.user),
            selectinload(Room.room_settings),
        )
        .where(
            (Room.hoster_id == user_id) | 
            (Room.id.in_(select(player_rooms_subq.c.room_id)))
        )
    )
    
    result = await db.execute(stmt)
    rooms: List[Room] = result.scalars().unique().all()
    
    return [RoomOut.model_validate(r) for r in rooms]

async def get_rooms_by_hoster_id(hoster_id: int, db: AsyncSession) -> List[RoomOut]:
    """ Obtener todas las salas donde el usuario es hoster """
    stmt = (
        select(Room)
        .options(
            selectinload(Room.hoster),
            selectinload(Room.players).selectinload(Player.user),
            selectinload(Room.tables)
                .selectinload(Table.seats)
                .selectinload(Seat.player)
                .selectinload(Player.user),
            selectinload(Room.room_settings),
        )
        .where(Room.hoster_id == hoster_id)
    )

    result = await db.execute(stmt)
    rooms: List[Room] = result.scalars().all()

    return [RoomOut.model_validate(r) for r in rooms]

async def get_room_public_data_by_code(room_code: str, db: AsyncSession) -> RoomPublicData:
    """ Buscar una sala por su código público """
    # Formatear código a mayúsculas
    room_code = room_code.upper()
    
    # Obtener sala
    stmt = (
        select(Room)
        .options(
            selectinload(Room.hoster),
            selectinload(Room.room_settings)
        )
        .where(Room.code == room_code)
    )
    result = await db.execute(stmt)
    
    try:
        room: Room = result.scalar_one()
    except NoResultFound:
        raise NotFoundException(f'No se encontró la sala con el código {room_code}')
    
    # Contar jugadores
    players_count_stmt = select(func.count(Player.id)).where(Player.room_id == room.id)
    players_count = (await db.execute(players_count_stmt)).scalar()
    
    # Contar mesas
    tables_count_stmt = select(func.count(Table.id)).where(Table.room_id == room.id)
    tables_count = (await db.execute(tables_count_stmt)).scalar()
    
    return RoomPublicData(
        id=room.id,
        hoster_id=room.hoster_id,
        code=room.code,
        hoster=UserOut.model_validate(room.hoster),
        room_settings=(
            RoomSettingsOut.model_validate(room.room_settings)
            if room.room_settings else None
        ),
        tables_number=tables_count,
        players_number=players_count,
    )

# ---------------------- VALIDATIONS ----------------------
async def _validate_user_in_room(user_id: int, room_id: int, db: AsyncSession):
    """ Verificar que el usuario pertenezca a la sala """
    # Verificar si el usuario es el hoster
    room = await room_crud.get_by_id(room_id, db)
    if room.hoster_id == user_id:
        return
    
    # Verificar si el usuario es jugador en la sala
    player = await player_crud.get_filtered(
        search_fields=[
            SearchField(field='user_id', value=user_id),
            SearchField(field='room_id', value=room_id)
        ],
        db=db
    )
    
    if not player:
        raise ValidationException(f'El usuario {user_id} no pertenece a la sala {room_id}')
