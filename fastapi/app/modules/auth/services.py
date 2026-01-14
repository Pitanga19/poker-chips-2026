from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from typing import Optional
from app.db.tables.users.schemas import UserCreate
from app.db.tables.users.model import User
from app.db.tables.users.crud import user_crud
from app.modules.auth.security import verify_password, create_access_token
from app.modules.auth.schemas import (
    AuthLoginData,
    AuthRegisterData,
    Token,
    TokenData,
    AuthResponse
)

def _create_auth_response(user_id: int, username: str) -> AuthResponse:
    token_data = TokenData(id=user_id, username=username)
    access_token = create_access_token(token_data.model_dump())
    token=Token(access_token=access_token)
    
    return AuthResponse(
        token=token,
        user=token_data
    )

# Registrar usuario
async def register_user(user_data: AuthRegisterData, db: AsyncSession) -> AuthResponse:
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
    user = await user_crud.create(create_data, db)
    
    # Crear y retornar token
    return _create_auth_response(user.id, user.username)

# Obtener usuario por username
async def _get_user_by_username(username: str, db: AsyncSession) -> Optional[User]:
    stmt = select(User).where(User.username == username)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def _authenticate_user(login_data: AuthLoginData, db: AsyncSession) -> User:
    username = login_data.username
    password = login_data.password
    user = await _get_user_by_username(username, db)
    
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

async def login_user(login_data: AuthLoginData, db: AsyncSession) -> AuthResponse:
    user = await _authenticate_user(login_data, db)
    
    # Crear y retornar token
    return _create_auth_response(user.id, user.username)

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
