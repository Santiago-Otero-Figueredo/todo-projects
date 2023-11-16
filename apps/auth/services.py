from fastapi.exceptions import HTTPException
from apps.users.models import User

from core.config import get_settings

from datetime import timedelta

from .responses import TokenResponse


settings = get_settings()

