from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from fastapi_zero.commands.user_commands import (
    AtualizarUserCommand,
    CriarUserCommand,
)
from fastapi_zero.database import Base, SessionLocal, engine
from fastapi_zero.models.task import Task
from fastapi_zero.models.user import User
from fastapi_zero.schemas import (
    AlterarSenhaRequest,
    LoginRequest,
    Message,
    TaskCreate,
    TaskPublic,
    TaskSchema,
    TaskUpdate,
    UserCreate,
    UserPublic,
    UserSchema,
)
from fastapi_zero.strategy.prioridade import get_prioridade_strategy

app = FastAPI(title="Disciplina Desenvolvimento WEB")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ----------------------- ROOT ----------------------------
@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def root():
    return {"message": "API funcionando"}


# ----------------------- LOGIN ---------------------------
@app.post("/login", response_model=UserPublic, status_code=HTTPStatus.OK)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user or user.senha != data.senha:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Usuário ou senha inválidos",
        )

    return user


# ------------------- ALTERAR SENHA -----------------------
@app.put(
    "/users/{user_id}/alterar-senha",
    response_model=Message,
    status_code=HTTPStatus.OK,
)
def alterar_senha(
    user_id: int,
    dados: AlterarSenhaRequest,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Usuário não encontrado",
        )

    if user.senha != dados.senha_atual:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Senha atual incorreta",
        )

    if dados.senha_atual == dados.nova_senha:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="A nova senha deve ser diferente da senha atual",
        )

    user.senha = dados.nova_senha
    db.commit()
    db.refresh(user)

    return {"message": "Senha alterada com sucesso"}


# ----------------------- USERS ---------------------------
@app.post("/users", response_model=UserPublic, status_code=HTTPStatus.CREATED)
def criar_user(user: UserCreate, db: Session = Depends(get_db)):
    email_existente = db.query(User).filter(User.email == user.email).first()

    if email_existente:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Já existe um usuário com esse email",
        )

    command = CriarUserCommand(db, user.model_dump())
    novo_user = command.execute()

    return novo_user


@app.get("/users", response_model=list[UserSchema])
def listar_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@app.get("/users/{user_id}", response_model=UserSchema)
def buscar_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Usuário não encontrado",
        )

    return user


@app.put("/users/{user_id}", response_model=UserPublic)
def atualizar_user(
    user_id: int,
    user: UserCreate,
    db: Session = Depends(get_db),
):
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Usuário não encontrado",
        )

    email_em_uso = (
        db
        .query(User)
        .filter(User.email == user.email, User.id != user_id)
        .first()
    )

    if email_em_uso:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Já existe um usuário com esse email",
        )

    dados = user.model_dump(exclude_unset=True)

    command = AtualizarUserCommand(db, db_user, dados)
    db_user = command.execute()

    return db_user


@app.delete(
    "/users/{user_id}",
    status_code=HTTPStatus.OK,
    response_model=UserPublic,
)
def deletar_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Usuário não encontrado",
        )

    db.delete(user)
    db.commit()
    return user


# ----------------------- TASKS ---------------------------
@app.post(
    "/tarefas",
    response_model=TaskPublic,
    status_code=HTTPStatus.CREATED,
)
def criar_tarefa(task: TaskCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == task.user_id).first()

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Usuário não encontrado",
        )

    strategy = get_prioridade_strategy(task.prioridade)
    mensagem_prioridade = strategy.executar()

    nova_tarefa = Task(**task.model_dump())
    db.add(nova_tarefa)
    db.commit()
    db.refresh(nova_tarefa)

    print(mensagem_prioridade)

    return nova_tarefa


@app.get("/tarefas", response_model=list[TaskSchema])
def listar_tarefas(db: Session = Depends(get_db)):
    return db.query(Task).all()


@app.get("/tarefas/{task_id}", response_model=TaskSchema)
def buscar_tarefa(task_id: int, db: Session = Depends(get_db)):
    tarefa = db.query(Task).filter(Task.id == task_id).first()

    if not tarefa:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Tarefa não encontrada",
        )

    return tarefa


@app.put("/tarefas/{task_id}", response_model=TaskSchema)
def atualizar_tarefa(
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db),
):
    tarefa = db.query(Task).filter(Task.id == task_id).first()

    if not tarefa:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Tarefa não encontrada",
        )

    dados = task.model_dump(exclude_unset=True)

    for key, value in dados.items():
        setattr(tarefa, key, value)

    db.commit()
    db.refresh(tarefa)
    return tarefa
