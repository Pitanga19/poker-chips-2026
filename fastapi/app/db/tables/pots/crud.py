from sqlalchemy.ext.asyncio import AsyncSession
from app.db.utils.base_crud import BaseCRUD
from app.db.tables.pots.model import Pot
from app.db.tables.pots.schemas import PotCreate, PotOptional
from app.db.tables.hands.crud import hand_crud
from app.core.exceptions import ValidationException

class PotCRUD(BaseCRUD[Pot, PotCreate, PotOptional]):
    async def validate_create(self, data: PotCreate, db: AsyncSession):
        # Verificar que exista la mano
        hand = await hand_crud.get_by_id(data.hand_id, db)
    
    async def validate_update(self, id: int, data: PotOptional, db: AsyncSession):
        # Impedir modificación de mesa
        if data.hand_id is not None:
            raise ValidationException(
                'No se puede modificar hand_id de un pot existente'
            )

pot_crud = PotCRUD(Pot, PotCreate, PotOptional)
