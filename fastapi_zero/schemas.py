from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class Message(BaseModel):
    message: str


class PrioridadeEnum(str, Enum):
    alta = 'alta'
    media = 'media'
    baixa = 'baixa'


class FrequenciaLembreteEnum(str, Enum):
    min_30 = '30min'
    hora_1 = '1h'
    hora_2 = '2h'
    dia_1 = '1x_dia'
    dia_2 = '2x_dia'
    dia_3 = '3x_dia'
    no_dia_limite = 'no_dia_limite'


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


class RedefinirSenhaSchema(BaseModel):
    email: EmailStr
    nova_senha: str


class UserPublic(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class CategoryBase(BaseModel):
    nome: str


class CategoryCreate(CategoryBase):
    user_id: int


class CategoryPublic(CategoryBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class TaskCreate(BaseModel):
    titulo: str
    descricao: str
    prioridade: PrioridadeEnum
    concluida: bool = False
    data_limite: date | None = None
    frequencia_lembrete: FrequenciaLembreteEnum | None = None
    user_id: int
    categoria_id: int | None = None


class TaskUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    prioridade: PrioridadeEnum | None = None
    concluida: Optional[bool] = None
    data_limite: date | None = None
    frequencia_lembrete: FrequenciaLembreteEnum | None = None
    categoria_id: Optional[int] = None


class TaskPublic(BaseModel):
    id: int
    titulo: str
    descricao: str
    prioridade: PrioridadeEnum
    concluida: bool
    criada_em: datetime
    data_limite: date | None = None
    frequencia_lembrete: FrequenciaLembreteEnum | None = None
    user_id: int
    categoria_id: int | None = None
    usuario: UserPublic
    categoria: CategoryPublic | None = None

    model_config = ConfigDict(from_attributes=True)