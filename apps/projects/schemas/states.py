from typing import Union
from pydantic import BaseModel, EmailStr

class CreateStateRequest(BaseModel):
    name: str
    description: Union[str, None]
    color: str

