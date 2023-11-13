from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING, List

from ..base import ModeloDetalle


#if TYPE_CHECKING:
#from .tasks import Task


# class Project(ModeloDetalle):
#     __tablename__ = "project"

#     id: Mapped[int] = mapped_column(primary_key=True, index=True)

#     tasks: Mapped[List[Task]] = relationship(back_populates='project')
