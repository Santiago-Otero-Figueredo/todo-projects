from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column

from typing import Union
from datetime import datetime

from config.database import Base
# Definición de las tablas

class ModeloBase(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    is_active: Mapped[bool] = mapped_column(default=True)


    @classmethod
    async def get_by_id(cls, id_search: int, session):
        return session.query(cls).filter(cls.id == id_search).first()

    @classmethod
    async def get_all(cls, session):
        return session.query(cls).all()

class ModeloDetalle(ModeloBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[Union[str, None]]
