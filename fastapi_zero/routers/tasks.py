from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from fastapi_zero.models.category import Category
from fastapi_zero.models.task import Task
from fastapi_zero.models.user import User
from fastapi_zero.schemas import Message, TaskCreate, TaskPublic, TaskUpdate
from fastapi_zero.services.notification_service import montar_mensagem_lembrete
from fastapi_zero.strategy.prioridade import get_prioridade_strategy

router = APIRouter(prefix='/tarefas', tags=['tarefas'])


def get_db():
    from fastapi_zero.database import SessionLocal

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post('', response_model=TaskPublic, status_code=HTTPStatus.CREATED)
def criar_tarefa(task: TaskCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == task.user_id).first()

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Usuário não encontrado',
        )

    categoria_id_final = task.categoria_id

    if categoria_id_final is None:
        categoria_todas = (
            db.query(Category)
            .filter(
                Category.user_id == task.user_id,
                Category.nome == 'TODAS',
            )
            .first()
        )

        if not categoria_todas:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Categoria padrão TODAS não encontrada',
            )

        categoria_id_final = categoria_todas.id

    else:
        categoria = (
            db.query(Category)
            .filter(
                Category.id == categoria_id_final,
                Category.user_id == task.user_id,
            )
            .first()
        )

        if not categoria:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Categoria não encontrada para esse usuário',
            )

    strategy = get_prioridade_strategy(task.prioridade.value)
    mensagem_prioridade = strategy.executar()

    nova_tarefa = Task(
        titulo=task.titulo,
        descricao=task.descricao,
        prioridade=task.prioridade.value,
        concluida=task.concluida,
        data_limite=task.data_limite,
        frequencia_lembrete=(
            task.frequencia_lembrete.value
            if task.frequencia_lembrete is not None
            else None
        ),
        user_id=task.user_id,
        categoria_id=categoria_id_final,
    )

    db.add(nova_tarefa)
    db.commit()
    db.refresh(nova_tarefa)

    mensagem_lembrete = montar_mensagem_lembrete(nova_tarefa)

    print(mensagem_prioridade)
    print(mensagem_lembrete)

    return nova_tarefa


@router.get('', response_model=list[TaskPublic], status_code=HTTPStatus.OK)
def listar_tarefas(db: Session = Depends(get_db)):
    return db.query(Task).all()


@router.get(
    '/user/{user_id}',
    response_model=list[TaskPublic],
    status_code=HTTPStatus.OK,
)
def listar_tarefas_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Usuário não encontrado',
        )

    return db.query(Task).filter(Task.user_id == user_id).all()


@router.get('/{task_id}', response_model=TaskPublic, status_code=HTTPStatus.OK)
def buscar_tarefa(task_id: int, db: Session = Depends(get_db)):
    tarefa = db.query(Task).filter(Task.id == task_id).first()

    if not tarefa:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Tarefa não encontrada',
        )

    return tarefa


@router.put('/{task_id}', response_model=TaskPublic, status_code=HTTPStatus.OK)
def atualizar_tarefa(
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db),
):
    tarefa = db.query(Task).filter(Task.id == task_id).first()

    if not tarefa:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Tarefa não encontrada',
        )

    dados = task.model_dump(exclude_unset=True)

    if task.prioridade is not None:
        strategy = get_prioridade_strategy(task.prioridade.value)
        mensagem_prioridade = strategy.executar()
        print(mensagem_prioridade)
        dados['prioridade'] = task.prioridade.value

    if task.frequencia_lembrete is not None:
        dados['frequencia_lembrete'] = task.frequencia_lembrete.value

    if 'categoria_id' in dados and dados['categoria_id'] is not None:
        categoria = (
            db.query(Category)
            .filter(
                Category.id == dados['categoria_id'],
                Category.user_id == tarefa.user_id,
            )
            .first()
        )

        if not categoria:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Categoria não encontrada para esse usuário',
            )

    for key, value in dados.items():
        setattr(tarefa, key, value)

    db.commit()
    db.refresh(tarefa)

    print(montar_mensagem_lembrete(tarefa))

    return tarefa


@router.delete(
    '/{task_id}',
    response_model=Message,
    status_code=HTTPStatus.OK,
)
def deletar_tarefa(task_id: int, db: Session = Depends(get_db)):
    tarefa = db.query(Task).filter(Task.id == task_id).first()

    if not tarefa:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Tarefa não encontrada',
        )

    db.delete(tarefa)
    db.commit()

    return {'message': 'Tarefa deletada com sucesso'}