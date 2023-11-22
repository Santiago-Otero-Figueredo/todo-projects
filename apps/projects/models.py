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

    @classmethod
    async def get_all(cls, session):
        return session.query(cls).order_by(cls.level).all()

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


    def update(self, data, session):
        self.name = data.name
        self.description = data.description

        session.commit()
        session.refresh(self)

    @classmethod
    async def get_all(cls, session):
        return session.query(cls).order_by(cls.name).all()

    @staticmethod
    def create(data, session):
        new_project = Project(name=data.name, description=data.description)
        session.add(new_project)
        session.commit()
        session.refresh(new_project)


class Task(ModeloDetalle):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    finish_at: Mapped[Union[datetime, None]]
    is_complete: Mapped[bool] = mapped_column(default=False)

    priority_id: Mapped[int] = mapped_column(ForeignKey('priority.id'))
    priority: Mapped['Priority'] = relationship(back_populates='tasks')

    project_id: Mapped[int] = mapped_column(ForeignKey('project.id'))
    project: Mapped['Project'] = relationship(back_populates='tasks')

    state_id: Mapped[int] = mapped_column(ForeignKey('state.id'), nullable=True)
    state: Mapped['State'] = relationship(back_populates='tasks')

    @property
    def finish_at_formatted(self):
        return self.finish_at.strftime('%Y-%m-%d %H:%M')

    def update(self, data, session):
        self.name = data.name
        self.description = data.description
        self.project_id = data.project
        self.priority_id = data.priority

        session.commit()
        session.refresh(self)

    def complete(self, data, session):
        self.state_id = data.state
        if data.state == 1:
            self.finish_at = datetime.now()

        session.commit()
        session.refresh(self)

    @classmethod
    def get_all(cls, session):
        return session.query(cls).order_by(cls.update_at.desc()).all()

    @staticmethod
    async def create(data, session):
        state = await State.get_by_name('Not initialized', session)
        new_task = Task(name=data.name, description=data.description, project_id = data.project, priority_id = data.priority, state_id=state.id)
        session.add(new_task)
        session.commit()
        session.refresh(new_task)


class State(ModeloDetalle):
    __tablename__ = "state"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    color: Mapped[str] = mapped_column(String(7))

    tasks: Mapped[List['Task']] = relationship(back_populates='state')

    __table_args__ = (
        CheckConstraint("color ~ '^(#[0-9A-Fa-f]{6})$'", name="check_color_hex_format"),
    )

    def update(self, data, session):
        self.name = data.name
        self.description = data.description
        self.color = data.color

        session.commit()
        session.refresh(self)

    @classmethod
    async def get_all(cls, session):
        return session.query(cls).order_by(cls.name).all()

    @staticmethod
    def create(data, session):
        new_state = State(name=data.name, description=data.description, color=data.color)
        session.add(new_state)
        session.commit()
        session.refresh(new_state)