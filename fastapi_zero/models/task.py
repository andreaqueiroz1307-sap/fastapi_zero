from datetime import UTC, date, datetime
from typing import Optional

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fastapi_zero.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    titulo: Mapped[str] = mapped_column(String, nullable=False)
    descricao: Mapped[str] = mapped_column(String, nullable=False)
    prioridade: Mapped[str] = mapped_column(String, nullable=False)

    concluida: Mapped[bool] = mapped_column(Boolean, default=False)

    criada_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )

    data_limite: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )

    usuario: Mapped["User"] = relationship("User", back_populates="tarefas")
