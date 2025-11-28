from sqlalchemy.ext.asyncio import AsyncSession
from app.db.utils import crud_helper as helper
from app.db.utils.base_crud import BaseCRUD
from app.db.tables.seats.model import Seat
from app.db.tables.seats.schemas import SeatCreate, SeatOptional
from app.db.tables.players.crud import player_crud
from app.db.tables.tables.crud import table_crud
from app.core.exceptions import ValidationException

class SeatCRUD(BaseCRUD[Seat, SeatCreate, SeatOptional]):
    async def validate_create(self, data: SeatCreate, db: AsyncSession):
        # Verificar si la posición ya está ocupada en la mesa
        existing_position = await helper.get_filtered(
            model=Seat,
            search_fields=[
                helper.SearchField(field='table_id', value=data.table_id),
                helper.SearchField(field='position', value=data.position),
            ],
            db=db
        )
        if len(existing_position) > 0:
            raise ValidationException(
                f'La posición {data.position} ya está ocupada en la mesa {data.table_id}'
            )

        # Verificar vacante con player_id
        if data.vacate and data.player_id is not None:
            raise ValidationException(
                'No se puede asignar un jugador a un asiento marcado como vacante'
            )
        elif not data.vacate and data.player_id is None:
            raise ValidationException(
                'Debe asignar un jugador a un asiento que no está vacante'
            )

        if data.player_id is not None:
            await self._validate_player(data.player_id, data.table_id, db)

    async def validate_update(self, id: int, data: SeatOptional, db: AsyncSession):
        seat = await self.get_by_id(id=id, db=db)

        if data.table_id is not None:
            raise ValidationException('No se puede modificar table_id de un seat existente')

        if data.position is not None:
            existing_position = await helper.get_filtered(
                model=Seat,
                search_fields=[
                    helper.SearchField(field='table_id', value=seat.table_id),
                    helper.SearchField(field='position', value=data.position),
                ],
                db=db,
                exclude_fields=[helper.SearchField(field='id', value=id)]
            )
            if existing_position:
                raise ValidationException(
                    f'La posición {data.position} ya está ocupada en la mesa {seat.table_id}'
                )

        # Verificar vacante
        if data.vacate is True:
            data.player_id = None  # Liberar asiento
        elif data.vacate is False and data.player_id is None:
            raise ValidationException(
                'Debe asignar un jugador a un asiento que no está vacante'
            )

        if data.player_id is not None:
            await self._validate_player(data.player_id, seat.table_id, db, exclude_seat_id=id)

    async def _validate_player(self, player_id: int, table_id: int, db: AsyncSession, exclude_seat_id: int = None):
        # Verificar existencia del jugador
        player = await player_crud.get_by_id(id=player_id, db=db)

        # Verificar que el jugador pertenece a la misma sala que la mesa
        table = await table_crud.get_by_id(id=table_id, db=db)
        if player.room_id != table.room_id:
            raise ValidationException(
                f'El jugador con id {player_id} no pertenece a la misma sala que la mesa {table_id}'
            )

        # Verificar si el jugador ya está en esta mesa
        user_in_table = await helper.get_filtered(
            model=Seat,
            search_fields=[
                helper.SearchField(field='table_id', value=table_id),
                helper.SearchField(field='player_id', value=player.id),
            ],
            db=db,
            exclude_fields=[helper.SearchField(field='id', value=exclude_seat_id)] if exclude_seat_id else None
        )
        if len(user_in_table) > 0:
            raise ValidationException(
                f'El usuario con id {player_id} ya está sentado en la mesa {table_id}'
            )

        # Verificar si el jugador ya está en otra mesa de la misma sala
        other_tables = await table_crud.get_filtered(
            search_fields=[helper.SearchField(field='room_id', value=table.room_id)],
            db=db,
            exclude_fields=[helper.SearchField(field='id', value=table_id)]
        )
        for other_table in other_tables:
            seat_in_other_table = await helper.get_filtered(
                model=Seat,
                search_fields=[
                    helper.SearchField(field='table_id', value=other_table.id),
                    helper.SearchField(field='player_id', value=player.id),
                ],
                db=db,
                exclude_fields=[helper.SearchField(field='id', value=exclude_seat_id)] if exclude_seat_id else None
            )
            if len(seat_in_other_table) > 0:
                raise ValidationException(
                    f'El usuario con id {player_id} ya está sentado en otra mesa de la misma sala'
                )

seat_crud = SeatCRUD(Seat, SeatCreate, SeatOptional)
