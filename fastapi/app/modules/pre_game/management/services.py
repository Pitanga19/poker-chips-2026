from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ValidationException, UnauthorizedException
from app.db.utils.crud_helper import SearchField
from app.db.tables.rooms.crud import room_crud
from app.db.tables.rooms.schemas import RoomCreate
from app.db.tables.room_settings.crud import room_settings_crud
from app.db.tables.room_settings.schemas import RoomSettingsBase, RoomSettingsCreate, RoomSettingsOptional
from app.db.tables.tables.crud import table_crud
from app.db.tables.tables.schemas import TableCreate
from app.db.tables.seats.crud import seat_crud
from app.db.tables.seats.schemas import SeatCreate
from app.db.tables.players.crud import player_crud
from app.db.tables.players.schemas import PlayerCreate, PlayerOptional
from app.modules.pre_game.schemas.api import (
    CreateRoomResponse, UpdateRoomSettingsResponse,
    CreateTableBody, CreateTableResponse,
    CreateSeatBody, CreateSeatResponse,
    UpdateStackOperation, UpdateStackBody, UpdateStackResponse
)

async def create_room(
    user_id: int,
    room_pre_game_settings_data: RoomSettingsBase,
    db: AsyncSession
) -> dict:
    """Crear una sala con configuración y jugador hoster"""
    # Crear la sala
    room_create_data = RoomCreate(hoster_id=user_id)
    room = await room_crud.create(room_create_data, db)

    # Crear configuración de la sala
    room_settings_create_data = RoomSettingsCreate(
        **room_pre_game_settings_data.model_dump(),
        room_id=room.id
    )
    room_settings = await room_settings_crud.create(room_settings_create_data, db)

    # Crear jugador hoster con stack si corresponde
    player_create_data = PlayerCreate(
        user_id=user_id,
        room_id=room.id,
        stack=room_settings.buy_in if room_settings.use_default_buy_in else 0
    )
    player = await player_crud.create(player_create_data, db)
    
    return CreateRoomResponse(
        hoster_id=user_id,
        player_id=player.id,
        room_id=room.id,
        room_code=room.code
    )

async def update_room_settings(
    hoster_id: int,
    room_id: int,
    room_settings_update_data: RoomSettingsOptional,
    db: AsyncSession
) -> None:
    """ Actualizar configuración de sala por hoster """
    # Verificar que la sala exista y el usuario sea hoster
    await _validate_room_hoster(hoster_id, room_id, db)
    
    # Obtener room_settings verificando que existe
    room_settings_search_result = await room_settings_crud.get_filtered(
        search_fields=[
            SearchField(field='room_id', value=room_id)
        ],
        db=db
    )
    if not room_settings_search_result:
        raise ValidationException(f'La sala {room_id} no tiene configuración')
    room_settings = room_settings_search_result[0]
    
    # Actualizar room_settings
    await room_settings_crud.update(room_settings.id, room_settings_update_data, db)
    
    return UpdateRoomSettingsResponse(
        hoster_id=hoster_id,
        room_id=room_id,
        room_settings_id=room_settings.id,
    )

async def create_table(
    hoster_id: int,
    room_id: int,
    create_table_body: CreateTableBody,
    db: AsyncSession,
) -> dict:
    """ Crear mesa con asientos """
    # Verificar que la sala exista y el usuario sea hoster
    await _validate_room_hoster(hoster_id, room_id, db)
    
    # Extraer y verificar el número de asientos
    seats_number = create_table_body.seats_number
    if seats_number < 2 or seats_number > 12:
        raise ValidationException('El número de asientos debe estar entre 2 y 12')
    
    # Crear la mesa
    table = await table_crud.create(TableCreate(room_id=room_id), db)
    
    # Crear los asientos
    seat_ids = []
    for pos in range(1, seats_number + 1):
        seat = await seat_crud.create(SeatCreate(table_id=table.id, position=pos), db)
        seat_ids.append(seat.id)
    
    return CreateTableResponse(
        hoster_id=hoster_id,
        room_id=room_id,
        table_id=table.id,
        seats_id_list=seat_ids,
    )

