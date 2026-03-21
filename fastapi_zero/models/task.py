from sqlalchemy import Boolean, Column, Integer, String

from fastapi_zero.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    concluida = Column(Boolean, default=False)
