from sqlalchemy import CheckConstraint, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import get_session

from typing import TYPE_CHECKING, List, Union

from datetime import datetime

from ..base import ModeloDetalle


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

    def update(self, data, session):
        self.name = data.name
        self.description = data.description
        self.level = data.level
        self.color = data.color

        session.commit()
        session.refresh(self)



    @staticmethod
    def create(data, session):
        new_priority = Priority(name=data.name, description=data.description, level=data.level, color=data.color)
        session.add(new_priority)
        session.commit()
        session.refresh(new_priority)



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
