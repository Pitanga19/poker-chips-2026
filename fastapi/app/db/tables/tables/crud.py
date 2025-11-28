from app.db.utils.base_crud import BaseCRUD
from app.db.tables.tables.model import Table
from app.db.tables.tables.schemas import TableCreate, TableOptional
from app.db.tables.rooms.crud import room_crud
from app.core.exceptions import ValidationException

class TableCRUD(BaseCRUD[Table, TableCreate, TableOptional]):
    async def validate_create(self, data: TableCreate, db):
        await room_crud.get_by_id(data.room_id, db)
    
    async def validate_update(self, id: int, data: TableOptional, db):
        if data.room_id is not None:
            raise ValidationException('No se puede cambiar la sala de una mesa existente')

table_crud = TableCRUD(Table, TableCreate, TableOptional)
