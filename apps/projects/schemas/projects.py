from pydantic import BaseModel, EmailStr

from typing import Union


class CreateProjectRequest(BaseModel):
    name: str
    description: Union[str, None]
