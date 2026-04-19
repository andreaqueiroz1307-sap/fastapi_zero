from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fastapi_zero.database import Base

if TYPE_CHECKING:
    from fastapi_zero.models.task import Task
    from fastapi_zero.models.user import User


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    nome: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'),
        nullable=False,
    )

    usuario: Mapped['User'] = relationship(
        'User',
        back_populates='categorias',
    )

    tarefas: Mapped[list['Task']] = relationship(
        'Task',
        back_populates='categoria',
    )