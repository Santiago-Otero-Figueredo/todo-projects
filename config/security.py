
from passlib.context import CryptContext
from passlib.exc import UnknownHashError

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import joinedload, Session

from datetime import timedelta, datetime

from config.settings import get_settings
from config.database import get_session

from apps.users.models import User, UserToken

import logging
import secrets
import base64
import jwt


SPECIAL_CHARACTERS = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>']

settings = get_settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except UnknownHashError:
        return False

def is_password_strong_enough(password: str) -> bool:
    if len(password) < 8:
        return False

    if not any(char.isupper() for char in password):
        return False

    if not any(char.islower() for char in password):
        return False

    if not any(char.isdigit() for char in password):
        return False

    if not any(char in SPECIAL_CHARACTERS for char in password):
        return False

    return True

async def create_access_token(data, expiry: timedelta):
    pass

async def create_refresh_token(data):
    pass

def get_token_payload(token: str, secret: str, algo: str):
    try:
        payload = jwt.decode(token, secret, algorithms=algo)
    except Exception as jwt_exec:
        logging.debug(f"JWT Error: {str(jwt_exec)}")
        payload = None
    return payload


def get_current_user(token: str = Depends(oauth2_scheme), db=None):
    payload = get_token_payload(token)

    if not payload or type(payload) is not dict:
        return None

    user_id = payload.get('id', None)
    if not user_id:
        return None

    if not db:
        db = next(get_session())

    user = db.query(User).filter(User.id == user_id).first()

    return user


def str_encode(string: str) -> str:
    """
        Encode a string in base85 and convert it to an ASCII string.
    """
    return base64.b85encode(string.encode('ascii')).decode('ascii')


def str_decode(string: str) -> str:
    """
        Decode a base85-encoded string back to an ASCII string.
    """
    return base64.b85decode(string.encode('ascii')).decode('ascii')

def unique_string(byte: int = 8) -> str:
    """
        Generate a unique and secure URL-safe character string.

        Args:
            byte (int, optional): The number of bytes to use for generation. Default value is 8.
    """
    return secrets.token_urlsafe(byte)

def generate_token(payload: dict, secret: str, algo: str, expiry: timedelta):
    """
        Generate a JWT token with the given payload, secret, algorithm, and expiration time.

        Args:
            payload (dict): The content of the token.
            secret (str): The secret key for token signature.
            algo (str): The algorithm for token signature.
            expiry (timedelta): The duration until the token expiration.

        Returns:
            str: The generated JWT token.
    """
    expire = datetime.utcnow() + expiry
    payload.update({"exp": expire})
    return jwt.encode(payload, secret, algorithm=algo)

async def get_token_user(token: str, db):
    payload = get_token_payload(token, settings.JWT_SECRET, settings.JWT_ALGORITHM)
    if payload:
        user_token_id = str_decode(payload.get('r'))
        user_id = str_decode(payload.get('sub'))
        access_key = payload.get('a')
        user_token = db.query(UserToken).options(joinedload(UserToken.user)).filter(UserToken.access_key == access_key,
                                                 UserToken.id == user_token_id,
                                                 UserToken.user_id == user_id,
                                                 UserToken.expires_at > datetime.utcnow(),
                                                 UserToken.is_active == True
                                                 ).first()
        if user_token:
            return user_token.user
    return None


async def load_user(email: str, db):
    from apps.users.models import User
    try:
        user = db.query(User).filter(User.email == email).first()
    except Exception as user_exec:
        logging.info(f"User Not Found, Email: {email}")
        user = None
    return user


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)):
    user = await get_token_user(token=token, db=db)

    if user:
        return user
    raise HTTPException(status_code=401, detail="Not authorized.")