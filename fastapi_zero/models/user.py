from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fastapi_zero.database import Base

if TYPE_CHECKING:
    from fastapi_zero.models.task import Task


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    nome: Mapped[str] = mapped_column(String, nullable=False)

    email: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
    )

    senha: Mapped[str] = mapped_column(String, nullable=False)

    tarefas: Mapped[list["Task"]] = relationship(
        "Task",
        back_populates="usuario",
        cascade="all, delete-orphan",
    )
