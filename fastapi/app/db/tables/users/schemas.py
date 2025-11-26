from pydantic import BaseModel, Field
from typing import Annotated, Optional

class UserBase(BaseModel):
    username: Annotated[str, Field(..., min_length=3, max_length=30)]
    
    model_config = {
        'from_attributes': True,
    }

class UserCreate(UserBase):
    password: Annotated[str, Field(..., min_length=6, max_length=70)]

class UserRead(UserBase):
    id: Annotated[int, Field(..., gt=0)]

class UserOptional(BaseModel):
    username: Annotated[Optional[str], Field(min_length=3, max_length=30)] = None
    password: Annotated[Optional[str], Field(min_length=6, max_length=70)] = None

class UserInDB(UserRead):
    hashed_password: Annotated[str, Field(..., min_length=6, max_length=255)]

class UserOut(UserRead):
    pass
