from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ValidationException
from app.db.utils.crud_helper import SearchField
from app.db.tables.room_settings.crud import room_settings_crud
from app.db.tables.rooms.crud import room_crud
from app.db.tables.tables.crud import table_crud
from app.db.tables.seats.crud import seat_crud
from app.db.tables.seats.schemas import SeatOptional
from app.db.tables.players.crud import player_crud
from app.db.tables.players.schemas import PlayerCreate, PlayerOptional
from app.modules.pre_game.schemas.api import (
    JoinRoomResponse, ChipsPurchaseBody, ChipsPurchaseResponse, JoinTableBody, JoinTableResponse, ChangeSeatBody, ChangeSeatResponse
)

async def join_room(
    user_id: int,
    room_id: int,
    db: AsyncSession
) -> JoinRoomResponse:
    """ Usuario se une a una sala existente """
    # Obtener sala por su código
    room = await room_crud.get_by_id(room_id, db)
    if not room:
        raise ValidationException(f'La sala {room_id} no existe')
    
    # Chequear duplicado: usuario ya está en la sala
    existing_players = await player_crud.get_filtered(
        search_fields=[
            SearchField(field='user_id', value=user_id),
            SearchField(field='room_id', value=room.id)
        ],
        db=db
    )
    if existing_players:
        raise ValidationException(f'El usuario ya está en la sala {room.id}')

    # Obtener configuración de la sala
    room_settings = await _get_room_settings(room.id, db)

    # Crear jugador con stack según configuración
    player_create_data = PlayerCreate(
        user_id=user_id,
        room_id=room.id,
        stack=room_settings.buy_in if room_settings.use_default_buy_in else 0
    )
    player = await player_crud.create(player_create_data, db)

    return JoinRoomResponse(
        room_id=room.id,
        user_id=user_id,
        player_id=player.id,
    )

async def leave_room(user_id: int, room_id: int, db: AsyncSession) -> None:
    """ Jugador abandona la sala y libera asiento si corresponde """
    # Obtener jugador
    player = await _get_player_in_room(user_id, room_id, db)
    
    # Obtener la sala
    room = await room_crud.get_by_id(room_id, db)
    
    # Verificar que no sea el hoster
    if room.hoster_id == user_id:
        raise ValidationException(f'El hoster no puede abandonar la sala')
    
    # Liberar asiento si está sentado
    seats_search = await seat_crud.get_filtered(
        search_fields=[SearchField(field='player_id', value=player.id)],
        db=db
    )
    if len(seats_search) > 0:
        seat = seats_search[0]
        seat_update_data = SeatOptional(player_id=None, vacate=True)
        await seat_crud.update(seat.id, seat_update_data, db)

    # Eliminar jugador
    await player_crud.delete(player.id, db)

async def chips_purchase(
    user_id: int,
    room_id: int,
    chips_purchase_body: ChipsPurchaseBody,
    db: AsyncSession
) -> ChipsPurchaseResponse:
    """ Jugador compra fichas dentro de la sala """
    # Obtener jugador
    player = await _get_player_in_room(user_id, room_id, db)
    
    # Obtener la cantidad de compra
    amount = chips_purchase_body.amount
    
    # Sumar las fichas compradas
    new_stack = player.stack + amount
    player_update_data = PlayerOptional(stack=new_stack)
    await player_crud.update(player.id, player_update_data, db)
    
    return ChipsPurchaseResponse(
        user_id=user_id,
        player_id=player.id,
        new_stack=new_stack,
    )

async def join_table(
    user_id: int,
    room_id: int,
    table_id: int,
    join_table_body: JoinTableBody,
    db: AsyncSession,
) -> JoinTableResponse:
    """ Jugador se sienta en una mesa """
    # Obtener la configuración de la sala
    room_settings = await _get_room_settings(room_id, db)
    
    # Obtener la mesa
    table = await table_crud.get_by_id(table_id, db)
    if not table:
        raise ValidationException(f'La mesa {table_id} no existe')
    
    # Obtener el jugador del usuario que comparta sala con la mesa
    player = await _get_player_in_room(user_id, table.room_id, db)

    # Verificar stack mínimo
    min_stack_required = room_settings.min_stack_bb * room_settings.big_blind
    if player.stack < min_stack_required:
        raise ValidationException(f'Jugador {player.id} no dispone de stack mínimo para la mesa')
    
    # Obtener asiento en la mesa
    search_fields=[
            SearchField(field='table_id', value=table_id),
            SearchField(field='player_id', value=None)
        ]
    
    # Verificar si hay posición solicitada
    position = join_table_body.position
    if position is not None:
        if position < 1 or position > 12:
            raise ValidationException(f'La posición debe estar entre 1 y 12')
        search_fields.append(SearchField(field='position', value=position))
    
    # Obtener el asiento
    seats_search = await seat_crud.get_filtered(
        search_fields=search_fields,
        db=db
    )
    if not seats_search:
        if position is not None:
            raise ValidationException(f'La posición {position} no está disponible')
        raise ValidationException(f'No hay asientos disponibles en esta mesa')
    seat = seats_search[0]

    # Asignar asiento
    await seat_crud.update(seat.id, SeatOptional(player_id=player.id, vacate=False), db)
    
    return JoinTableResponse(
        room_id=room_id,
        user_id=user_id,
        player_id=player.id,
        seat_id=seat.id,
        position=seat.position,
    )

