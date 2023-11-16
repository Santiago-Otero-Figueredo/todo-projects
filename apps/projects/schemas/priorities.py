from typing import Union
from pydantic import BaseModel, EmailStr

class CreatePriorityRequest(BaseModel):
    name: str
    description: Union[str, None]
    level: int
    color: str

