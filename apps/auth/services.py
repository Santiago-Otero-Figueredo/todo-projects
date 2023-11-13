from fastapi.exceptions import HTTPException
from apps.users.models import User

from config.security import verify_password, create_access_token, create_refresh_token, get_token_payload
from config.settings import get_settings

from datetime import timedelta

from .responses import TokenResponse


settings = get_settings()

