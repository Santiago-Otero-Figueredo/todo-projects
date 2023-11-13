from fastapi.exceptions import HTTPException

from sqlalchemy import CheckConstraint, String, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship, joinedload

from config.database import Base
from config.settings import get_settings


from datetime import datetime
from typing import List

from ..base import ModeloBase

from datetime import datetime, timedelta
import logging

settings = get_settings()

class User(ModeloBase):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    is_verified: Mapped[bool] = mapped_column(default=False)

    tokens: Mapped[List['UserToken']] = relationship(back_populates='user')


    def get_context_string(self, context: str):
        return f"{context}{self.password[-6:]}{self.updated_at.strftime('%m%d%Y%H%M%S')}".strip()



    @staticmethod
    async def create_account(data, session):
        from config.security import hash_password, is_password_strong_enough
        from apps.mails.services import send_account_verification_email

        if await User.get_user(data.email, session):
            raise HTTPException(status_code=422, detail='Email is already registered with us.')

        if not is_password_strong_enough(data.password):
            raise HTTPException(status_code=400, detail='Please provide a strong password.')

        new_user = User(
            username=data.email,
            email=data.email,
            password=hash_password(data.password)
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        # Account Verification Email
        await send_account_verification_email(user=new_user)


        return new_user


    @staticmethod
    async def active_user_account(email, token, session):
        from config.security import verify_password
        from apps.mails.services import send_account_activation_confirmation_email

        user = await User.get_user(email, session)

        if not user:
            raise HTTPException(status_code=422, detail='This link is not valid.')

        user_token = user.get_context_string(context=settings.USER_VERIFY_ACCOUNT)
        try:
            token_valid = verify_password(user_token, token)
        except Exception as verify_exec:
            logging.exception(verify_exec)
            token_valid = False

        if not token_valid:
            raise HTTPException(status_code=422, detail='This link either expired or not valid.')

        user.is_verified = True

        session.add(user)
        session.commit()
        session.refresh(user)

        # Activation confirmation email
        await send_account_activation_confirmation_email(user)

        return user

    @staticmethod
    async def email_forgot_password_link(data, session):
        from apps.mails.services import send_password_reset_email

        user = await User.get_user(data.email, session)
        if not user.is_verified:
            raise HTTPException(status_code=400, detail="Your account is not verified. Please check your email inbox to verify your account.")

        if not user.is_active:
            raise HTTPException(status_code=400, detail="Your account has been dactivated. Please contact support.")

        await send_password_reset_email(user)


    @staticmethod
    async def reset_user_password(data, session):
        from config.security import verify_password, hash_password

        user = await User.get_user(data.email, session)

        if not user:
            raise HTTPException(status_code=400, detail="Invalid request")


        if not user.is_verified:
            raise HTTPException(status_code=400, detail="Invalid request")

        if not user.is_active:
            raise HTTPException(status_code=400, detail="Invalid request")

        user_token = user.get_context_string(context=settings.FORGOT_PASSWORD)
        try:
            token_valid = verify_password(user_token, data.token)
        except Exception as verify_exec:
            logging.exception(verify_exec)
            token_valid = False
        if not token_valid:
            raise HTTPException(status_code=400, detail="Invalid window.")

        user.password = hash_password(data.password)
        user.updated_at = datetime.now()
        session.add(user)
        session.commit()
        session.refresh(user)
        # Notify user that password has been updated

    @staticmethod
    async def get_login_token(data, session):
        # verify the email and password
        # Verify that user account is verified
        # Verify user account is active
        # generate access_token and refresh_token and ttl
        from config.security import verify_password, load_user


        user = await load_user(data.username, session)
        if not user:
            raise HTTPException(status_code=400, detail="Email is not registered with us.")

        if not verify_password(data.password, user.password):
            raise HTTPException(status_code=400, detail="Incorrect email or password.")

        if not user.is_verified:
            raise HTTPException(status_code=400, detail="Your account is not verified. Please check your email inbox to verify your account.")

        if not user.is_active:
            raise HTTPException(status_code=400, detail="Your account has been deactivated. Please contact support.")

        # Generate the JWT Token
        return _generate_tokens(user, session)


    @staticmethod
    async def get_refresh_token(refresh_token, session):
        from config.security import get_token_payload, str_decode

        token_payload = get_token_payload(refresh_token, settings.SECRET_KEY, settings.JWT_ALGORITHM)
        if not token_payload:
            raise HTTPException(status_code=400, detail="Invalid Request.")

        refresh_key = token_payload.get('t')
        access_key = token_payload.get('a')
        user_id = str_decode(token_payload.get('sub'))

        user_tokens = session.query(UserToken).options(joinedload(UserToken.user)).filter(UserToken.refresh_key == refresh_key,
                                                    UserToken.access_key == access_key,
                                                    UserToken.user_id == user_id,
                                                    UserToken.is_active == True,
                                                    UserToken.expires_at > datetime.utcnow()
                                                    ).all()

        if not user_tokens or len(user_tokens) == 0:
            raise HTTPException(status_code=400, detail="Invalid Request.")

        for old_user_token in user_tokens:
            old_user_token.is_active = False
            session.add(old_user_token)

        user_tokens[-1].expires_at = datetime.utcnow()
        session.add(user_tokens[-1])
        session.commit()

        return _generate_tokens(user_tokens[-1].user, session)


    @staticmethod
    async def get_user(email: str, session):
        return session.query(User).filter(User.email == email).first()



class UserToken(ModeloBase):
    __tablename__ = "user_tokens"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    access_key: Mapped[str] = mapped_column(nullable=True, index=True, default=None)
    refresh_key: Mapped[str] = mapped_column(nullable=True, index=True, default=None)
    created_at:Mapped[datetime] = mapped_column(nullable=False, server_default=func.now())
    expires_at:Mapped[datetime] = mapped_column(nullable=False)

    user: Mapped['User'] = relationship(back_populates="tokens")
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))



def _generate_tokens(user, session):
    from config.security import str_encode, unique_string, generate_token



    refresh_key = unique_string(100)
    access_key = unique_string(50)
    rt_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    user_token = UserToken()
    user_token.user_id = user.id
    user_token.refresh_key = refresh_key
    user_token.access_key = access_key
    user_token.expires_at = datetime.utcnow() + rt_expires
    session.add(user_token)
    session.commit()
    session.refresh(user_token)

    at_payload = {
        "sub": str_encode(str(user.id)),
        'a': access_key,
        'r': str_encode(str(user_token.id)),
        'n': str_encode(f"{user.username}")
    }

    at_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = generate_token(at_payload, settings.JWT_SECRET, settings.JWT_ALGORITHM, at_expires)

    rt_payload = {"sub": str_encode(str(user.id)), "t": refresh_key, 'a': access_key}
    refresh_token = generate_token(rt_payload, settings.SECRET_KEY, settings.JWT_ALGORITHM, rt_expires)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_in": at_expires.seconds
    }