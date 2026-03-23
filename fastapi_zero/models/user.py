from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from fastapi_zero.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    senha = Column(String, nullable=False)
    tarefas = relationship("Task", back_populates="usuario")