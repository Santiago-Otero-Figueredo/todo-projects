from sqlalchemy import CheckConstraint, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.database import get_session

from typing import TYPE_CHECKING, List, Union

from datetime import datetime


from ..base import ModeloDetalle

#if TYPE_CHECKING:
#from .tasks import Task


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

    # @staticmethod
    # def registro(name:str, level: int, color:str):
    #     with get_session() as session:
    #         session.add(Priority(name=name, level=level, color=color))
    #         session.commit()


class Project(ModeloDetalle):
    __tablename__ = "project"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    tasks: Mapped[List['Task']] = relationship(back_populates='project')


class Task(ModeloDetalle):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    finish_at: Mapped[Union[datetime, None]]
    is_complete: Mapped[bool] = mapped_column(default=False)

    priority_id: Mapped[int] = mapped_column(ForeignKey('priority.id'))
    priority: Mapped['Priority'] = relationship(back_populates='tasks')

    project_id: Mapped[int] = mapped_column(ForeignKey('project.id'))
    project: Mapped['Project'] = relationship(back_populates='tasks')