from pydantic import BaseModel

class DeleteResponse(BaseModel):
    msg: str
