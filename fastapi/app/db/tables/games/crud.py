from sqlalchemy.ext.asyncio import AsyncSession
from app.db.utils.base_crud import BaseCRUD
from app.db.tables.games.model import Game
from app.db.tables.games.schemas import GameCreate, GameOptional
from app.db.tables.tables.crud import table_crud
from app.core.exceptions import ValidationException

class GameCRUD(BaseCRUD[Game, GameCreate, GameOptional]):
    async def validate_create(self, data: GameCreate, db: AsyncSession):
        # Verificar que exista la mesa
        user = await table_crud.get_by_id(data.table_id, db)
    
    async def validate_update(self, id: int, data: GameOptional, db: AsyncSession):
        # Impedir modificación de mesa
        if data.table_id is not None:
            raise ValidationException(
                'No se puede modificar table_id de un game existente'
            )

game_crud = GameCRUD(Game, GameCreate, GameOptional)
