from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str
    is_active: bool


class UserInDB(User):
    password: str
