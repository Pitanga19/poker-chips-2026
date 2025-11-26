from passlib.context import CryptContext
from datetime import datetime, timedelta
import pytz
from jose import JWTError, jwt
from app.core.config import settings
from app.core.exceptions import InvalidTokenException
from pydantic import BaseModel, Field
from typing import Annotated

# Modelo de token
class Token(BaseModel):
    access_token: str
    token_type: str = Field(default='bearer')

# Modelo de datos del token
class TokenData(BaseModel):
    id: Annotated[int, Field(...)]
    username: Annotated[str, Field(...)]

# Contexto para hash de contraseñas
pwd_context = CryptContext(schemes=['argon2'], deprecated='auto')

# Función para hashear contraseña
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Función para verificar contraseña
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Función para crear JWT
def create_access_token(
    data: dict,
    expires_delta: timedelta = timedelta(minutes=settings.JWT_EXPIRATION_MINUTES)
) -> str:
    to_encode = data.copy()
    tz = pytz.timezone(settings.JWT_TIMEZONE)
    expire = datetime.now(tz) + expires_delta
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )
    return encoded_jwt

# Función para verificar el JWT
def verify_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return TokenData(**payload)
    except JWTError:
        raise InvalidTokenException('Token inválido o expirado')
