from typing import Generic, TypeVar, Type, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from app.db.utils import crud_helper as helper

# --- TypeVars ---
ModelType = TypeVar('ModelType') # SQLAlchemy model
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)

class BaseCRUD(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(
        self,
        model: Type[ModelType],
        schema_create: Type[CreateSchemaType],
        schema_update: Type[UpdateSchemaType]
    ):
        self.model = model
        self.schema_create = schema_create
        self.schema_update = schema_update

    async def validate_create(self, data: CreateSchemaType, db: AsyncSession) -> None:
        # A definir en la subclase
        pass
    
    async def validate_update(self, id: int, data: UpdateSchemaType, db: AsyncSession) -> None:
        # A definir en la subclase
        pass
    
    async def validate_common(self, data: BaseModel, db: AsyncSession) -> dict:
        return data.model_dump(exclude_unset=True)

    async def create(self, data: CreateSchemaType, db: AsyncSession) -> ModelType:
        data = self.schema_create(**data.model_dump())
        await self.validate_create(data, db)
        fields = await self.validate_common(data, db)

        obj = self.model(**fields)
        return await helper.commit_and_refresh(obj, db)

    async def get_by_id(self, id: int, db: AsyncSession) -> ModelType:
        return await helper.get_validated(
            stmt = select(self.model).filter_by(id=id),
            should_exist = True,
            search_fields = [helper.SearchField(field='id', value=id)],
            db = db
        )

    async def get_filtered(
        self,
        search_fields: List[helper.SearchField],
        db: AsyncSession,
        exclude_fields: Optional[List[helper.SearchField]] = None
    ) -> List[ModelType]:
        return await helper.get_filtered(self.model, search_fields, db, exclude_fields)

    async def get_all(self, db: AsyncSession) -> List[ModelType]:
        return await helper.get_all(self.model, db)

    async def update(self, id: int, data: UpdateSchemaType, db: AsyncSession) -> ModelType:
        data = self.schema_update(**data.model_dump(exclude_unset=True))
        obj = await self.get_by_id(id, db)

        await self.validate_update(id, data, db)
        fields = await self.validate_common(data, db)

        for k, v in fields.items():
            setattr(obj, k, v)

        return await helper.commit_and_refresh(obj, db)

    async def delete(self, id: int, db: AsyncSession) -> bool:
        obj = await self.get_by_id(id, db)
        await helper.delete(obj, db)
        return True
