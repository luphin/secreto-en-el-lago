from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorDatabase
import uuid
import structlog

from app.config.database import get_database
from app.models.loan import (
    LoanCreate, LoanUpdate, LoanInDB, LoanResponse, LoanItem,
    LoanType, LoanStatus
)
from app.models.ejemplar import EjemplarStatus
from app.models.sancion import SancionCreate, SancionType, SancionStatus
from app.services.kafka_service import KafkaService
from app.services.email_service import EmailService

logger = structlog.get_logger()

class LoanService:
    def __init__(self, db: AsyncIOMotorDatabase = None):
        self.db = db if db is not None else get_database()
        self.kafka_service = KafkaService()
        self.email_service = EmailService()
        self.loans_collection = self.db.loans
        self.ejemplares_collection = self.db.ejemplares
        self.documents_collection = self.db.documents
        self.users_collection = self.db.users
        self.sanciones_collection = self.db.sanciones

    async def create_loan(self, loan_data: LoanCreate) -> LoanInDB:
        # Verificar que el usuario existe y no está suspendido
        user = await self.users_collection.find_one({"id": loan_data.usuario_id})
        if not user:
            raise ValueError("Usuario no encontrado")
        
        if user["status"] == "suspendido":
            raise ValueError("Usuario suspendido, no puede realizar préstamos")

        # Verificar disponibilidad de ejemplares
        available_ejemplares = []
        for ejemplar_id in loan_data.ejemplares_ids:
            ejemplar = await self.ejemplares_collection.find_one({
                "id": ejemplar_id,
                "estado": EjemplarStatus.DISPONIBLE.value
            })
            if not ejemplar:
                raise ValueError(f"Ejemplar {ejemplar_id} no disponible")
            available_ejemplares.append(ejemplar)

        loan_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        # Calcular fechas de devolución
        if loan_data.tipo_prestamo == LoanType.DOMICILIO:
            duracion_dias = loan_data.duracion_dias or 7  # Default 7 días
            fecha_devolucion = now + timedelta(days=duracion_dias)
        else:
            # Préstamo en sala: devolución el mismo día
            fecha_devolucion = now.replace(hour=20, minute=0, second=0)  # Cierre biblioteca

        # Crear items del préstamo
        loan_items = []
        for ejemplar in available_ejemplares:
            loan_item = {
                "ejemplar_id": ejemplar["id"],
                "fecha_devolucion": fecha_devolucion,
                "hora_devolucion": "20:00",  # Hora de cierre
                "estado": LoanStatus.ACTIVO.value
            }
            loan_items.append(loan_item)

        loan_dict = {
            "id": loan_id,
            "usuario_id": loan_data.usuario_id,
            "tipo_prestamo": loan_data.tipo_prestamo.value,
            "fecha_prestamo": now,
            "hora_prestamo": now.strftime("%H:%M"),
            "fecha_devolucion": fecha_devolucion,
            "hora_devolucion": "20:00",
            "items": loan_items,
            "estado_general": LoanStatus.ACTIVO.value,
            "created_at": now,
            "updated_at": now
        }

        # Actualizar estado de ejemplares
        for ejemplar_id in loan_data.ejemplares_ids:
            estado = (
                EjemplarStatus.PRESTADO_DOMICILIO.value 
                if loan_data.tipo_prestamo == LoanType.DOMICILIO 
                else EjemplarStatus.PRESTADO_SALA.value
            )
            
            await self.ejemplares_collection.update_one(
                {"id": ejemplar_id},
                {"$set": {"estado": estado, "updated_at": now}}
            )

        # Actualizar contadores de documentos
        for ejemplar in available_ejemplares:
            await self.documents_collection.update_one(
                {"id": ejemplar["documento_id"]},
                {"$inc": {"ejemplares_disponibles": -1}}
            )

        await self.loans_collection.insert_one(loan_dict)
        
        # Enviar notificación via Kafka
        await self.kafka_service.send_loan_created_event(loan_id, loan_data.usuario_id)
        
        logger.info("Préstamo creado", loan_id=loan_id, usuario_id=loan_data.usuario_id)
        return LoanInDB(**loan_dict)

    async def return_loan_items(self, loan_id: str, ejemplares_ids: List[str]) -> bool:
        loan = await self.loans_collection.find_one({"id": loan_id})
        if not loan:
            raise ValueError("Préstamo no encontrado")

        now = datetime.utcnow()
        items_updated = 0

        for item in loan["items"]:
            if item["ejemplar_id"] in ejemplares_ids and item["estado"] == LoanStatus.ACTIVO.value:
                item["estado"] = LoanStatus.DEVUELTO.value
                items_updated += 1

                # Actualizar ejemplar
                await self.ejemplares_collection.update_one(
                    {"id": item["ejemplar_id"]},
                    {"$set": {"estado": EjemplarStatus.DISPONIBLE.value, "updated_at": now}}
                )

                # Actualizar contador de documento
                ejemplar = await self.ejemplares_collection.find_one({"id": item["ejemplar_id"]})
                if ejemplar:
                    await self.documents_collection.update_one(
                        {"id": ejemplar["documento_id"]},
                        {"$inc": {"ejemplares_disponibles": 1}}
                    )

        # Verificar si todos los items fueron devueltos
        all_returned = all(item["estado"] == LoanStatus.DEVUELTO.value for item in loan["items"])
        if all_returned:
            await self.loans_collection.update_one(
                {"id": loan_id},
                {
                    "$set": {
                        "estado_general": LoanStatus.DEVUELTO.value,
                        "fecha_devolucion_real": now,
                        "hora_devolucion_real": now.strftime("%H:%M"),
                        "updated_at": now
                    }
                }
            )
        else:
            await self.loans_collection.update_one(
                {"id": loan_id},
                {
                    "$set": {
                        "items": loan["items"],
                        "updated_at": now
                    }
                }
            )

        # Verificar retrasos y aplicar sanciones
        if now > loan["fecha_devolucion"]:
            dias_retraso = (now - loan["fecha_devolucion"]).days
            if dias_retraso > 0:
                await self._apply_sanction(loan["usuario_id"], loan_id, dias_retraso)

        logger.info("Items devueltos", loan_id=loan_id, items_devueltos=items_updated)
        return items_updated > 0

    async def _apply_sanction(self, usuario_id: str, loan_id: str, dias_retraso: int):
        # Calcular días de sanción (1 día de sanción por cada 2 días de retraso)
        dias_sancion = max(1, dias_retraso // 2)
        
        sancion_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        sancion_dict = {
            "id": sancion_id,
            "usuario_id": usuario_id,
            "tipo": SancionType.RETRASO.value,
            "prestamo_id": loan_id,
            "dias_sancion": dias_sancion,
            "fecha_inicio": now,
            "fecha_fin": now + timedelta(days=dias_sancion),
            "descripcion": f"Sanción por retraso de {dias_retraso} días en devolución",
            "estado": SancionStatus.ACTIVA.value,
            "created_at": now,
            "updated_at": now
        }

        await self.sanciones_collection.insert_one(sancion_dict)
        
        # Suspender usuario
        await self.users_collection.update_one(
            {"id": usuario_id},
            {
                "$set": {
                    "status": "suspendido",
                    "suspension_end": now + timedelta(days=dias_sancion),
                    "updated_at": now
                }
            }
        )

        # Enviar notificación de sanción
        user = await self.users_collection.find_one({"id": usuario_id})
        if user:
            await self.email_service.send_sanction_email(
                user["email"],
                dias_sancion,
                f"Retraso de {dias_retraso} días en devolución"
            )

        logger.info("Sanción aplicada", usuario_id=usuario_id, dias_sancion=dias_sancion)

    async def get_user_loans(self, usuario_id: str, activos: bool = True) -> List[LoanInDB]:
        query = {"usuario_id": usuario_id}
        if activos:
            query["estado_general"] = LoanStatus.ACTIVO.value

        cursor = self.loans_collection.find(query).sort("fecha_prestamo", -1)
        loans = await cursor.to_list(length=None)
        return [LoanInDB(**loan) for loan in loans]

    async def get_overdue_loans(self) -> List[LoanInDB]:
        now = datetime.utcnow()
        cursor = self.loans_collection.find({
            "estado_general": LoanStatus.ACTIVO.value,
            "fecha_devolucion": {"$lt": now}
        })
        loans = await cursor.to_list(length=None)
        return [LoanInDB(**loan) for loan in loans]

    async def get_loan(self, loan_id: str) -> Optional[LoanInDB]:
        loan = await self.loans_collection.find_one({"id": loan_id})
        if loan:
            return LoanInDB(**loan)
        return None

    async def extend_loan(self, loan_id: str, dias_extension: int) -> bool:
        loan = await self.loans_collection.find_one({"id": loan_id})
        if not loan:
            return False

        nueva_fecha = loan["fecha_devolucion"] + timedelta(days=dias_extension)
        
        result = await self.loans_collection.update_one(
            {"id": loan_id},
            {
                "$set": {
                    "fecha_devolucion": nueva_fecha,
                    "updated_at": datetime.utcnow()
                }
            }
        )

        if result.modified_count > 0:
            logger.info("Préstamo extendido", loan_id=loan_id, dias_extension=dias_extension)
            return True
        return False
