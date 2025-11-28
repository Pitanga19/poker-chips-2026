from datetime import datetime, timedelta
from jose import jwt, JWTError, ExpiredSignatureError
from passlib.context import CryptContext
from app.core.config import settings
from app.core.exceptions import InvalidTokenException
from app.modules.auth.schemas import TokenData

# Configuración de Passlib
pwd_context = CryptContext(
    schemes=['argon2'],
    deprecated='auto',
    argon2__memory_cost=102400,
    argon2__parallelism=8,
    argon2__time_cost=3
)

# Función para hashear contraseñas
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Función para verificar contraseñas
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Función para crear JWT
def create_access_token(
    data: dict,
    expires_delta: timedelta = timedelta(minutes=settings.JWT_EXPIRATION_MINUTES)
) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta

    to_encode.update({
        'exp': expire,
        'iat': datetime.utcnow(),
        'sub': str(data['id'])
    })

    return jwt.encode(
        to_encode,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )

# Función para verificar JWT
def verify_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
    except ExpiredSignatureError:
        raise InvalidTokenException('Token expirado')
    except JWTError:
        raise InvalidTokenException('Token inválido')

    data = {
        'id': payload.get('id'),
        'username': payload.get('username')
    }

    if not data['id'] or not data['username']:
        raise InvalidTokenException('Token inválido')

    return TokenData(**data)
