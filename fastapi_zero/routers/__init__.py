from fastapi_zero.routers.categories import router as categories_router
from fastapi_zero.routers.tasks import router as tasks_router
from fastapi_zero.routers.users import router as users_router

__all__ = ['users_router', 'tasks_router', 'categories_router']