async def delete_table(
    hoster_id: int,
    room_id: int,
    table_id: int,
    db: AsyncSession
) -> None:
    """ Eliminar mesa de una sala """
    # Verificar que la sala exista y el usuario sea hoster
    await _validate_room_hoster(hoster_id, room_id, db)
    
    # Verificar que la mesa exista en la sala
    await _validate_table_room(table_id, room_id, db)
    
    # Eliminar la mesa (sus asientos son eliminados en el CRUD)
    await table_crud.delete(table_id, db)

async def create_seat(
    hoster_id: int,
    room_id: int,
    table_id: int,
    create_seat_body: CreateSeatBody,
    db: AsyncSession,
) -> dict:
    """ Crear asiento en una mesa """
    # Verificar que la sala exista y el usuario sea hoster
    await _validate_room_hoster(hoster_id, room_id, db)
    
    # Verificar que la mesa exista en la sala
    await _validate_table_room(table_id, room_id, db)
    
    # Obtener posición recibida
    position = create_seat_body.position
    
    # Crear asiento (Verifica que la posición no esté ocupada en el CRUD)
    seat = await seat_crud.create(SeatCreate(table_id=table_id, position=position), db)
    
    return CreateSeatResponse(
        hoster_id=hoster_id,
        room_id=room_id,
        table_id=table_id,
        seat_id=seat.id,
    )

async def delete_seat(
    hoster_id: int,
    room_id: int,
    table_id: int,
    seat_id: int,
    db: AsyncSession
) -> None:
    """ Eliminar asiento de una mesa """
    # Verificar que la sala exista y el usuario sea hoster
    await _validate_room_hoster(hoster_id, room_id, db)
    
    # Verificar que la mesa exista en la sala
    await _validate_table_room(table_id, room_id, db)
    
    # Verificar que el asiento exista en la mesa
    await _validate_seat_table(seat_id, table_id, db)
    
    # Eliminar asiento
    await seat_crud.delete(seat_id, db)

async def update_stack(
    hoster_id: int,
    room_id: int,
    player_id: int,
    update_stack_body: UpdateStackBody,
    db: AsyncSession
) -> UpdateStackResponse:
    """ Actualizar stack de jugador """
    # Verificar que la sala exista y el usuario sea hoster
    await _validate_room_hoster(hoster_id, room_id, db)
    
    # Verificar que el jugador pertenezca a la sala
    player = await player_crud.get_by_id(player_id, db)
    if not player or player.room_id != room_id:
        raise ValidationException(f'El jugador {player_id} no pertenece a la sala {room_id}')
    
    # Obtener data del body
    operation = update_stack_body.operation
    amount = update_stack_body.amount
    
    # Obtener valor de nuevo stack
    new_stack = player.stack
    match operation:
        case UpdateStackOperation.SET:
            new_stack = amount
        case UpdateStackOperation.ADD:
            new_stack += amount
        case UpdateStackOperation.SUB:
            new_stack -= amount
    
    # Actualizar player
    player_update_data = PlayerOptional(stack=new_stack)
    await player_crud.update(player.id, player_update_data, db)
    
    return UpdateStackResponse(
        hoster_id=hoster_id,
        room_id=room_id,
        user_id=player.user_id,
        player_id=player_id,
        new_stack=new_stack,
    )

async def _validate_room_hoster(hoster_id: int, room_id: int, db: AsyncSession):
    """ Verificar que la sala exista y el usuario sea hoster """
    # Verificar que la sala exista
    room = await room_crud.get_by_id(room_id, db)
    if not room:
        raise ValidationException(f'La sala {room_id} no existe')
    
    # Verificar que sea hoster de la sala
    if room.hoster_id != hoster_id:
        raise UnauthorizedException(f'Usuario {hoster_id} no es hoster de la sala {room_id}')
    return room

async def _validate_table_room(table_id: int, room_id: int, db: AsyncSession):
    """ Verificar que la mesa exista en la sala """
    table = await table_crud.get_by_id(table_id, db)
    if not table or table.room_id != room_id:
        raise ValidationException(f'La mesa {table_id} no existe en la sala {room_id}')
    return table

async def _validate_seat_table(seat_id: int, table_id: int, db: AsyncSession):
    """ Verificar que el asiento exista en la mesa """
    seat = await seat_crud.get_by_id(seat_id, db)
    if not seat or seat.table_id != table_id:
        raise ValidationException(f'Asiento {seat_id} no existe en la mesa {table_id}')
    return seat
