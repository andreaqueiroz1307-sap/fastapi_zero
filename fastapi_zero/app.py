from http import HTTPStatus

from fastapi import FastAPI

from fastapi_zero.database import Base, SessionLocal, engine
from fastapi_zero.models.task import Task
from fastapi_zero.schemas import Message

app = FastAPI(title="Disciplina Desenvolvimento WEB")

Base.metadata.create_all(bind=engine)


@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def root():
    return {"message": "API funcionando"}


@app.post("/tarefas")
def criar_tarefa(titulo: str):
    db = SessionLocal()

    try:
        nova_tarefa = Task(titulo=titulo)

        db.add(nova_tarefa)
        db.commit()
        db.refresh(nova_tarefa)

        return nova_tarefa

    finally:
        db.close()


@app.get("/tarefas")
def listar_tarefas():
    db = SessionLocal()

    try:
        tarefas = db.query(Task).all()
        return tarefas

    finally:
        db.close()


@app.get("/tarefas/{task_id}")
def buscar_tarefa(task_id: int):
    db = SessionLocal()

    try:
        tarefa = db.query(Task).filter(Task.id == task_id).first()
        return tarefa

    finally:
        db.close()


@app.put("/tarefas/{task_id}")
def atualizar_tarefa(task_id: int, titulo: str, concluida: bool):
    db = SessionLocal()

    try:
        tarefa = db.query(Task).filter(Task.id == task_id).first()
        if not tarefa:
            return {"erro": "Tarefa não encontrada"}

        tarefa.titulo = titulo
        tarefa.concluida = concluida

        db.commit()
        db.refresh(tarefa)

        return tarefa

    finally:
        db.close()
