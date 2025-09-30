from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import structlog
import asyncio

from app.config.settings import settings
from app.config.database import connect_to_mongo, close_mongo_connection
from app.routes import auth, users, documents, loans, requests, kafka, metrics
from app.middleware.logging import LoggingMiddleware, setup_structured_logging
from app.services.kafka_manager import kafka_manager
from app.services.kafka_consumer_service import kafka_consumer_service
from app.monitoring.prometheus_metrics import metrics_service

logger = structlog.get_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Configurar logging estructurado
    setup_structured_logging()
    
    # Startup
    await connect_to_mongo()
    
    # Configurar servicio de métricas
    metrics_service.db = get_database()
    
    # Crear topics de Kafka
    await kafka_manager.create_topics()
    
    # Iniciar consumers de Kafka
    await kafka_consumer_service.start_consumers()
    
    # Iniciar actualización periódica de métricas
    asyncio.create_task(update_metrics_periodically())
    
    logger.info("Application started successfully")
    
    yield
    
    # Shutdown
    await kafka_consumer_service.stop_consumers()
    kafka_manager.close()
    await close_mongo_connection()
    
    logger.info("Application shutdown")

async def update_metrics_periodically():
    """Actualiza las métricas cada 30 segundos"""
    while True:
        try:
            if metrics_service.db:
                await metrics_service.update_business_metrics()
        except Exception as e:
            logger.error("Error actualizando métricas periódicas", error=str(e))
        
        await asyncio.sleep(30)  # Actualizar cada 30 segundos

app = FastAPI(
    title="Sistema de Biblioteca Municipal",
    description="Backend para el sistema de préstamos de la Biblioteca Municipal",
    version="1.0.0",
    lifespan=lifespan
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LoggingMiddleware)

# Routes
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(documents.router, prefix="/api/v1/documents", tags=["Documents"])
app.include_router(loans.router, prefix="/api/v1/loans", tags=["Loans"])
app.include_router(requests.router, prefix="/api/v1/requests", tags=["Requests"])
app.include_router(kafka.router, prefix="/api/v1/kafka", tags=["Kafka"])
app.include_router(metrics.router, prefix="/api/v1", tags=["Metrics"])

@app.get("/")
async def root():
    return {"message": "Sistema de Biblioteca Municipal API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    kafka_status = "healthy" if kafka_manager.admin_client else "unhealthy"
    db_status = "healthy" if get_database() else "unhealthy"
    
    return {
        "status": "healthy", 
        "service": "biblioteca-backend",
        "kafka": kafka_status,
        "database": db_status
    }
