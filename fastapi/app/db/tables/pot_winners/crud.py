from sqlalchemy.ext.asyncio import AsyncSession
from app.db.utils.base_crud import BaseCRUD
from app.db.tables.pot_winners.model import PotWinner
from app.db.tables.pot_winners.schemas import PotWinnerCreate, PotWinnerOptional
from app.db.tables.pots.crud import pot_crud
from app.db.tables.players.crud import player_crud
from app.core.exceptions import ValidationException

class PotWinnerCRUD(BaseCRUD[PotWinner, PotWinnerCreate, PotWinnerOptional]):
    async def validate_create(self, data: PotWinnerCreate, db: AsyncSession):
        # Verificar que exista el pot
        pot = await pot_crud.get_by_id(data.pot_id, db)
        
        # Verificar que exista el player
        player = await player_crud.get_by_id(data.winner_id, db)
    
    async def validate_update(self, id: int, data: PotWinnerOptional, db: AsyncSession):
        # Impedir modificación de mesa
        if (data.pot_id is not None) or (data.player_id is not None):
            raise ValidationException(
                'No se puede modificar pot_id ni winner_id de una relación pot_winner'
            )

pot_winner_crud = PotWinnerCRUD(PotWinner, PotWinnerCreate, PotWinnerOptional)
