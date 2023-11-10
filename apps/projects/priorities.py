from sqlalchemy import CheckConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import get_db

from typing import TYPE_CHECKING, List

from ..base import ModeloDetalle

if TYPE_CHECKING:
    from .tasks import Task


class Priority(ModeloDetalle):
    __tablename__ = "priority"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    level: Mapped[int]
    color: Mapped[str] = mapped_column(String(7))

    tasks: Mapped[List['Task']] = relationship(back_populates='priority')

    __table_args__ = (
        CheckConstraint("level IN (1, 2, 3)", name="check_level_in_values"),
        CheckConstraint("color ~ '^(#[0-9A-Fa-f]{6})$'", name="check_color_hex_format"),
    )

    @staticmethod
    def registro(name:str, level: int, color:str):
        with get_db() as session:
            session.add(Priority(name=name, level=level, color=color))
            session.commit()
