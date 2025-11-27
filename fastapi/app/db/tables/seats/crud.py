from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.utils import crud_helper as helper
from app.db.utils.base_crud import BaseCRUD
from app.db.tables.seats.model import Seat
from app.db.tables.seats.schemas import SeatCreate, SeatOptional
from app.core.exceptions import ValidationException

class SeatCRUD(BaseCRUD[Seat, SeatCreate, SeatOptional]):
    async def validate_create(self, data: SeatCreate, db: AsyncSession):
        # Verificar si ese usuario ya está como seat en esa room
        await helper.get_filtered(
            model=Seat,
            search_fields=[
                helper.SearchField(field='user_id', value=data.user_id),
                helper.SearchField(field='room_id', value=data.room_id),
            ],
            db=db
        )

    async def validate_update(self, id: int, data: SeatOptional, db: AsyncSession):
        # Verificar si ese usuario ya está como seat en esa room
        if data.user_id or data.room_id:
            raise ValidationException(
                'No se puede modificar user_id o room_id de un seat existente'
            )


seat_crud = SeatCRUD(Seat, SeatCreate, SeatOptional)
