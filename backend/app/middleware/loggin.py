import time
import structlog
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.monitoring.prometheus_metrics import metrics_service

logger = structlog.get_logger()

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Registrar inicio de la solicitud
        start_time = time.time()
        
        # Extraer información de la solicitud
        method = request.method
        url = str(request.url)
        client_ip = request.client.host if request.client else "unknown"
        
        # Excluir endpoints de health check y métricas del logging detallado
        exclude_paths = ['/health', '/metrics', '/docs', '/redoc']
        should_log = not any(url.endswith(path) for path in exclude_paths)
        
        if should_log:
            logger.info(
                "Solicitud iniciada",
                method=method,
                url=url,
                client_ip=client_ip
            )
        
        # Procesar la solicitud
        try:
            response = await call_next(request)
        except Exception as e:
            # Registrar error
            logger.error(
                "Error procesando solicitud",
                method=method,
                url=url,
                error=str(e),
                exc_info=True
            )
            raise
        
        # Calcular duración
        process_time = time.time() - start_time
        
        # Registrar métricas
        endpoint = request.url.path
        status_code = response.status_code
        metrics_service.record_request(method, endpoint, status_code, process_time)
        
        if should_log:
            # Registrar fin de la solicitud
            logger.info(
                "Solicitud completada",
                method=method,
                url=url,
                status_code=status_code,
                duration_seconds=round(process_time, 4),
                client_ip=client_ip
            )
        
        # Agregar headers de métricas
        response.headers["X-Process-Time"] = str(process_time)
        
        return response

# Configurar structlog para logging estructurado
def setup_structured_logging():
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
