from fastapi import APIRouter
from fastapi.responses import Response
from app.monitoring.prometheus_metrics import generate_latest, metrics_service
from app.config.database import get_database

router = APIRouter()

@router.get("/metrics")
async def get_metrics():
    """Endpoint para Prometheus metrics"""
    # Actualizar métricas de negocio antes de generar la respuesta
    db = get_database()
    metrics_service.db = db
    await metrics_service.update_business_metrics()
    
    # Generar métricas en formato Prometheus
    metrics_data = generate_latest()
    
    return Response(
        content=metrics_data,
        media_type="text/plain"
    )

@router.get("/health/detailed")
async def detailed_health_check():
    """Health check detallado con métricas del sistema"""
    from datetime import datetime
    import psutil
    import os
    
    # Información del sistema
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    
    health_info = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "biblioteca-backend",
        "system": {
            "memory_usage_mb": round(memory_info.rss / 1024 / 1024, 2),
            "cpu_percent": process.cpu_percent(),
            "threads": process.num_threads()
        },
        "database": {
            "connected": get_database() is not None
        }
    }
    
    return health_info
