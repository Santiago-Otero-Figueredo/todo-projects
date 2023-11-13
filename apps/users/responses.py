from typing import Union
from datetime import datetime
from pydantic import EmailStr, BaseModel
from apps.core.responses.base import BaseResponse


class UserResponse(BaseResponse):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    created_at: Union[str, None, datetime] = None



class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str = "Bearer"