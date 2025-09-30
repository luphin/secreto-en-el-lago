from typing import List, Optional, Dict, Any
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase
import uuid
import structlog

from app.config.database import get_database
from app.models.document import (
    DocumentCreate, DocumentUpdate, DocumentInDB, DocumentResponse,
    DocumentType, DocumentCategory, DocumentStatus
)
from app.models.ejemplar import EjemplarCreate, EjemplarInDB, EjemplarStatus
from app.services.kafka_service import KafkaService

logger = structlog.get_logger()

class DocumentService:
    def __init__(self, db: AsyncIOMotorDatabase = None):
        self.db = db if db is not None else get_database()
        self.kafka_service = KafkaService()
        self.documents_collection = self.db.documents
        self.ejemplares_collection = self.db.ejemplares

    async def create_document(self, document_data: DocumentCreate) -> DocumentInDB:
        document_id = str(uuid.uuid4())
        
        document_dict = {
            "id": document_id,
            "titulo": document_data.titulo,
            "autor": document_data.autor,
            "tipo": document_data.tipo.value,
            "categoria": document_data.categoria.value,
            "editorial": document_data.editorial,
            "edicion": document_data.edicion,
            "ano_edicion": document_data.ano_edicion,
            "isbn": document_data.isbn,
            "descripcion": document_data.descripcion,
            "formato_medio": document_data.formato_medio.value if document_data.formato_medio else None,
            "duracion": document_data.duracion,
            "numero_ejemplares": document_data.numero_ejemplares,
            "ejemplares_disponibles": document_data.numero_ejemplares,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        await self.documents_collection.insert_one(document_dict)
        
        # Crear ejemplares
        await self._create_ejemplares(document_id, document_data.numero_ejemplares)
        
        logger.info("Documento creado", document_id=document_id, titulo=document_data.titulo)
        return DocumentInDB(**document_dict)

    async def _create_ejemplares(self, document_id: str, numero_ejemplares: int):
        ejemplares = []
        for i in range(numero_ejemplares):
            ejemplar_id = str(uuid.uuid4())
            ejemplar = {
                "id": ejemplar_id,
                "documento_id": document_id,
                "codigo_ubicacion": f"DOC-{document_id[:8]}-{i+1:03d}",
                "estado": EjemplarStatus.DISPONIBLE.value,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            ejemplares.append(ejemplar)
        
        if ejemplares:
            await self.ejemplares_collection.insert_many(ejemplares)

    async def get_document(self, document_id: str) -> Optional[DocumentInDB]:
        document = await self.documents_collection.find_one({"id": document_id})
        if document:
            return DocumentInDB(**document)
        return None

    async def get_documents(
        self,
        skip: int = 0,
        limit: int = 100,
        tipo: Optional[DocumentType] = None,
        categoria: Optional[DocumentCategory] = None,
        disponible: Optional[bool] = None
    ) -> List[DocumentInDB]:
        query = {}
        if tipo:
            query["tipo"] = tipo.value
        if categoria:
            query["categoria"] = categoria.value
        if disponible is not None:
            if disponible:
                query["ejemplares_disponibles"] = {"$gt": 0}
            else:
                query["ejemplares_disponibles"] = 0

        cursor = self.documents_collection.find(query).skip(skip).limit(limit)
        documents = await cursor.to_list(length=limit)
        return [DocumentInDB(**doc) for doc in documents]

    async def search_documents(
        self,
        query: str,
        tipo: Optional[DocumentType] = None,
        categoria: Optional[DocumentCategory] = None
    ) -> List[DocumentInDB]:
        search_query = {
            "$or": [
                {"titulo": {"$regex": query, "$options": "i"}},
                {"autor": {"$regex": query, "$options": "i"}},
                {"editorial": {"$regex": query, "$options": "i"}},
                {"descripcion": {"$regex": query, "$options": "i"}}
            ]
        }
        
        if tipo:
            search_query["tipo"] = tipo.value
        if categoria:
            search_query["categoria"] = categoria.value

        cursor = self.documents_collection.find(search_query).limit(50)
        documents = await cursor.to_list(length=50)
        return [DocumentInDB(**doc) for doc in documents]

    async def update_document(self, document_id: str, document_update: DocumentUpdate) -> Optional[DocumentInDB]:
        update_data = document_update.dict(exclude_unset=True)
        update_data["updated_at"] = datetime.utcnow()

        result = await self.documents_collection.update_one(
            {"id": document_id},
            {"$set": update_data}
        )

        if result.modified_count == 0:
            return None

        updated_document = await self.get_document(document_id)
        logger.info("Documento actualizado", document_id=document_id)
        return updated_document

    async def add_ejemplar(self, document_id: str) -> bool:
        document = await self.get_document(document_id)
        if not document:
            return False

        # Actualizar contadores
        await self.documents_collection.update_one(
            {"id": document_id},
            {
                "$inc": {
                    "numero_ejemplares": 1,
                    "ejemplares_disponibles": 1
                },
                "$set": {"updated_at": datetime.utcnow()}
            }
        )

        # Crear nuevo ejemplar
        ejemplar_id = str(uuid.uuid4())
        ejemplar = {
            "id": ejemplar_id,
            "documento_id": document_id,
            "codigo_ubicacion": f"DOC-{document_id[:8]}-{document.numero_ejemplares + 1:03d}",
            "estado": EjemplarStatus.DISPONIBLE.value,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        await self.ejemplares_collection.insert_one(ejemplar)
        logger.info("Ejemplar agregado", document_id=document_id, ejemplar_id=ejemplar_id)
        return True

    async def get_document_ejemplares(self, document_id: str) -> List[EjemplarInDB]:
        cursor = self.ejemplares_collection.find({"documento_id": document_id})
        ejemplares = await cursor.to_list(length=None)
        return [EjemplarInDB(**ejemplar) for ejemplar in ejemplares]

    async def get_available_ejemplares(self, document_id: str) -> List[EjemplarInDB]:
        cursor = self.ejemplares_collection.find({
            "documento_id": document_id,
            "estado": EjemplarStatus.DISPONIBLE.value
        })
        ejemplares = await cursor.to_list(length=None)
        return [EjemplarInDB(**ejemplar) for ejemplar in ejemplares]

    async def get_document_stats(self) -> Dict[str, Any]:
        pipeline = [
            {
                "$group": {
                    "_id": "$tipo",
                    "total_documentos": {"$sum": 1},
                    "total_ejemplares": {"$sum": "$numero_ejemplares"},
                    "ejemplares_disponibles": {"$sum": "$ejemplares_disponibles"}
                }
            }
        ]
        
        stats = await self.documents_collection.aggregate(pipeline).to_list(length=None)
        return {"por_tipo": stats}
