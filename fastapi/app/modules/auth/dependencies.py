from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.modules.auth.schemas import TokenData
from app.modules.auth.security import verify_token

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='/auth/login',
    auto_error=True,
    scopes={}   # No usar scopes por ahora
)

from app.modules.auth.security import verify_token

async def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    try:
        return verify_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token inválido o expirado',
            headers={'WWW-Authenticate': 'Bearer'},
        )
