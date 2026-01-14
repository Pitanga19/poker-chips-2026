from pydantic import BaseModel, Field
from typing import Annotated

class AuthLoginData(BaseModel):
    username: Annotated[str, Field(..., min_length=3, max_length=30)]
    password: Annotated[str, Field(..., min_length=6, max_length=70)]

class AuthRegisterData(AuthLoginData):
    password_confirm: Annotated[str, Field(..., min_length=6, max_length=70)]

class Token(BaseModel):
    access_token: Annotated[str, Field(...)]
    token_type: Annotated[str, Field(...)] = 'bearer'

class TokenData(BaseModel):
    id: Annotated[int, Field(..., gt=0)]
    username: Annotated[str, Field(..., min_length=3, max_length=30)]

class AuthResponse(BaseModel):
    token: Token
    user: TokenData
