from sqlalchemy.ext.asyncio import AsyncSession
from app.db.utils.base_crud import BaseCRUD
from app.db.tables.bet_rounds.model import BetRound
from app.db.tables.bet_rounds.schemas import BetRoundCreate, BetRoundOptional
from app.db.tables.hands.crud import hand_crud
from app.core.exceptions import ValidationException

class BetRoundCRUD(BaseCRUD[BetRound, BetRoundCreate, BetRoundOptional]):
    async def validate_create(self, data: BetRoundCreate, db: AsyncSession):
        # Verificar que exista la mano
        hand = await hand_crud.get_by_id(data.hand_id, db)
    
    async def validate_update(self, id: int, data: BetRoundOptional, db: AsyncSession):
        # Impedir modificación de mesa
        if data.hand_id is not None:
            raise ValidationException(
                'No se puede modificar hand_id de un bet_round existente'
            )

bet_round_crud = BetRoundCRUD(BetRound, BetRoundCreate, BetRoundOptional)
