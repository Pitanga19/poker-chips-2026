from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.utils import crud_helper as helper
from app.db.utils.base_crud import BaseCRUD
from app.db.tables.players.model import Player
from app.db.tables.players.schemas import PlayerCreate, PlayerOptional
from app.core.exceptions import ValidationException

class PlayerCRUD(BaseCRUD[Player, PlayerCreate, PlayerOptional]):
    async def validate_create(self, data: PlayerCreate, db: AsyncSession):
        # Verificar si ese usuario ya está como player en esa room
        await helper.get_filtered(
            model=Player,
            search_fields=[
                helper.SearchField(field='user_id', value=data.user_id),
                helper.SearchField(field='room_id', value=data.room_id),
            ],
            db=db
        )

    async def validate_update(self, id: int, data: PlayerOptional, db: AsyncSession):
        # Verificar si ese usuario ya está como player en esa room
        if data.user_id or data.room_id:
            raise ValidationException(
                'No se puede modificar user_id o room_id de un player existente'
            )


player_crud = PlayerCRUD(Player, PlayerCreate, PlayerOptional)
