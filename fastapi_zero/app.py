from http import HTTPStatus

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi_zero.database import Base, engine
from fastapi_zero.models import Category, Task, User
from fastapi_zero.routers.categories import router as categories_router
from fastapi_zero.routers.tasks import router as tasks_router
from fastapi_zero.routers.users import router as users_router
from fastapi_zero.schemas import Message

app = FastAPI(title='Disciplina Desenvolvimento WEB')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

Base.metadata.create_all(bind=engine)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def root():
    return {'message': 'API funcionando'}


app.include_router(users_router)
app.include_router(tasks_router)
app.include_router(categories_router)