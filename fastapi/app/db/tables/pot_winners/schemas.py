from pydantic import BaseModel, Field
from typing import Annotated

class PotWinnerBase(BaseModel):
    pot_id: Annotated[int, Field(..., gt=0)]
    winner_id: Annotated[int, Field(..., gt=0)]
    amount_won: Annotated[int, Field(ge=0)] = 0
    
    model_config = {
        'from_attributes': True,
    }

class PotWinnerCreate(PotWinnerBase):
    pass

class PotWinnerOptional(BaseModel):
    pot_id: Annotated[int, Field(gt=0)] = None
    winner_id: Annotated[int, Field(gt=0)] = None
    amount_won: Annotated[int, Field(ge=0)] = None

class PotWinnerRead(PotWinnerBase):
    id: Annotated[int, Field(gt=0)]
