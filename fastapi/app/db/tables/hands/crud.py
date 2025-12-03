from sqlalchemy.ext.asyncio import AsyncSession
from app.db.utils.base_crud import BaseCRUD
from app.db.tables.hands.model import Hand
from app.db.tables.hands.schemas import HandCreate, HandOptional
from app.db.tables.tables.crud import table_crud
from app.core.exceptions import ValidationException

class HandCRUD(BaseCRUD[Hand, HandCreate, HandOptional]):
    async def validate_create(self, data: HandCreate, db: AsyncSession):
        # Verificar que exista el juego
        game = await table_crud.get_by_id(data.game_id, db)
    
    async def validate_update(self, id: int, data: HandOptional, db: AsyncSession):
        # Impedir modificación de juego
        if data.game_id is not None:
            raise ValidationException(
                'No se puede modificar game_id de una hand existente'
            )

hand_crud = HandCRUD(Hand, HandCreate, HandOptional)
