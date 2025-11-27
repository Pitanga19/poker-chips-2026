from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.utils import crud_helper as helper
from app.db.utils.base_crud import BaseCRUD
from app.db.tables.seats.model import Seat
from app.db.tables.seats.schemas import SeatCreate, SeatOptional
from app.db.tables.players.crud import player_crud
from app.db.tables.tables.crud import table_crud
from app.core.exceptions import ValidationException

class SeatCRUD(BaseCRUD[Seat, SeatCreate, SeatOptional]):
    async def validate_create(self, data: SeatCreate, db: AsyncSession):
        # Verificar si la posición ya está ocupada en esa mesa
        existing_position = await helper.get_filtered(
            model=Seat,
            search_fields=[
                helper.SearchField(field='table_id', value=data.table_id),
                helper.SearchField(field='position', value=data.position),
            ],
            db=db
        )
        if existing_position: raise ValidationException(
            f'La posición {data.position} ya está ocupada en esa mesa'
        )
        
        if data.player_id:
            # Verificar si ese jugador existe
            player = await player_crud.get_by_id(
                id=data.player_id,
                db=db,
            )
            
            # Verificar si ese jugador pertence a la misma sala que la mesa
            table = await table_crud.get_by_id(
                id=data.table_id,
                db=db,
            )
            if table.room_id != player.room_id:
                raise ValidationException(
                    f'El jugador con id {data.player_id} no pertenece a la misma sala que la mesa {data.table_id}'
                )
            
            # Verificar si ese jugador ya está sentado en esa mesa
            user_in_table = await helper.get_filtered(
                model=Seat,
                search_fields=[
                    helper.SearchField(field='table_id', value=data.table_id),
                    helper.SearchField(field='player_id', value=player.id),
                ],
                db=db,
            )
            if user_in_table: raise ValidationException(
                f'El usuario con id {data.player_id} ya está sentado en esa mesa'
            )

    async def validate_update(self, id: int, data: SeatOptional, db: AsyncSession):
        # Obtener información actual del seat
        seat = await self.get_by_id(id=id, db=db)
        
        # Verificar si ese jugador ya está como seat en esa room
        if data.table_id:
            raise ValidationException(
                'No se puede modificar table_id de un seat existente'
            )
        
        if data.position is not None:
            # Verificar si la posición ya está ocupada en esa mesa
            existing_position = await helper.get_filtered(
                model=Seat,
                search_fields=[
                    helper.SearchField(field='table_id', value=seat.table_id),
                    helper.SearchField(field='position', value=data.position),
                ],
                db=db,
                exclude_fields=[helper.SearchField(field='id', value=id)]
            )
            if existing_position: raise ValidationException(
                f'La posición {data.position} ya está ocupada en esa mesa'
            )
        
        if data.player_id:
            # Verificar si ese jugador existe
            player = await player_crud.get_by_id(
                id=data.player_id,
                db=db,
            )
            
            # Verificar si ese jugador pertence a la misma sala que la mesa
            table = await table_crud.get_by_id(
                id=seat.table_id,
                db=db,
            )
            if table.room_id != player.room_id:
                raise ValidationException(
                    f'El jugador con id {data.player_id} no pertenece a la misma sala que la mesa {seat.table_id}'
                )
            
            # Verificar si ese jugador ya está sentado en esa mesa
            user_in_table = await helper.get_filtered(
                model=Seat,
                search_fields=[
                    helper.SearchField(field='table_id', value=table.id),
                    helper.SearchField(field='player_id', value=player.id),
                ],
                db=db,
                exclude_fields=[helper.SearchField(field='id', value=id)]
            )
            if user_in_table: raise ValidationException(
                f'El usuario con id {data.player_id} ya está sentado en esa mesa'
            )

seat_crud = SeatCRUD(Seat, SeatCreate, SeatOptional)
