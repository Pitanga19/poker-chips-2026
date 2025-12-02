from pydantic import BaseModel, Field
from typing import Annotated

class PotPlayerBase(BaseModel):
    pot_id: Annotated[int, Field(..., gt=0)]
    player_id: Annotated[int, Field(..., gt=0)]
    
    model_config = {
        'from_attributes': True,
    }

class PotPlayerCreate(PotPlayerBase):
    pass

class PotPlayerRead(PotPlayerBase):
    id: Annotated[int, Field(gt=0)]
