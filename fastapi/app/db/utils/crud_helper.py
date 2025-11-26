from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select
from sqlalchemy.future import select
from typing import TypeVar, List
from pydantic import BaseModel
from app.core.exceptions import NotFoundException , AlreadyExistsException 

# Tipo genérico para los modelos
T = TypeVar('T')

# Tipo para campos de busqueda
class SearchField(BaseModel):
    field: str
    value: str | int

# Ejecutar consulta y obtener uno o ningún registro
async def get_one_or_none(stmt: Select, db: AsyncSession) -> T | None:
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

# Ejecutar consulta y obtener lista de registro
async def get_many(stmt: Select, db: AsyncSession) -> list[T]:
    result = await db.execute(stmt)
    return result.scalars().all()

# Obtener todos los registros de una tabla
async def get_all(table: T, db: AsyncSession) -> list[T]:
    stmt = select(table)
    return await get_many(stmt, db)

# Generar respuesta según uno o varios campos de búsqueda
def generate_response(search_fields: List[SearchField]) -> str:
    if len(search_fields) == 1:
        return f'{search_fields[0].field.title()} {search_fields[0].value}'
    else:
        response = 'Conjunto de búsqueda'
        for sf in search_fields:
            response += f' {sf.field.title()} {sf.value}'
        return response

# Validar existencia de un objeto en la db
def ensure_exists(obj: T | None, search_fields: List[SearchField]) -> None:
    if not obj:
        raise NotFoundException (f'{generate_response(search_fields)} no encontrado.')

def ensure_not_exists(obj: T | None, search_fields: List[SearchField]) -> None:
    if obj:
        raise AlreadyExistsException (f'{generate_response(search_fields)} ya existe.')

# Buscar un objeto en la db y validar su existencia
async def get_validated(
    stmt: Select,
    should_exist: bool,
    search_fields: List[SearchField],
    db: AsyncSession
) -> T | None:
    obj: T = await get_one_or_none(stmt, db)
    
    if should_exist: ensure_exists(obj, search_fields)
    else: ensure_not_exists(obj, search_fields)
    
    return obj

def update_fields(obj, data: dict):
    for key, value in data.items():
        if value is not None:     # evita sobreescribir con None
            setattr(obj, key, value)

# Eliminar un objeto de la db
async def delete(obj: T, db: AsyncSession) -> None:
    await db.delete(obj)
    await db.commit()

# Aplicar cambios a la db y devolver el objeto actualizado
async def commit_and_refresh(obj: T, db: AsyncSession) -> T:
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj
