from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.db.tables.users.schemas import UserRead
from app.modules.auth.schemas import AuthRegisterData, AuthLoginData, TokenData, AuthResponse
from app.modules.auth import dependencies as auth_deps
from app.modules.auth import services as auth_services

router = APIRouter(prefix='/auth', tags=['Auth'])

# Registrar usuario
@router.post('/register', response_model=AuthResponse)
async def register_user_endpoint(
    user_data: AuthRegisterData,
    db: AsyncSession = Depends(get_db)
):
    return await auth_services.register_user(user_data, db)

# Iniciar sesión
@router.post('/login', response_model=AuthResponse)
async def login_user_endpoint(
    login_data: AuthLoginData,
    db: AsyncSession = Depends(get_db)
):
    return await auth_services.login_user(login_data, db)

# Obtener usuario actual (/me)
@router.get('/me', response_model=UserRead)
async def get_me_endpoint(
    current_user: TokenData = Depends(auth_deps.get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await auth_services.get_current_user_service(current_user.id, db)

# Cerrar sesión
@router.post('/logout')
async def logout_endpoint(
    authorization: str = Header(..., description='Bearer token'),
):
    """
    Logout del usuario. Actualmente invalida sesión en el cliente.
    """
    token = authorization.replace('Bearer ', '')
    return await auth_services.logout_user_service(token)
