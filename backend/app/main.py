"""
Aplicación principal FastAPI para el Sistema de Préstamo BEC
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.core.config import settings
from app.core.database import connect_to_mongo, close_mongo_connection
from app.core.kafka_producer import kafka_producer
from app.core.storage import storage_manager
from app.api.v1.router import api_router

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Maneja el ciclo de vida de la aplicación"""
    # Startup
    logger.info("🚀 Iniciando Sistema de Préstamo BEC...")
    
    await connect_to_mongo()
    await kafka_producer.start()
    storage_manager.initialize()
    
    logger.info("✨ Sistema iniciado correctamente")
    
    yield
    
    # Shutdown
    logger.info("🛑 Deteniendo sistema...")
    
    await close_mongo_connection()
    await kafka_producer.stop()
    
    logger.info("👋 Sistema detenido correctamente")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API Backend para el Sistema de Préstamo de la Biblioteca de Estación Central",
    lifespan=lifespan
)

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/", tags=["Health"])
async def root():
    """Endpoint de verificación de salud"""
    return {
        "message": "Sistema de Préstamo BEC - API Running",
        "version": settings.VERSION,
        "status": "healthy"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Endpoint de health check"""
    return {"status": "ok"}
