from typing import List, Optional
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase
import uuid
import structlog

from app.config.database import get_database
from app.models.user import UserInDB, UserUpdate, UserResponse, UserStatus, UserRole
from app.services.kafka_service import KafkaService

logger = structlog.get_logger()

class UserService:
    def __init__(self, db: AsyncIOMotorDatabase = None):
        self.db = db or get_database()
        self.kafka_service = KafkaService()
        self.collection = self.db.users

    async def get_user(self, user_id: str) -> Optional[UserInDB]:
        user = await self.collection.find_one({"id": user_id})
        if user:
            return UserInDB(**user)
        return None

    async def get_users(
        self, 
        skip: int = 0, 
        limit: int = 100,
        status: Optional[UserStatus] = None,
        role: Optional[UserRole] = None
    ) -> List[UserInDB]:
        query = {}
        if status:
            query["status"] = status.value
        if role:
            query["role"] = role.value

        cursor = self.collection.find(query).skip(skip).limit(limit)
        users = await cursor.to_list(length=limit)
        return [UserInDB(**user) for user in users]

    async def update_user(self, user_id: str, user_update: UserUpdate) -> Optional[UserInDB]:
        update_data = user_update.dict(exclude_unset=True)
        update_data["updated_at"] = datetime.utcnow()

        result = await self.collection.update_one(
            {"id": user_id},
            {"$set": update_data}
        )

        if result.modified_count == 0:
            return None

        updated_user = await self.get_user(user_id)
        logger.info("Usuario actualizado", user_id=user_id)
        return updated_user

    async def update_user_status(self, user_id: str, status: UserStatus) -> bool:
        result = await self.collection.update_one(
            {"id": user_id},
            {
                "$set": {
                    "status": status.value,
                    "updated_at": datetime.utcnow()
                }
            }
        )

        if result.modified_count > 0:
            logger.info("Estado de usuario actualizado", user_id=user_id, status=status.value)
            return True
        return False

    async def suspend_user(self, user_id: str, days: int) -> bool:
        suspension_end = datetime.utcnow() + timedelta(days=days)
        
        result = await self.collection.update_one(
            {"id": user_id},
            {
                "$set": {
                    "status": UserStatus.SUSPENDED.value,
                    "suspension_end": suspension_end,
                    "updated_at": datetime.utcnow()
                }
            }
        )

        if result.modified_count > 0:
            logger.info("Usuario suspendido", user_id=user_id, days=days)
            return True
        return False

    async def search_users(self, query: str) -> List[UserInDB]:
        search_query = {
            "$or": [
                {"names": {"$regex": query, "$options": "i"}},
                {"last_names": {"$regex": query, "$options": "i"}},
                {"email": {"$regex": query, "$options": "i"}},
                {"rut": {"$regex": query, "$options": "i"}}
            ]
        }

        cursor = self.collection.find(search_query).limit(50)
        users = await cursor.to_list(length=50)
        return [UserInDB(**user) for user in users]

    async def get_users_with_active_loans(self) -> List[UserInDB]:
        # Buscar usuarios con préstamos activos
        active_loans = await self.db.loans.find({
            "estado_general": "activo"
        }).to_list(length=None)
        
        user_ids = list(set(loan["usuario_id"] for loan in active_loans))
        
        if not user_ids:
            return []
            
        cursor = self.collection.find({"id": {"$in": user_ids}})
        users = await cursor.to_list(length=len(user_ids))
        return [UserInDB(**user) for user in users]
