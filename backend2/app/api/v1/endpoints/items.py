"""
Endpoints de gestión de ejemplares (items)
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query

from app.core.database import get_database
from app.models.item import ItemCreate, ItemUpdate, ItemResponse, ItemStatus
from app.services.item_service import ItemService
from app.api.dependencies import get_bibliotecario_user, get_current_user

router = APIRouter()


@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(
    item: ItemCreate,
    db=Depends(get_database),
    current_user: dict = Depends(get_bibliotecario_user)
):
    """
    Crea un nuevo ejemplar.
    Requiere rol de bibliotecario o administrativo.
    """
    item_service = ItemService(db)
    new_item = await item_service.create_item(item)
    
    return ItemResponse(
        _id=str(new_item["_id"]),
        document_id=new_item["document_id"],
        ubicacion=new_item["ubicacion"],
        estado=new_item["estado"]
    )


@router.get("/", response_model=List[ItemResponse])
async def list_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    document_id: Optional[str] = None,
    estado: Optional[ItemStatus] = None,
    db=Depends(get_database)
):
    """
    Lista ejemplares con filtros opcionales.
    Acceso público para consultar disponibilidad.
    """
    item_service = ItemService(db)
    items = await item_service.get_items(
        skip=skip,
        limit=limit,
        document_id=document_id,
        estado=estado
    )
    
    return [
        ItemResponse(
            _id=str(item["_id"]),
            document_id=item["document_id"],
            ubicacion=item["ubicacion"],
            estado=item["estado"]
        )
        for item in items
    ]


@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(item_id: str, db=Depends(get_database)):
    """
    Obtiene un ejemplar específico por su ID.
    """
    item_service = ItemService(db)
    item = await item_service.get_item_by_id(item_id)
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ejemplar no encontrado"
        )
    
    return ItemResponse(
        _id=str(item["_id"]),
        document_id=item["document_id"],
        ubicacion=item["ubicacion"],
        estado=item["estado"]
    )


@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: str,
    item_update: ItemUpdate,
    db=Depends(get_database),
    current_user: dict = Depends(get_bibliotecario_user)
):
    """
    Actualiza un ejemplar.
    Requiere rol de bibliotecario o administrativo.
    """
    item_service = ItemService(db)
    updated_item = await item_service.update_item(item_id, item_update)
    
    if not updated_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ejemplar no encontrado"
        )
    
    return ItemResponse(
        _id=str(updated_item["_id"]),
        document_id=updated_item["document_id"],
        ubicacion=updated_item["ubicacion"],
        estado=updated_item["estado"]
    )


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: str,
    db=Depends(get_database),
    current_user: dict = Depends(get_bibliotecario_user)
):
    """
    Elimina un ejemplar.
    Requiere rol de bibliotecario o administrativo.
    """
    item_service = ItemService(db)
    deleted = await item_service.delete_item(item_id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ejemplar no encontrado"
        )
    
    return None

