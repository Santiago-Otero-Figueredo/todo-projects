
from passlib.context import CryptContext
from passlib.exc import UnknownHashError

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from starlette.authentication import AuthCredentials, UnauthenticatedUser

from datetime import timedelta, datetime


from core.config import get_settings
from core.database import get_session


from apps.users.models import User

settings = get_settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')

def get_hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except UnknownHashError:
        return False

