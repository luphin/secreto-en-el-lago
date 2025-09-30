from prometheus_client import Counter, Histogram, Gauge, generate_latest, REGISTRY
import time
import structlog

logger = structlog.get_logger()

# Métricas de solicitudes HTTP
REQUEST_COUNT = Counter(
    'biblioteca_requests_total',
    'Total de solicitudes HTTP',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'biblioteca_request_duration_seconds',
    'Duración de las solicitudes HTTP',
    ['method', 'endpoint'],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
)

# Métricas de negocio
ACTIVE_LOANS = Gauge(
    'biblioteca_loans_active',
    'Número de préstamos activos'
)

TOTAL_USERS = Gauge(
    'biblioteca_users_total',
    'Total de usuarios registrados'
)

DOCUMENTS_AVAILABLE = Gauge(
    'biblioteca_documents_available',
    'Número de documentos disponibles'
)

LOANS_CREATED = Counter(
    'biblioteca_loans_created_total',
    'Total de préstamos creados'
)

LOANS_RETURNED = Counter(
    'biblioteca_loans_returned_total',
    'Total de préstamos devueltos'
)

OVERDUE_LOANS = Gauge(
    'biblioteca_loans_overdue',
    'Número de préstamos vencidos'
)

# Métricas de Kafka
KAFKA_MESSAGES_SENT = Counter(
    'biblioteca_kafka_messages_sent_total',
    'Total de mensajes Kafka enviados',
    ['topic']
)

KAFKA_MESSAGES_PROCESSED = Counter(
    'biblioteca_kafka_messages_processed_total',
    'Total de mensajes Kafka procesados',
    ['topic']
)

KAFKA_PROCESSING_ERRORS = Counter(
    'biblioteca_kafka_processing_errors_total',
    'Total de errores procesando mensajes Kafka'
)

# Métricas del sistema
DATABASE_CONNECTIONS = Gauge(
    'biblioteca_database_connections',
    'Número de conexiones a la base de datos'
)

MEMORY_USAGE = Gauge(
    'biblioteca_memory_usage_bytes',
    'Uso de memoria de la aplicación'
)

class MetricsService:
    def __init__(self, db=None):
        self.db = db

    async def update_business_metrics(self):
        """Actualiza las métricas de negocio periódicamente"""
        try:
            # Actualizar préstamos activos
            active_loans_count = await self.db.loans.count_documents({
                "estado_general": "activo"
            })
            ACTIVE_LOANS.set(active_loans_count)

            # Actualizar total de usuarios
            total_users = await self.db.users.count_documents({
                "status": "active"
            })
            TOTAL_USERS.set(total_users)

            # Actualizar documentos disponibles
            available_docs = await self.db.documents.aggregate([
                {"$group": {"_id": None, "total": {"$sum": "$ejemplares_disponibles"}}}
            ]).to_list(length=1)
            
            if available_docs:
                DOCUMENTS_AVAILABLE.set(available_docs[0]['total'])

            # Actualizar préstamos vencidos
            overdue_loans = await self.db.loans.count_documents({
                "estado_general": "activo",
                "fecha_devolucion": {"$lt": time.time()}
            })
            OVERDUE_LOANS.set(overdue_loans)

            logger.debug("Métricas de negocio actualizadas")
            
        except Exception as e:
            logger.error("Error actualizando métricas de negocio", error=str(e))

    def record_request(self, method: str, endpoint: str, status: int, duration: float):
        """Registra una solicitud HTTP para métricas"""
        REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=status).inc()
        REQUEST_DURATION.labels(method=method, endpoint=endpoint).observe(duration)

    def record_loan_created(self):
        """Registra la creación de un préstamo"""
        LOANS_CREATED.inc()

    def record_loan_returned(self):
        """Registra la devolución de un préstamo"""
        LOANS_RETURNED.inc()

    def record_kafka_message_sent(self, topic: str):
        """Registra un mensaje Kafka enviado"""
        KAFKA_MESSAGES_SENT.labels(topic=topic).inc()

    def record_kafka_message_processed(self, topic: str):
        """Registra un mensaje Kafka procesado"""
        KAFKA_MESSAGES_PROCESSED.labels(topic=topic).inc()

    def record_kafka_error(self):
        """Registra un error de procesamiento Kafka"""
        KAFKA_PROCESSING_ERRORS.inc()

# Singleton para el servicio de métricas
metrics_service = MetricsService()
