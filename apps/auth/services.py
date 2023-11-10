from fastapi.exceptions import HTTPException
from apps.users.models import User

from core.security import verify_password, create_access_token, create_refresh_token, get_token_payload
from core.config import get_settings

from datetime import timedelta

from .responses import TokenResponse


settings = get_settings()


async def get_token(data, db):
    user = db.query(User).filter(User.email == data.username).first()

    if not user:
        raise HTTPException(
            status_code=400,
            detail='Email is not registered with us',
            headers={'WWW-Authenticate': 'Bearer'}
        )

    if not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=400,
            detail='Invalid login credentials.',
            headers={'WWW-Authenticate': 'Bearer'}
        )

    _verify_user_access(user=user)

    return await _get_user_token(user=user)


async def get_refresh_token(token, db):
    payload = get_token_payload(token=token)
    user_id = payload.get('id', None)

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail='Invalid refresh token.',
            headers={'WWW-Authenticate': 'Bearer'}
        )

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail='Invalid refresh token.',
            headers={'WWW-Authenticate': 'Bearer'}
        )

    return await _get_user_token(user=user, refresh_token=token)


def _verify_user_access(user: User):

    if not user.is_active:
        raise HTTPException(
            status_code=400,
            detail='Your account is inactive. Please contact support.',
            headers={'WWW-Authenticate': 'Bearer'}
        )

    if not user.is_verified:
        #   Trigger user acount verification email
        raise HTTPException(
            status_code=400,
            detail='Your account is unverified',
            headers={'WWW-Authenticate': 'Bearer'}
        )


async def _get_user_token(user: User, refresh_token = None):
    payload = {'id': user.id}

    access_token_expiry = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = await create_access_token(payload, access_token_expiry)
    if not refresh_token:
        refresh_token = await create_refresh_token(payload)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=access_token_expiry.seconds # in seconds
    )

