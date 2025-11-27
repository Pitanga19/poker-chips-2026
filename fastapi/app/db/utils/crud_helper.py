from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select
from sqlalchemy import select
from typing import TypeVar, List, Type
from pydantic import BaseModel
from app.core.exceptions import NotFoundException, AlreadyExistsException

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

# Ejecutar consulta y obtener varios o ningún registro
async def get_many(stmt: Select, db: AsyncSession) -> list[T]:
    result = await db.execute(stmt)
    return result.scalars().all()

# Obtener registros filtrados según un esquema opcional
async def get_filtered(
    model: Type[T],
    search_fields: List[SearchField],
    db: AsyncSession,
    exclude_fields: List[SearchField] | None = None
) -> List[T]:
    if not search_fields:
        raise ValueError('Debe proporcionar al menos un campo para buscar.')

    stmt = select(model)

    # Aplicar filtros AND
    for sf in search_fields:
        if not hasattr(model, sf.field):
            raise AttributeError(
                f'El modelo {model.__name__} no tiene el campo "{sf.field}".'
            )
        stmt = stmt.where(getattr(model, sf.field) == sf.value)

    # Aplicar exclusiones
    if exclude_fields:
        for ex in exclude_fields:
            if not hasattr(model, ex.field):
                raise AttributeError(
                    f'El modelo {model.__name__} no tiene el campo "{ex.field}".'
                )
            stmt = stmt.where(getattr(model, ex.field) != ex.value)

    return await get_many(stmt, db)

# Ejecutar consulta y obtener todos los registros
async def get_all(table: T, db: AsyncSession) -> list[T]:
    stmt = select(table)
    return await get_many(stmt, db)

# Generar respuesta según uno o varios campos de búsqueda
def generate_response(search_fields: List[SearchField]) -> str:
    if len(search_fields) == 1:
        sf = search_fields[0]
        return f'{sf.field.title()} {sf.value}'
    else:
        return ' | '.join(
            f'{sf.field.title()}={sf.value}' for sf in search_fields
        )

# Validar existencia de un objeto en la db
def ensure_exists(obj: T | None, search_fields: List[SearchField]):
    if not obj:
        raise NotFoundException(f'{generate_response(search_fields)} no encontrado.')

def ensure_not_exists(obj: T | None, search_fields: List[SearchField]):
    if obj:
        raise AlreadyExistsException(f'{generate_response(search_fields)} ya existe.')

# Buscar un objeto en la db y validar su existencia
async def get_validated(
    stmt: Select,
    should_exist: bool,
    search_fields: List[SearchField],
    db: AsyncSession
) -> T | None:
    obj: T = await get_one_or_none(stmt, db)
    
    if should_exist:
        ensure_exists(obj, search_fields)
    else:
        ensure_not_exists(obj, search_fields)
    
    return obj

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

def parse_search_fields(raw: str) -> List[SearchField]:
    """
    Recibe:
        "name:juan,lastname:perez,age:20"
    Devuelve:
        [SearchField(field="name", value="juan"), ...]
    """
    sf_list = []

    for part in raw.split(','):
        if ':' not in part:
            continue
        k, v = part.split(':', 1)

        # convertir números
        if v.isdigit():
            v = int(v)

        sf_list.append(SearchField(field=k, value=v))

    return sf_list
