from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from fastapi_zero.database import Base, SessionLocal, engine
from fastapi_zero.models.task import Task
from fastapi_zero.models.user import User
from fastapi_zero.schemas import (
    Message,
    TaskCreate,
    TaskSchema,
    TaskUpdate,
    TaskPublic,
    UserCreate,
    UserSchema,
    UserPublic
)

app = FastAPI(title="Disciplina Desenvolvimento WEB")


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#------------------------------------ROOT-----------------------------------------------
@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def root():
    return {"message": "API funcionando"}


#------------------------------USERS--------------------------------------------
@app.post("/users", response_model=UserPublic, status_code=HTTPStatus.CREATED)
def criar_user(user: UserCreate, db: Session = Depends(get_db)):
    novo_user = User(**user.model_dump()) #recebe os campos do UserCreate
    db.add(novo_user)
    db.commit()
    db.refresh(novo_user)
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

    if not db_user: #caso não ache o user, levanta exceção
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Usuário não encontrado",
        )

    dados = user.model_dump(exclude_unset=True)

    for key, value in dados.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)

    return db_user

@app.delete("/users/{user_id}",
            status_code=HTTPStatus.OK,
            response_model=UserPublic)
def deletar_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Usuário não encontrado"
        )

    db.delete(user)
    db.commit()
    return user




#-------------------------------------TASKS--------------------------------------
@app.post("/tarefas", response_model=TaskPublic, status_code=HTTPStatus.CREATED)
def criar_tarefa(task: TaskCreate, db: Session = Depends(get_db)):
    nova_tarefa = Task(**task.model_dump())
    db.add(nova_tarefa)
    db.commit()
    db.refresh(nova_tarefa)
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