async def leave_table(
    user_id: int,
    room_id: int,
    table_id: int,
    db: AsyncSession
) -> None:
    """ Jugador se levanta de la mesa """
    # Obtener la mesa
    table = await table_crud.get_by_id(table_id, db)
    if not table:
        raise ValidationException(f'La mesa {table_id} no existe')
    
    # Verificar que la mesa pertenezca a la sala
    if table.room_id != room_id:
        raise ValidationException(f'La mesa {table_id} no pertenece a la sala {room_id}')
    
    # Obtener el jugador del usuario que comparta sala con la mesa
    player = await _get_player_in_room(user_id, room_id, db)
    
    # Obtener asiento del jugador en esa mesa
    seats_search = await seat_crud.get_filtered(
        search_fields=[
            SearchField(field='table_id', value=table_id),
            SearchField(field='player_id', value=player.id)
        ],
        db=db
    )
    if not seats_search:
        raise ValidationException(f'Jugador {player.id} no está en la mesa {table_id}')
    seat = seats_search[0]
    
    seat_update_data = SeatOptional(player_id=None, vacate=True)
    await seat_crud.update(seat.id, seat_update_data, db)

async def change_seat(
    user_id: int,
    room_id: int,
    table_id: int,
    change_seat_body: ChangeSeatBody,
    db: AsyncSession
) -> ChangeSeatResponse:
    """ Jugador cambia asiento dentro de la misma mesa """
    # Obtener jugador
    player = await _get_player_in_room(user_id, room_id, db)
    
    # Obtener mesa
    table = await table_crud.get_by_id(table_id, db)
    
    # Verificar que la mesa pertenezca a la sala
    if table.room_id != room_id:
        raise ValidationException(f'La mesa {table_id} no pertenece a la sala {room_id}')
    
    # Obtener asiento actual
    current_seat = await seat_crud.get_filtered(
        search_fields=[SearchField(field='player_id', value=player.id)],
        db=db
    )
    if len(current_seat) == 0:
        raise ValidationException(f'Jugador {player.id} no está sentado en la mesa {table_id}')
    current_seat = current_seat[0]
    if not current_seat:
        raise ValidationException(f'El jugador {player.id} no está sentado en la mesa {table_id}')
    
    # Obtener asiento objetivo
    new_position = change_seat_body.new_position
    new_seat_search = await seat_crud.get_filtered(
        search_fields=[SearchField(field='position', value=new_position)],
        db=db
    )
    if len(new_seat_search) == 0:
        raise ValidationException(f'El asiento {new_position} no existe')
    new_seat = new_seat_search[0]
    
    # Verificar que el asiento objetivo esté disponible
    if new_seat.vacate is False:
        raise ValidationException(f'El asiento {new_position} no está disponible')
    
    # Levantarse del asiento actual
    leave_current_seat_data = SeatOptional(player_id=None, vacate=True)
    await seat_crud.update(current_seat.id, leave_current_seat_data, db)
    
    # Sentarse en el nuevo asiento
    join_new_seat_data = SeatOptional(player_id=player.id, vacate=False)
    await seat_crud.update(new_seat.id, join_new_seat_data, db)
    
    return ChangeSeatResponse(
        room_id=room_id,
        user_id=user_id,
        player_id=player.id,
        new_seat_id=new_seat.id,
        new_position=new_seat.position,
    )

async def _get_room_settings(room_id: int, db: AsyncSession):
    """ Obtener configuración de la sala """
    room_settings_search = await room_settings_crud.get_filtered(
        search_fields=[SearchField(field='room_id', value=room_id)],
        db=db
    )
    if not room_settings_search:
        raise ValidationException(f'La configuración para la sala con id {room_id} no existe')
    return room_settings_search[0]

async def _get_player_in_room(user_id: int, room_id: int, db: AsyncSession):
    player_search = await player_crud.get_filtered(
        search_fields=[
            SearchField(field='user_id', value=user_id),
            SearchField(field='room_id', value=room_id)
        ],
        db=db
    )
    if not player_search:
        raise ValidationException(f'Usuario {user_id} no pertenece a esta sala')
    return player_search[0]
