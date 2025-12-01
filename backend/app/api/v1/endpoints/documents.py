"""
Endpoints de gestión de documentos bibliográficos
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query

from app.core.database import get_database
from app.models.document import DocumentCreate, DocumentUpdate, DocumentResponse
from app.services.document_service import DocumentService
from app.api.dependencies import get_bibliotecario_user

router = APIRouter()


@router.post("/", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def create_document(
    document: DocumentCreate,
    db=Depends(get_database),
    current_user: dict = Depends(get_bibliotecario_user)
):
    """
    Crea un nuevo documento en la colección.
    Requiere rol de bibliotecario o administrativo.
    """
    doc_service = DocumentService(db)

    try:
        new_doc = await doc_service.create_document(document)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return DocumentResponse(
        _id=str(new_doc["_id"]),
        id_fisico=new_doc["id_fisico"],
        titulo=new_doc["titulo"],
        autor=new_doc["autor"],
        editorial=new_doc["editorial"],
        edicion=new_doc["edicion"],
        ano_edicion=new_doc["ano_edicion"],
        tipo=new_doc["tipo"],
        categoria=new_doc["categoria"],
        tipo_medio=new_doc.get("tipo_medio"),
        items_disponibles=0
    )


@router.get("/", response_model=List[DocumentResponse])
async def list_documents(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    titulo: Optional[str] = None,
    autor: Optional[str] = None,
    categoria: Optional[str] = None,
    search: Optional[str] = None,
    db=Depends(get_database)
):
    """
    Lista documentos del catálogo con filtros opcionales.
    No requiere autenticación (acceso público al catálogo).
    """
    doc_service = DocumentService(db)
    documents = await doc_service.get_documents(
        skip=skip,
        limit=limit,
        titulo=titulo,
        autor=autor,
        categoria=categoria,
        search=search
    )
    
    return [
        DocumentResponse(
            _id=str(doc["_id"]),
            id_fisico=doc["id_fisico"],
            titulo=doc["titulo"],
            autor=doc["autor"],
            editorial=doc["editorial"],
            edicion=doc["edicion"],
            ano_edicion=doc["ano_edicion"],
            tipo=doc["tipo"],
            categoria=doc["categoria"],
            tipo_medio=doc.get("tipo_medio"),
            items_disponibles=doc.get("items_disponibles", 0)
        )
        for doc in documents
    ]


@router.get("/by-physical-id/{id_fisico}")
async def get_document_id_by_physical_id(id_fisico: str, db=Depends(get_database)):
    """
    Obtiene el ID de un documento por su ID físico.
    No requiere autenticación.
    """
    doc_service = DocumentService(db)
    document = await doc_service.get_document_by_physical_id(id_fisico)

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró un documento con id_fisico: {id_fisico}"
        )

    return {
        "id_fisico": id_fisico,
        "document_id": str(document["_id"])
    }


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(document_id: str, db=Depends(get_database)):
    """
    Obtiene un documento específico por su ID.
    No requiere autenticación.
    """
    doc_service = DocumentService(db)
    document = await doc_service.get_document_by_id(document_id)
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento no encontrado"
        )
    
    # Obtener disponibilidad
    items_disponibles = await doc_service._count_available_items(document_id)

    return DocumentResponse(
        _id=str(document["_id"]),
        id_fisico=document["id_fisico"],
        titulo=document["titulo"],
        autor=document["autor"],
        editorial=document["editorial"],
        edicion=document["edicion"],
        ano_edicion=document["ano_edicion"],
        tipo=document["tipo"],
        categoria=document["categoria"],
        tipo_medio=document.get("tipo_medio"),
        items_disponibles=items_disponibles
    )


@router.put("/{document_id}", response_model=DocumentResponse)
async def update_document(
    document_id: str,
    document_update: DocumentUpdate,
    db=Depends(get_database),
    current_user: dict = Depends(get_bibliotecario_user)
):
    """
    Actualiza un documento.
    Requiere rol de bibliotecario o administrativo.
    """
    doc_service = DocumentService(db)

    try:
        updated_doc = await doc_service.update_document(document_id, document_update)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    if not updated_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento no encontrado"
        )

    items_disponibles = await doc_service._count_available_items(document_id)

    return DocumentResponse(
        _id=str(updated_doc["_id"]),
        id_fisico=updated_doc["id_fisico"],
        titulo=updated_doc["titulo"],
        autor=updated_doc["autor"],
        editorial=updated_doc["editorial"],
        edicion=updated_doc["edicion"],
        ano_edicion=updated_doc["ano_edicion"],
        tipo=updated_doc["tipo"],
        categoria=updated_doc["categoria"],
        tipo_medio=updated_doc.get("tipo_medio"),
        items_disponibles=items_disponibles
    )


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    document_id: str,
    db=Depends(get_database),
    current_user: dict = Depends(get_bibliotecario_user)
):
    """
    Elimina un documento.
    Solo se puede eliminar si no tiene ejemplares asociados.
    Requiere rol de bibliotecario o administrativo.
    """
    doc_service = DocumentService(db)
    deleted = await doc_service.delete_document(document_id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar el documento. Puede que no exista o tenga ejemplares asociados."
        )
    
    return None

