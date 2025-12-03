from sqlalchemy.ext.asyncio import AsyncSession
from app.db.utils.base_crud import BaseCRUD
from app.db.tables.turns.model import Turn
from app.db.tables.turns.schemas import TurnCreate, TurnOptional
from app.db.tables.bet_rounds.crud import bet_round_crud
from app.db.tables.players.crud import player_crud
from app.core.exceptions import ValidationException

class TurnCRUD(BaseCRUD[Turn, TurnCreate, TurnOptional]):
    async def validate_create(self, data: TurnCreate, db: AsyncSession):
        # Verificar que exista la ronda de apuestas
        bet_round = await bet_round_crud.get_by_id(data.bet_round_id, db)
        
        # Verificar que exista el jugador
        player = await player_crud.get_by_id(data.player_id, db)
    
    async def validate_update(self, id: int, data: TurnOptional, db: AsyncSession):
        # Impedir modificación de ronda de apuestas o jugador
        if (data.game_id is not None) or (data.player_id is not None):
            raise ValidationException(
                'No se puede modificar bet_round_id ni player_id de una turn existente'
            )

turn_crud = TurnCRUD(Turn, TurnCreate, TurnOptional)
