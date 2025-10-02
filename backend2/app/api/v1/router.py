"""
Router principal de la API v1
"""
from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth, users, documents, items, loans, reservations, files, statistics
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Autenticación"])
api_router.include_router(users.router, prefix="/users", tags=["Usuarios"])
api_router.include_router(documents.router, prefix="/documents", tags=["Documentos"])
api_router.include_router(items.router, prefix="/items", tags=["Ejemplares"])
api_router.include_router(loans.router, prefix="/loans", tags=["Préstamos"])
api_router.include_router(reservations.router, prefix="/reservations", tags=["Reservas"])
api_router.include_router(files.router, prefix="/files", tags=["Archivos"])
api_router.include_router(statistics.router, prefix="/statistics", tags=["Estadísticas y Reportes"])

