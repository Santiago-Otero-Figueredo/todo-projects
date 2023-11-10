from fastapi.exceptions import HTTPException

from sqlalchemy import CheckConstraint, String
from sqlalchemy.orm import Mapped, mapped_column


from ..base import ModeloBase



class User(ModeloBase):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    is_verified: Mapped[bool] = mapped_column(default=False)




    @staticmethod
    async def register_account(data, db):
        from core.security import get_hash_password

        if await User.get_user(data.email, db):
            raise HTTPException(status_code=422, detail='Email is already registered with us')

        new_user = User(
            username=data.username,
            email=data.email,
            password=get_hash_password(data.password)
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

    @staticmethod
    async def get_user(email: str, db):
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def authenticate(username:str, password:str):
        pass