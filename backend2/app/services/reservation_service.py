"""
Servicio de gestión de reservas
"""
from datetime import datetime
from typing import Optional, List
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.reservation import ReservationCreate, ReservationStatus


class ReservationService:
    """Servicio para operaciones de reservas"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.reservations
        self.documents_collection = db.documents
        self.users_collection = db.users
    
    async def create_reservation(self, reservation: ReservationCreate) -> Optional[dict]:
        """Crea una nueva reserva"""
        # Verificar que el documento existe
        document = await self.documents_collection.find_one(
            {"_id": ObjectId(reservation.document_id)}
        )
        if not document:
            return None
        
        # Verificar que el usuario existe
        user = await self.users_collection.find_one(
            {"_id": ObjectId(reservation.user_id)}
        )
        if not user:
            return None
        
        # Verificar que no tenga otra reserva activa del mismo documento
        existing = await self.collection.find_one({
            "document_id": reservation.document_id,
            "user_id": reservation.user_id,
            "estado": ReservationStatus.ACTIVA
        })
        if existing:
            return None  # Ya tiene una reserva activa
        
        reservation_dict = reservation.model_dump()
        reservation_dict["fecha_creacion"] = datetime.utcnow()
        reservation_dict["estado"] = ReservationStatus.ACTIVA
        
        result = await self.collection.insert_one(reservation_dict)
        reservation_dict["_id"] = result.inserted_id
        return reservation_dict
    
    async def get_reservation_by_id(self, reservation_id: str) -> Optional[dict]:
        """Obtiene una reserva por su ID"""
        if not ObjectId.is_valid(reservation_id):
            return None
        return await self.collection.find_one({"_id": ObjectId(reservation_id)})
    
    async def get_reservations(
        self,
        skip: int = 0,
        limit: int = 100,
        user_id: Optional[str] = None,
        document_id: Optional[str] = None,
        estado: Optional[ReservationStatus] = None
    ) -> List[dict]:
        """Obtiene una lista de reservas"""
        query = {}
        if user_id:
            query["user_id"] = user_id
        if document_id:
            query["document_id"] = document_id
        if estado:
            query["estado"] = estado
        
        cursor = self.collection.find(query).skip(skip).limit(limit)
        return await cursor.to_list(length=limit)
    
    async def cancel_reservation(self, reservation_id: str) -> Optional[dict]:
        """Cancela una reserva"""
        if not ObjectId.is_valid(reservation_id):
            return None
        
        result = await self.collection.find_one_and_update(
            {"_id": ObjectId(reservation_id)},
            {"$set": {"estado": ReservationStatus.EXPIRADA}},
            return_document=True
        )
        return result
    
    async def complete_reservation(self, reservation_id: str) -> Optional[dict]:
        """Marca una reserva como completada"""
        if not ObjectId.is_valid(reservation_id):
            return None
        
        result = await self.collection.find_one_and_update(
            {"_id": ObjectId(reservation_id)},
            {"$set": {"estado": ReservationStatus.COMPLETADA}},
            return_document=True
        )
        return result
    
    async def expire_old_reservations(self) -> int:
        """Expira reservas cuya fecha ya pasó"""
        result = await self.collection.update_many(
            {
                "estado": ReservationStatus.ACTIVA,
                "fecha_reserva": {"$lt": datetime.utcnow()}
            },
            {"$set": {"estado": ReservationStatus.EXPIRADA}}
        )
        return result.modified_count

