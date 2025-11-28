from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from typing import Optional
from app.modules.auth.schemas import AuthLoginData, AuthRegisterData, Token
from app.modules.auth.security import verify_password, create_access_token
from app.db.tables.users.schemas import UserCreate
from app.db.tables.users.model import User
from app.db.tables.users.crud import user_crud

# Registrar usuario
async def register_user(user_data: AuthRegisterData, db: AsyncSession) -> User:
    # Verificar misma contraseña
    if user_data.password != user_data.password_confirm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Las contraseñas no coinciden'
        )
    
    # Extraer datos
    create_data = UserCreate(
        username=user_data.username,
        password=user_data.password,
    )
    
    # Crear usuario (hashea la contraseña en el CRUD)
    return await user_crud.create(create_data, db)

# Obtener usuario por username
async def get_user_by_username(username: str, db: AsyncSession) -> Optional[User]:
    stmt = select(User).where(User.username == username)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def authenticate_user(login_data: AuthLoginData, db: AsyncSession) -> User:
    username = login_data.username
    password = login_data.password
    user = await get_user_by_username(username, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Credenciales incorrectas'
        )

    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Credenciales incorrectas'
        )

    return user

async def login_user(login_data: AuthLoginData, db: AsyncSession) -> Token:
    user = await authenticate_user(login_data, db)

    token_data = {
        'id': user.id,
        'username': user.username
    }

    access_token = create_access_token(token_data)

    return Token(
        access_token=access_token,
        token_type='bearer'
    )

async def get_current_user_service(user_id: int, db: AsyncSession) -> User:
    user = await user_crud.get_by_id(user_id, db)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Usuario no encontrado'
        )
    
    return user

# Logout: opcionalmente podés implementar blacklist de JWT en el futuro
async def logout_user_service(token: str) -> dict:
    """
    Logout de usuario. Actualmente solo devuelve mensaje.
    Token podría agregarse a blacklist si implementás control de revocación.
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Token requerido para logout'
        )

    # Por ahora no hacemos nada con el token, solo respondemos
    return {'msg': 'Logout exitoso'}
