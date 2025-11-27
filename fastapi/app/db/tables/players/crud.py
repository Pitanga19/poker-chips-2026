from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.utils import crud_helper as helper
from app.db.utils.base_crud import BaseCRUD
from app.db.tables.players.model import Player
from app.db.tables.players.schemas import PlayerCreate, PlayerOptional
from app.db.tables.users.crud import user_crud
from app.db.tables.rooms.crud import room_crud
from app.core.exceptions import ValidationException

class PlayerCRUD(BaseCRUD[Player, PlayerCreate, PlayerOptional]):
    async def validate_create(self, data: PlayerCreate, db: AsyncSession):
        # Verificar que exista el usuario
        user = await user_crud.get_by_id(id=data.user_id, db=db)
        
        # Verificar que exista la sala
        room = await room_crud.get_by_id(id=data.room_id, db=db)
        
        # Verificar si ese usuario ya está como player en esa room
        user_in_room = await helper.get_filtered(
            model=Player,
            search_fields=[
                helper.SearchField(field='user_id', value=data.user_id),
                helper.SearchField(field='room_id', value=data.room_id),
            ],
            db=db
        )
        if user_in_room: raise ValidationException(
            f'El usuario con id {data.user_id} ya está en esa sala'
        )

    async def validate_update(self, id: int, data: PlayerOptional, db: AsyncSession):
        # Verificar si ese usuario ya está como player en esa room
        if data.user_id or data.room_id:
            raise ValidationException(
                'No se puede modificar user_id o room_id de un player existente'
            )


player_crud = PlayerCRUD(Player, PlayerCreate, PlayerOptional)
