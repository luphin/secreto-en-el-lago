"""
Servicio de gestión de usuarios
"""
from datetime import datetime
from typing import Optional, List
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.user import UserCreate, UserUpdate, UserInDB, UserRole
from app.core.security import get_password_hash, verify_password


class UserService:
    """Servicio para operaciones CRUD de usuarios"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.users
    
    async def create_user(self, user: UserCreate) -> dict:
        """Crea un nuevo usuario"""
        user_dict = user.model_dump()
        user_dict["password"] = get_password_hash(user.password)
        user_dict["activo"] = False  # Requiere activación
        user_dict["fecha_creacion"] = datetime.utcnow()
        
        result = await self.collection.insert_one(user_dict)
        user_dict["_id"] = result.inserted_id
        return user_dict
    
    async def get_user_by_id(self, user_id: str) -> Optional[dict]:
        """Obtiene un usuario por su ID"""
        if not ObjectId.is_valid(user_id):
            return None
        return await self.collection.find_one({"_id": ObjectId(user_id)})
    
    async def get_user_by_email(self, email: str) -> Optional[dict]:
        """Obtiene un usuario por su email"""
        return await self.collection.find_one({"email": email})
    
    async def get_user_by_rut(self, rut: str) -> Optional[dict]:
        """Obtiene un usuario por su RUT"""
        return await self.collection.find_one({"rut": rut})
    
    async def get_users(
        self,
        skip: int = 0,
        limit: int = 100,
        rol: Optional[UserRole] = None
    ) -> List[dict]:
        """Obtiene una lista de usuarios"""
        query = {}
        if rol:
            query["rol"] = rol
        
        cursor = self.collection.find(query).skip(skip).limit(limit)
        return await cursor.to_list(length=limit)
    
    async def update_user(self, user_id: str, user_update: UserUpdate) -> Optional[dict]:
        """Actualiza un usuario"""
        if not ObjectId.is_valid(user_id):
            return None
        
        update_data = user_update.model_dump(exclude_unset=True)
        
        # Hash de la contraseña si se está actualizando
        if "password" in update_data and update_data["password"]:
            update_data["password"] = get_password_hash(update_data["password"])
        
        if not update_data:
            return await self.get_user_by_id(user_id)
        
        result = await self.collection.find_one_and_update(
            {"_id": ObjectId(user_id)},
            {"$set": update_data},
            return_document=True
        )
        return result
    
    async def delete_user(self, user_id: str) -> bool:
        """Elimina un usuario"""
        if not ObjectId.is_valid(user_id):
            return False
        
        result = await self.collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0
    
    async def activate_user(self, user_id: str) -> Optional[dict]:
        """Activa la cuenta de un usuario"""
        if not ObjectId.is_valid(user_id):
            return None
        
        result = await self.collection.find_one_and_update(
            {"_id": ObjectId(user_id)},
            {"$set": {"activo": True}},
            return_document=True
        )
        return result
    
    async def authenticate_user(self, email: str, password: str) -> Optional[dict]:
        """Autentica a un usuario"""
        user = await self.get_user_by_email(email)
        if not user:
            return None
        if not verify_password(password, user["password"]):
            return None
        return user
    
    async def is_user_sanctioned(self, user_id: str) -> bool:
        """Verifica si un usuario está sancionado"""
        user = await self.get_user_by_id(user_id)
        if not user:
            return False
        
        if user.get("sancion_hasta"):
            return user["sancion_hasta"] > datetime.utcnow()
        return False

