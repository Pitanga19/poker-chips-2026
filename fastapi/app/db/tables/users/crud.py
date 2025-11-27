from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.utils import crud_helper as helper
from app.db.utils.base_crud import BaseCRUD
from app.db.tables.users.model import User
from app.db.tables.users.schemas import UserCreate, UserOptional
from app.core.security import hash_password

class UserCRUD(BaseCRUD[User, UserCreate, UserOptional]):
    async def validate_create(self, data: UserCreate, db: AsyncSession):
        # Verificar si username ya existe
        await helper.get_validated(
            stmt=select(User).where(User.username == data.username),
            should_exist=False,
            search_fields=[helper.SearchField(field='username', value=data.username)],
            db=db
        )

    async def validate_update(self, id: int, data: UserOptional, db: AsyncSession):
        # Si quiere cambiar username, verificar duplicado
        if data.username:
            await helper.get_validated(
                stmt=select(User).where(User.username == data.username, User.id != id),
                should_exist=False,
                search_fields=[helper.SearchField(field='username', value=data.username)],
                db=db
            )

    async def validate_common(self, data, db: AsyncSession) -> dict:
        fields = data.model_dump(exclude_unset=True)

        # Si modificó password, hashearla
        if 'password' in fields:
            fields['hashed_password'] = hash_password(fields.pop('password'))

        return fields

user_crud = UserCRUD(User, UserCreate, UserOptional)
