from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from fastapi_zero.database import get_db
from fastapi_zero.models.category import Category
from fastapi_zero.models.user import User
from fastapi_zero.schemas import CategoryCreate, CategoryPublic, Message

router = APIRouter(tags=['categories'])


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
            Category.user_id == category.user_id,
            Category.nome == category.nome,
        )
        .first()
    )

    if categoria_existente:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Já existe uma categoria com esse nome para esse usuário',
        )

    nova_categoria = Category(**category.model_dump())
    db.add(nova_categoria)
    db.commit()
    db.refresh(nova_categoria)

    return nova_categoria