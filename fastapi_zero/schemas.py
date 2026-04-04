from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class Message(BaseModel):
    message: str


class UserBase(BaseModel):
    nome: str
    email: EmailStr


class UserCreate(UserBase):
    senha: str


class LoginRequest(BaseModel):
    email: EmailStr
    senha: str


class AlterarSenhaRequest(BaseModel):
    senha_atual: str
    nova_senha: str


class UserPublic(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class UserSchema(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class TaskCreate(BaseModel):
    titulo: str
    descricao: str
    prioridade: str
    data_limite: date | None = None
    user_id: int


class TaskUpdate(BaseModel):
    titulo: str | None = None
    descricao: str | None = None
    prioridade: str | None = None
    concluida: bool | None = None
    data_limite: date | None = None


class TaskPublic(BaseModel):
    id: int
    titulo: str
    descricao: str
    prioridade: str
    concluida: bool
    criada_em: datetime
    data_limite: date | None = None
    usuario: UserPublic
    model_config = ConfigDict(from_attributes=True)


class TaskSchema(TaskPublic):
    pass