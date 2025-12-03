from sqlalchemy.ext.asyncio import AsyncSession
from app.db.utils.base_crud import BaseCRUD
from app.db.tables.pot_players.model import PotPlayer
from app.db.tables.pot_players.schemas import PotPlayerCreate, PotPlayerOptional
from app.db.tables.pots.crud import pot_crud
from app.db.tables.players.crud import player_crud
from app.core.exceptions import ValidationException

class PotPlayerCRUD(BaseCRUD[PotPlayer, PotPlayerCreate, PotPlayerOptional]):
    async def validate_create(self, data: PotPlayerCreate, db: AsyncSession):
        # Verificar que exista el pot
        pot = await pot_crud.get_by_id(data.pot_id, db)
        
        # Verificar que exista el player
        player = await player_crud.get_by_id(data.player_id, db)
    
    async def validate_update(self, id: int, data: PotPlayerOptional, db: AsyncSession):
        # Impedir modificación de relación
        raise ValidationException('No se puede modificar una relación pot_player-player')
    
    async def update(self, id: int, data: PotPlayerOptional, db: AsyncSession):
        pass

pot_player_crud = PotPlayerCRUD(PotPlayer, PotPlayerCreate, PotPlayerOptional)
