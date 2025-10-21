"""
Servicio de gestión de préstamos
"""
from datetime import datetime, timedelta
from typing import Optional, List
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.loan import LoanCreate, LoanType, LoanStatus
from app.models.item import ItemStatus
from app.core.config import settings


class LoanService:
    """Servicio para operaciones de préstamos"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.loans
        self.items_collection = db.items
        self.users_collection = db.users
    
    async def create_loan(self, loan: LoanCreate) -> Optional[dict]:
        """Crea un nuevo préstamo"""
        # Verificar que el item esté disponible
        item = await self.items_collection.find_one({
            "_id": ObjectId(loan.item_id),
            "estado": ItemStatus.DISPONIBLE
        })
        if not item:
            return None
        
        # Verificar que el usuario no esté sancionado
        user = await self.users_collection.find_one({"_id": ObjectId(loan.user_id)})
        if user and user.get("sancion_hasta"):
            if user["sancion_hasta"] > datetime.utcnow():
                return None  # Usuario sancionado
        
        # Calcular fecha de devolución
        fecha_prestamo = datetime.utcnow()
        if loan.tipo_prestamo == LoanType.DOMICILIO:
            fecha_devolucion = fecha_prestamo + timedelta(days=settings.LOAN_DAYS_HOME)
        else:  # SALA
            fecha_devolucion = fecha_prestamo + timedelta(hours=settings.LOAN_HOURS_ROOM)
        
        loan_dict = loan.model_dump()
        loan_dict["fecha_prestamo"] = fecha_prestamo
        loan_dict["fecha_devolucion_pactada"] = fecha_devolucion
        loan_dict["fecha_devolucion_real"] = None
        loan_dict["estado"] = LoanStatus.ACTIVO
        
        # Crear el préstamo
        result = await self.collection.insert_one(loan_dict)
        loan_dict["_id"] = result.inserted_id
        
        # Actualizar estado del item
        await self.items_collection.update_one(
            {"_id": ObjectId(loan.item_id)},
            {"$set": {"estado": ItemStatus.PRESTADO}}
        )
        
        return loan_dict
    
    async def get_loan_by_id(self, loan_id: str) -> Optional[dict]:
        """Obtiene un préstamo por su ID"""
        if not ObjectId.is_valid(loan_id):
            return None
        return await self.collection.find_one({"_id": ObjectId(loan_id)})
    
    async def get_loans(
        self,
        skip: int = 0,
        limit: int = 100,
        user_id: Optional[str] = None,
        estado: Optional[LoanStatus] = None
    ) -> List[dict]:
        """Obtiene una lista de préstamos"""
        query = {}
        if user_id:
            query["user_id"] = user_id
        if estado:
            query["estado"] = estado
        
        cursor = self.collection.find(query).skip(skip).limit(limit)
        return await cursor.to_list(length=limit)
    
    async def return_loan(self, loan_id: str) -> Optional[dict]:
        """Procesa la devolución de un préstamo"""
        if not ObjectId.is_valid(loan_id):
            return None
        
        loan = await self.get_loan_by_id(loan_id)
        if not loan or loan["estado"] != LoanStatus.ACTIVO:
            return None
        
        fecha_devolucion = datetime.utcnow()
        
        # Actualizar préstamo
        update_data = {
            "fecha_devolucion_real": fecha_devolucion,
            "estado": LoanStatus.DEVUELTO
        }
        
        # Verificar si está vencido y calcular sanción
        dias_atraso = 0
        if fecha_devolucion > loan["fecha_devolucion_pactada"]:
            dias_atraso = (fecha_devolucion - loan["fecha_devolucion_pactada"]).days
            dias_sancion = dias_atraso * settings.SANCTION_MULTIPLIER
            
            # Aplicar sanción al usuario
            fecha_fin_sancion = fecha_devolucion + timedelta(days=dias_sancion)
            await self.users_collection.update_one(
                {"_id": ObjectId(loan["user_id"])},
                {"$set": {"sancion_hasta": fecha_fin_sancion}}
            )
        
        result = await self.collection.find_one_and_update(
            {"_id": ObjectId(loan_id)},
            {"$set": update_data},
            return_document=True
        )
        
        # Actualizar estado del item
        await self.items_collection.update_one(
            {"_id": ObjectId(loan["item_id"])},
            {"$set": {"estado": ItemStatus.DISPONIBLE}}
        )
        
        return result
    
    async def get_overdue_loans(self) -> List[dict]:
        """Obtiene préstamos vencidos"""
        cursor = self.collection.find({
            "estado": LoanStatus.ACTIVO,
            "fecha_devolucion_pactada": {"$lt": datetime.utcnow()}
        })
        return await cursor.to_list(length=None)
    
    async def mark_loans_as_overdue(self) -> int:
        """Marca préstamos activos como vencidos si pasó su fecha"""
        result = await self.collection.update_many(
            {
                "estado": LoanStatus.ACTIVO,
                "fecha_devolucion_pactada": {"$lt": datetime.utcnow()}
            },
            {"$set": {"estado": LoanStatus.VENCIDO}}
        )
        return result.modified_count

