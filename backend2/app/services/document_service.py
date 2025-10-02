"""
Servicio de gestión de documentos
"""
from typing import Optional, List
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.document import DocumentCreate, DocumentUpdate
from app.models.item import ItemStatus


class DocumentService:
    """Servicio para operaciones CRUD de documentos"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.documents
        self.items_collection = db.items
    
    async def create_document(self, document: DocumentCreate) -> dict:
        """Crea un nuevo documento"""
        document_dict = document.model_dump()
        result = await self.collection.insert_one(document_dict)
        document_dict["_id"] = result.inserted_id
        return document_dict
    
    async def get_document_by_id(self, document_id: str) -> Optional[dict]:
        """Obtiene un documento por su ID"""
        if not ObjectId.is_valid(document_id):
            return None
        return await self.collection.find_one({"_id": ObjectId(document_id)})
    
    async def get_documents(
        self,
        skip: int = 0,
        limit: int = 100,
        titulo: Optional[str] = None,
        autor: Optional[str] = None,
        categoria: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[dict]:
        """Obtiene una lista de documentos con filtros"""
        query = {}
        
        if search:
            # Búsqueda por texto completo
            query["$text"] = {"$search": search}
        else:
            # Búsqueda por filtros específicos
            if titulo:
                query["titulo"] = {"$regex": titulo, "$options": "i"}
            if autor:
                query["autor"] = {"$regex": autor, "$options": "i"}
            if categoria:
                query["categoria"] = {"$regex": categoria, "$options": "i"}
        
        cursor = self.collection.find(query).skip(skip).limit(limit)
        documents = await cursor.to_list(length=limit)
        
        # Agregar información de disponibilidad
        for doc in documents:
            doc["items_disponibles"] = await self._count_available_items(str(doc["_id"]))
        
        return documents
    
    async def update_document(
        self,
        document_id: str,
        document_update: DocumentUpdate
    ) -> Optional[dict]:
        """Actualiza un documento"""
        if not ObjectId.is_valid(document_id):
            return None
        
        update_data = document_update.model_dump(exclude_unset=True)
        
        if not update_data:
            return await self.get_document_by_id(document_id)
        
        result = await self.collection.find_one_and_update(
            {"_id": ObjectId(document_id)},
            {"$set": update_data},
            return_document=True
        )
        return result
    
    async def delete_document(self, document_id: str) -> bool:
        """Elimina un documento"""
        if not ObjectId.is_valid(document_id):
            return False
        
        # Verificar que no tenga ejemplares asociados
        items_count = await self.items_collection.count_documents(
            {"document_id": document_id}
        )
        if items_count > 0:
            return False  # No se puede eliminar si tiene ejemplares
        
        result = await self.collection.delete_one({"_id": ObjectId(document_id)})
        return result.deleted_count > 0
    
    async def _count_available_items(self, document_id: str) -> int:
        """Cuenta los ejemplares disponibles de un documento"""
        return await self.items_collection.count_documents({
            "document_id": document_id,
            "estado": ItemStatus.DISPONIBLE
        })

