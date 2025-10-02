"""
Servicio de gestión de ejemplares (items)
"""
from typing import Optional, List
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.item import ItemCreate, ItemUpdate, ItemStatus


class ItemService:
    """Servicio para operaciones CRUD de ejemplares"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.items
    
    async def create_item(self, item: ItemCreate) -> dict:
        """Crea un nuevo ejemplar"""
        item_dict = item.model_dump()
        result = await self.collection.insert_one(item_dict)
        item_dict["_id"] = result.inserted_id
        return item_dict
    
    async def get_item_by_id(self, item_id: str) -> Optional[dict]:
        """Obtiene un ejemplar por su ID"""
        if not ObjectId.is_valid(item_id):
            return None
        return await self.collection.find_one({"_id": ObjectId(item_id)})
    
    async def get_items(
        self,
        skip: int = 0,
        limit: int = 100,
        document_id: Optional[str] = None,
        estado: Optional[ItemStatus] = None
    ) -> List[dict]:
        """Obtiene una lista de ejemplares"""
        query = {}
        if document_id:
            query["document_id"] = document_id
        if estado:
            query["estado"] = estado
        
        cursor = self.collection.find(query).skip(skip).limit(limit)
        return await cursor.to_list(length=limit)
    
    async def update_item(self, item_id: str, item_update: ItemUpdate) -> Optional[dict]:
        """Actualiza un ejemplar"""
        if not ObjectId.is_valid(item_id):
            return None
        
        update_data = item_update.model_dump(exclude_unset=True)
        
        if not update_data:
            return await self.get_item_by_id(item_id)
        
        result = await self.collection.find_one_and_update(
            {"_id": ObjectId(item_id)},
            {"$set": update_data},
            return_document=True
        )
        return result
    
    async def delete_item(self, item_id: str) -> bool:
        """Elimina un ejemplar"""
        if not ObjectId.is_valid(item_id):
            return False
        
        result = await self.collection.delete_one({"_id": ObjectId(item_id)})
        return result.deleted_count > 0
    
    async def update_item_status(self, item_id: str, status: ItemStatus) -> Optional[dict]:
        """Actualiza el estado de un ejemplar"""
        if not ObjectId.is_valid(item_id):
            return None
        
        result = await self.collection.find_one_and_update(
            {"_id": ObjectId(item_id)},
            {"$set": {"estado": status}},
            return_document=True
        )
        return result
    
    async def get_available_item_for_document(self, document_id: str) -> Optional[dict]:
        """Obtiene un ejemplar disponible para un documento"""
        return await self.collection.find_one({
            "document_id": document_id,
            "estado": ItemStatus.DISPONIBLE
        })

