from pydantic import BaseModel, EmailStr

from typing import Union


class CreateTaskRequest(BaseModel):
    name: str
    description: Union[str, None]
