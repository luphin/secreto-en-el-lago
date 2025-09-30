from .auth import router as auth_router
from .users import router as users_router
from .documents import router as documents_router
from .loans import router as loans_router
from .requests import router as requests_router
from .kafka import router as kafka_router
from .metrics import router as metrics_router

__all__ = [
    "auth_router",
    "users_router",
    "documents_router",
    "loans_router",
    "requests_router",
    "kafka_router",
    "metrics_router"
]
