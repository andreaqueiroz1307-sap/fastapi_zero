from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


# TASK
class TaskBase(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    prioridade: str


class TaskCreate(TaskBase):
    user_id: int


class TaskUpdate(TaskBase):
    concluida: Optional[bool] = None


class UserSimple(BaseModel):
    id: int
    nome: str

    class Config:
        from_attributes = True


class TaskSchema(TaskBase):
    id: int
    concluida: bool
    criada_em: datetime
    usuario: Optional[UserSimple] = None

    class Config:
        from_attributes = True

class TaskPublic(TaskBase):
    concluida: bool


# USER

class UserPublic(BaseModel):
    nome: str
    email: EmailStr


class UserCreate(UserPublic):
    senha: str


class UserSchema(UserSimple):
    #lista de tarefas: nome, descrição, prioridade e concluída
    tarefas: List[TaskUpdate] = []

    class Config:
        from_attributes = True


