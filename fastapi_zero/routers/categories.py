from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from fastapi_zero.database import get_db
from fastapi_zero.models.category import Category
from fastapi_zero.models.task import Task
from fastapi_zero.models.user import User
from fastapi_zero.schemas import CategoryCreate, CategoryPublic, Message

router = APIRouter(tags=['categories'])


def get_category_or_404(category_id: int, db: Session) -> Category:
    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Categoria não encontrada',
        )

    return category


@router.post(
    '/categories',
    response_model=CategoryPublic,
    status_code=HTTPStatus.CREATED,
)
def criar_categoria(
    category: CategoryCreate,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == category.user_id).first()

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Usuário não encontrado',
        )

    categoria_existente = (
        db.query(Category)
        .filter(
            Category.nome == category.nome,
            Category.user_id == category.user_id,
        )
        .first()
    )

    if categoria_existente:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Essa categoria já existe para esse usuário',
        )

    nova_categoria = Category(**category.model_dump())
    db.add(nova_categoria)
    db.commit()
    db.refresh(nova_categoria)

    return