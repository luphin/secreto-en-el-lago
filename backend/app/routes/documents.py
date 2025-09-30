from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.services.document_service import DocumentService
from app.schemas.document import (
    DocumentCreate, DocumentUpdate, DocumentResponse, 
    DocumentType, DocumentCategory, MediaFormat
)
from app.schemas.ejemplar import EjemplarResponse
from app.schemas.user import UserRole
from app.middleware.auth import get_current_user, require_roles

router = APIRouter()

def get_document_service() -> DocumentService:
    """Dependency para obtener una instancia de DocumentService"""
    return DocumentService()

@router.post("/", response_model=DocumentResponse, status_code=201)
async def create_document(
    document_data: DocumentCreate,
    document_service: DocumentService = Depends(get_document_service),
    current_user = Depends(require_roles([UserRole.ADMIN, UserRole.LIBRARIAN]))
):
    """CU2: Administrar Colección - RF2"""
    try:
        return await document_service.create_document(document_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[DocumentResponse])
async def get_documents(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    tipo: Optional[DocumentType] = None,
    categoria: Optional[DocumentCategory] = None,
    disponible: Optional[bool] = None,
    document_service: DocumentService = Depends(get_document_service)
):
    """CU6: Consultar Catálogo - RF3, RF7 (sin autenticación)"""
    try:
        return await document_service.get_documents(
            skip=skip, limit=limit, tipo=tipo, 
            categoria=categoria, disponible=disponible
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search/")
async def search_documents(
    query: str = Query(..., min_length=1),
    tipo: Optional[DocumentType] = None,
    categoria: Optional[DocumentCategory] = None,
    document_service: DocumentService = Depends(get_document_service)
):
    """CU6: Consultar Catálogo - RF7 - Búsqueda avanzada"""
    try:
        documents = await document_service.search_documents(query, tipo, categoria)
        return documents
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: str,
    document_service: DocumentService = Depends(get_document_service)
):
    """Obtener documento por ID"""
    try:
        document = await document_service.get_document(document_id)
        if not document:
            raise HTTPException(status_code=404, detail="Documento no encontrado")
        return document
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{document_id}", response_model=DocumentResponse)
async def update_document(
    document_id: str,
    document_update: DocumentUpdate,
    document_service: DocumentService = Depends(get_document_service),
    current_user = Depends(require_roles([UserRole.ADMIN, UserRole.LIBRARIAN]))
):
    """Actualizar documento"""
    try:
        updated_document = await document_service.update_document(document_id, document_update)
        if not updated_document:
            raise HTTPException(status_code=404, detail="Documento no encontrado")
        return updated_document
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{document_id}/ejemplares")
async def add_ejemplar(
    document_id: str,
    document_service: DocumentService = Depends(get_document_service),
    current_user = Depends(require_roles([UserRole.ADMIN, UserRole.LIBRARIAN]))
):
    """Agregar un nuevo ejemplar a un documento"""
    try:
        success = await document_service.add_ejemplar(document_id)
        if not success:
            raise HTTPException(status_code=404, detail="Documento no encontrado")
        return {"message": "Ejemplar agregado exitosamente"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{document_id}/ejemplares", response_model=List[EjemplarResponse])
async def get_document_ejemplares(
    document_id: str,
    document_service: DocumentService = Depends(get_document_service)
):
    """Obtener todos los ejemplares de un documento"""
    try:
        ejemplares = await document_service.get_document_ejemplares(document_id)
        return ejemplares
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{document_id}/ejemplares/disponibles", response_model=List[EjemplarResponse])
async def get_available_ejemplares(
    document_id: str,
    document_service: DocumentService = Depends(get_document_service)
):
    """Obtener ejemplares disponibles de un documento"""
    try:
        ejemplares = await document_service.get_available_ejemplares(document_id)
        return ejemplares
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats/overview")
async def get_document_stats(
    document_service: DocumentService = Depends(get_document_service),
    current_user = Depends(require_roles([UserRole.ADMIN, UserRole.LIBRARIAN]))
):
    """Obtener estadísticas de documentos"""
    try:
        stats = await document_service.get_document_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
