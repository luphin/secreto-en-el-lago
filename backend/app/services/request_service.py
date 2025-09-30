from typing import List, Optional
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase
import uuid
import structlog

from app.config.database import get_database
from app.models.request import (
    RequestCreate, RequestUpdate, RequestInDB, RequestResponse, 
    RequestItem, RequestType, RequestStatus
)
from app.services.kafka_service import KafkaService

logger = structlog.get_logger()

class RequestService:
    def __init__(self, db: AsyncIOMotorDatabase = None):
        self.db = db or get_database()
        self.kafka_service = KafkaService()
        self.requests_collection = self.db.requests
        self.documents_collection = self.db.documents
        self.users_collection = self.db.users

    async def create_request(self, request_data: RequestCreate) -> RequestInDB:
        # Verificar que el usuario existe
        user = await self.users_collection.find_one({"id": request_data.usuario_id})
        if not user:
            raise ValueError("Usuario no encontrado")

        # Verificar que los documentos existen
        for doc_id in request_data.documentos_ids:
            document = await self.documents_collection.find_one({"id": doc_id})
            if not document:
                raise ValueError(f"Documento {doc_id} no encontrado")

        request_id = str(uuid.uuid4())
        now = datetime.utcnow()

        # Crear items de la solicitud
        request_items = []
        for doc_id in request_data.documentos_ids:
            item = {
                "documento_id": doc_id,
                "estado": RequestStatus.PENDIENTE.value
            }
            request_items.append(item)

        request_dict = {
            "id": request_id,
            "usuario_id": request_data.usuario_id,
            "tipo_solicitud": request_data.tipo_solicitud.value,
            "fecha_solicitud": now,
            "hora_solicitud": now.strftime("%H:%M"),
            "fecha_reserva": request_data.fecha_reserva,
            "items": request_items,
            "estado": RequestStatus.PENDIENTE.value,
            "created_at": now,
            "updated_at": now
        }

        await self.requests_collection.insert_one(request_dict)
        
        # Enviar evento Kafka
        await self.kafka_service.send_system_alert_event(
            "request_created",
            f"Nueva solicitud {request_data.tipo_solicitud.value} creada",
            "info"
        )

        logger.info("Solicitud creada", request_id=request_id, tipo=request_data.tipo_solicitud.value)
        return RequestInDB(**request_dict)

    async def get_request(self, request_id: str) -> Optional[RequestInDB]:
        request = await self.requests_collection.find_one({"id": request_id})
        if request:
            return RequestInDB(**request)
        return None

    async def get_requests(
        self,
        skip: int = 0,
        limit: int = 100,
        tipo: Optional[RequestType] = None,
        estado: Optional[str] = None
    ) -> List[RequestInDB]:
        query = {}
        if tipo:
            query["tipo_solicitud"] = tipo.value
        if estado:
            query["estado"] = estado

        cursor = self.requests_collection.find(query).skip(skip).limit(limit).sort("fecha_solicitud", -1)
        requests = await cursor.to_list(length=limit)
        return [RequestInDB(**req) for req in requests]

    async def process_request(self, request_id: str, processed_by: str) -> bool:
        request = await self.requests_collection.find_one({"id": request_id})
        if not request:
            return False

        now = datetime.utcnow()
        result = await self.requests_collection.update_one(
            {"id": request_id},
            {
                "$set": {
                    "estado": RequestStatus.PROCESADA.value,
                    "procesada_por": processed_by,
                    "fecha_procesamiento": now,
                    "updated_at": now
                }
            }
        )

        if result.modified_count > 0:
            logger.info("Solicitud procesada", request_id=request_id, processed_by=processed_by)
            return True
        return False

    async def cancel_request(self, request_id: str, user_id: str) -> bool:
        request = await self.requests_collection.find_one({"id": request_id})
        if not request:
            return False

        # Verificar que el usuario es el dueño de la solicitud o es admin
        if request["usuario_id"] != user_id:
            # Verificar si es admin
            user = await self.users_collection.find_one({"id": user_id})
            if not user or user["role"] not in ["admin", "librarian"]:
                return False

        result = await self.requests_collection.update_one(
            {"id": request_id},
            {
                "$set": {
                    "estado": RequestStatus.CANCELADA.value,
                    "updated_at": datetime.utcnow()
                }
            }
        )

        if result.modified_count > 0:
            logger.info("Solicitud cancelada", request_id=request_id, user_id=user_id)
            return True
        return False

    async def get_user_requests(self, usuario_id: str, activas: bool = True) -> List[RequestInDB]:
        query = {"usuario_id": usuario_id}
        if activas:
            query["estado"] = {"$in": [RequestStatus.PENDIENTE.value, RequestStatus.PROCESADA.value]}

        cursor = self.requests_collection.find(query).sort("fecha_solicitud", -1)
        requests = await cursor.to_list(length=None)
        return [RequestInDB(**req) for req in requests]
