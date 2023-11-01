from sqlalchemy import CheckConstraint, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import  TYPE_CHECKING, Union

from datetime import datetime

from ..base import ModeloDetalle

if TYPE_CHECKING:
    from .priorities import Priority
    from .projects import Project



class Task(ModeloDetalle):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    finish_at: Mapped[Union[datetime, None]]
    is_complete: Mapped[bool] = mapped_column(default=False)

    priority_id: Mapped[int] = mapped_column(ForeignKey('priority.id'))
    priority: Mapped['Priority'] = relationship(back_populates='tasks')

    project_id: Mapped[int] = mapped_column(ForeignKey('project.id'))
    project: Mapped['Project'] = relationship(back_populates='tasks')
