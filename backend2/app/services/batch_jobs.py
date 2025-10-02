"""
Procesos batch para tareas programadas
"""
import asyncio
import logging
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings
from app.core.kafka_producer import kafka_producer
from app.services.loan_service import LoanService
from app.services.reservation_service import ReservationService
from app.services.user_service import UserService

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BatchJobsRunner:
    """Ejecutor de trabajos batch"""
    
    def __init__(self):
        self.client = None
        self.db = None
    
    async def connect_db(self):
        """Conecta a la base de datos"""
        self.client = AsyncIOMotorClient(settings.MONGODB_URL)
        self.db = self.client[settings.MONGODB_DB_NAME]
        logger.info("✓ Conectado a MongoDB")
    
    async def close_db(self):
        """Cierra la conexión a la base de datos"""
        if self.client:
            self.client.close()
            logger.info("✓ Conexión a MongoDB cerrada")
    
    async def check_overdue_loans(self):
        """Verifica préstamos vencidos y envía notificaciones"""
        logger.info("📋 Verificando préstamos vencidos...")
        
        loan_service = LoanService(self.db)
        user_service = UserService(self.db)
        
        # Marcar préstamos como vencidos
        updated_count = await loan_service.mark_loans_as_overdue()
        logger.info(f"✓ {updated_count} préstamos marcados como vencidos")
        
        # Obtener préstamos vencidos
        overdue_loans = await loan_service.get_overdue_loans()
        
        # Enviar notificaciones
        for loan in overdue_loans:
            user = await user_service.get_user_by_id(loan["user_id"])
            if not user:
                continue
            
            # Calcular días de atraso
            days_overdue = (datetime.utcnow() - loan["fecha_devolucion_pactada"]).days
            
            # Obtener información del documento (simplificado)
            document = await self.db.documents.find_one(
                {"_id": await self.db.items.find_one({"_id": loan["item_id"]}).get("document_id")}
            )
            
            loan_details = {
                "document_title": document.get("titulo", "N/A") if document else "N/A",
                "due_date": loan["fecha_devolucion_pactada"].strftime("%d/%m/%Y"),
                "days_overdue": days_overdue
            }
            
            # Enviar notificación
            await kafka_producer.send_overdue_reminder(
                user_email=user["email"],
                user_name=f"{user['nombres']} {user['apellidos']}",
                loan_details=loan_details
            )
        
        logger.info(f"✓ {len(overdue_loans)} notificaciones de préstamos vencidos enviadas")
    
    async def expire_old_reservations(self):
        """Expira reservas antiguas"""
        logger.info("📋 Expirando reservas antiguas...")
        
        reservation_service = ReservationService(self.db)
        expired_count = await reservation_service.expire_old_reservations()
        
        logger.info(f"✓ {expired_count} reservas expiradas")
    
    async def run_daily_jobs(self):
        """Ejecuta trabajos diarios"""
        logger.info("🌅 Iniciando trabajos batch diarios...")
        
        await self.connect_db()
        await kafka_producer.start()
        
        try:
            await self.check_overdue_loans()
            await self.expire_old_reservations()
            logger.info("✨ Trabajos batch completados exitosamente")
        except Exception as e:
            logger.error(f"✗ Error en trabajos batch: {e}")
        finally:
            await kafka_producer.stop()
            await self.close_db()


async def run_batch_jobs():
    """Función principal para ejecutar los trabajos batch"""
    runner = BatchJobsRunner()
    await runner.run_daily_jobs()


if __name__ == "__main__":
    asyncio.run(run_batch_jobs())

