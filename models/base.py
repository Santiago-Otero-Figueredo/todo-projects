from sqlalchemy import String, func, Boolean
from sqlalchemy.orm import Mapped,  mapped_column

from typing import Union
from datetime import datetime

from config.db import Base
# Definición de las tablas

class ModeloBase(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    update_at: Mapped[datetime] = mapped_column(onupdate=func.now())
    is_active: Mapped[bool] = mapped_column(default=True)


class ModeloDetalle(ModeloBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[Union[str, None]]
