from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import datetime
from app.services.request_service import RequestService
from app.schemas.request import RequestCreate, RequestResponse, RequestType
from app.middleware.auth import get_current_user, require_roles

router = APIRouter()

@router.post("/", response_model=RequestResponse, status_code=201)
async def create_request(
    request_data: RequestCreate,
    request_service: RequestService = Depends(),
    current_user = Depends(get_current_user)  # Usuario normal puede crear solicitudes
):
    """CU7: Solicitar Préstamo - RF8 y CU8: Reservar Documento - RF9"""
    try:
        return await request_service.create_request(request_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[RequestResponse])
async def get_requests(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    tipo: Optional[RequestType] = None,
    estado: Optional[str] = None,
    request_service: RequestService = Depends(),
    current_user = Depends(require_roles([UserRole.ADMIN, UserRole.LIBRARIAN]))
):
    """CU9: Revisar Solicitudes Préstamo - RF10"""
    try:
        return await request_service.get_requests(skip=skip, limit=limit, tipo=tipo, estado=estado)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{request_id}", response_model=RequestResponse)
async def get_request(
    request_id: str,
    request_service: RequestService = Depends(),
    current_user = Depends(require_roles([UserRole.ADMIN, UserRole.LIBRARIAN]))
):
    """Obtener solicitud por ID"""
    try:
        request = await request_service.get_request(request_id)
        if not request:
            raise HTTPException(status_code=404, detail="Solicitud no encontrada")
        return request
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{request_id}/procesar")
async def process_request(
    request_id: str,
    request_service: RequestService = Depends(),
    current_user = Depends(require_roles([UserRole.LIBRARIAN]))
):
    """Procesar solicitud (marcar como procesada)"""
    try:
        success = await request_service.process_request(request_id, current_user.id)
        if not success:
            raise HTTPException(status_code=404, detail="Solicitud no encontrada")
        return {"message": "Solicitud procesada exitosamente"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{request_id}/cancelar")
async def cancel_request(
    request_id: str,
    request_service: RequestService = Depends(),
    current_user = Depends(get_current_user)
):
    """Cancelar solicitud (solo el usuario que la creó o admin)"""
    try:
        success = await request_service.cancel_request(request_id, current_user.id)
        if not success:
            raise HTTPException(status_code=404, detail="Solicitud no encontrada o no autorizado")
        return {"message": "Solicitud cancelada exitosamente"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/usuario/{usuario_id}", response_model=List[RequestResponse])
async def get_user_requests(
    usuario_id: str,
    activas: bool = Query(True),
    request_service: RequestService = Depends(),
    current_user = Depends(require_roles([UserRole.ADMIN, UserRole.LIBRARIAN]))
):
    """Obtener solicitudes de un usuario específico"""
    try:
        requests = await request_service.get_user_requests(usuario_id, activas)
        return requests
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/mis-solicitudes/", response_model=List[RequestResponse])
async def get_my_requests(
    activas: bool = Query(True),
    request_service: RequestService = Depends(),
    current_user = Depends(get_current_user)
):
    """Obtener las solicitudes del usuario actual"""
    try:
        requests = await request_service.get_user_requests(current_user.id, activas)
        return requests
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
