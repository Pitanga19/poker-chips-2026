from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ValidationException
from app.db.utils.base_crud import BaseCRUD
from app.db.utils.crud_helper import SearchField
from app.db.tables.rooms.model import Room
from app.db.tables.rooms.schemas import RoomCreate, RoomOptional
from app.db.tables.users.crud import user_crud
import random
import string

class RoomCRUD(BaseCRUD[Room, RoomCreate, RoomOptional]):
    async def validate_create(self, data: RoomCreate, db: AsyncSession):
        # Verificar que el hoster exista
        await user_crud.get_by_id(data.hoster_id, db)
        
        # Impedir usar un código personalizado
        if data.code is not None:
            raise ValidationException('El código será proporcionado por la aplicación.')
        
        # Generar código único
        data.code = await self._generate_unique_code(4, db)
    
    async def validate_update(self, id: int, data: RoomOptional, db: AsyncSession):
        # Impedir la actualización del código
        if data.code is not None:
            raise ValidationException('El código de la room no puede ser actualizado.')
        
        # Verificar que el hoster exista
        if data.hoster_id:
            await user_crud.get_by_id(data.hoster_id, db)
    
    async def _generate_unique_code(self, length: int, db: AsyncSession) -> str:
        # Generar un código aleatorio único
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
            existing = await self.get_filtered([SearchField(field='code', value=code)], db)
            if not existing:
                return code

room_crud = RoomCRUD(Room, RoomCreate, RoomOptional)
