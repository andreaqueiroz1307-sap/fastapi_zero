from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from fastapi_zero.auth import hash_senha, verificar_senha
from fastapi_zero.commands.user_commands import (
    AtualizarUserCommand,
    CriarUserCommand,
)
from fastapi_zero.database import get_db
from fastapi_zero.models.user import User
from fastapi_zero.schemas import (
    AlterarSenhaRequest,
    LoginRequest,
    Message,
    RedefinirSenhaSchema,
    UserCreate,
    UserPublic,
)

router = APIRouter(tags=['users'])


def get_user_or_404(user_id: int, db: Session) -> User:
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Usuário não encontrado',
        )

    return user


@router.post('/users', response_model=UserPublic, status_code=HTTPStatus.CREATED)
def criar_user(user: UserCreate, db: Session = Depends(get_db)):
    email_existente = db.query(User).filter(User.email == user.email).first()

    if email_existente:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Já existe um usuário com esse email',
        )

    command = CriarUserCommand(db, user.model_dump())
    novo_user = command.execute()
    return novo_user


@router.post('/login', response_model=UserPublic, status_code=HTTPStatus.OK)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verificar_senha(data.senha, user.senha):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Usuário ou senha inválidos',
        )

    return user


@router.get('/users', response_model=list[UserPublic], status_code=HTTPStatus.OK)
def listar_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.get('/users/{user_id}', response_model=UserPublic)
def buscar_user(user_id: int, db: Session = Depends(get_db)):
    return get_user_or_404(user_id, db)


@router.put('/users/{user_id}', response_model=UserPublic)
def atualizar_user(
    user_id: int,
    user: UserCreate,
    db: Session = Depends(get_db),
):
    db_user = get_user_or_404(user_id, db)

    email_em_uso = (
        db.query(User)
        .filter(User.email == user.email, User.id != user_id)
        .first()
    )

    if email_em_uso:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Já existe um usuário com esse email',
        )

    dados = user.model_dump(exclude_unset=True)

    command = AtualizarUserCommand(db, db_user, dados)
    user_atualizado = command.execute()

    return user_atualizado


@router.delete('/users/{user_id}', response_model=UserPublic)
def deletar_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_or_404(user_id, db)

    db.delete(user)
    db.commit()

    return user


@router.put('/users/{user_id}/alterar-senha', response_model=Message)
def alterar_senha(
    user_id: int,
    dados: AlterarSenhaRequest,
    db: Session = Depends(get_db),
):
    user = get_user_or_404(user_id, db)

    if not verificar_senha(dados.senha_atual, user.senha):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Senha atual incorreta',
        )

    if verificar_senha(dados.nova_senha, user.senha):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='A nova senha deve ser diferente da senha atual',
        )

    user.senha = hash_senha(dados.nova_senha)
    db.commit()
    db.refresh(user)

    return {'message': 'Senha alterada com sucesso'}


@router.put('/users/redefinir-senha', response_model=Message)
def redefinir_senha(
    dados: RedefinirSenhaSchema,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == dados.email).first()

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Usuário não encontrado.',
        )

    if verificar_senha(dados.nova_senha, user.senha):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='A nova senha deve ser diferente da senha atual.',
        )

    user.senha = hash_senha(dados.nova_senha)
    db.commit()
    db.refresh(user)

    return {'message': 'Senha redefinida com sucesso.'}