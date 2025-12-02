"""
Endpoints de gestión de reservas
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query

from app.core.database import get_database
from app.models.reservation import ReservationCreate, ReservationResponse, ReservationStatus
from app.services.reservation_service import ReservationService
from app.api.dependencies import get_current_user, get_bibliotecario_user

router = APIRouter()


@router.post("/", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED)
async def create_reservation(
    reservation: ReservationCreate,
    db=Depends(get_database),
    current_user: dict = Depends(get_current_user)
):
    """
    Crea una nueva reserva.
    Los usuarios pueden crear reservas para sí mismos.
    """
    from app.models.user import UserRole
    
    # Si no es staff, solo puede crear reservas para sí mismo
    if current_user["rol"] not in [UserRole.BIBLIOTECARIO, UserRole.ADMINISTRATIVO]:
        reservation.user_id = str(current_user["_id"])
    
    reservation_service = ReservationService(db)
    new_reservation = await reservation_service.create_reservation(reservation)
    
    if not new_reservation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede crear la reserva. Verifique que el documento exista y no tenga otra reserva activa."
        )
    
    return ReservationResponse(
        _id=str(new_reservation["_id"]),
        document_id=new_reservation["document_id"],
        user_id=new_reservation["user_id"],
        fecha_reserva=new_reservation["fecha_reserva"],
        fecha_creacion=new_reservation["fecha_creacion"],
        estado=new_reservation["estado"]
    )


@router.get("/", response_model=List[ReservationResponse])
async def list_reservations(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    user_id: Optional[str] = None,
    document_id: Optional[str] = None,
    estado: Optional[ReservationStatus] = None,
    db=Depends(get_database),
    current_user: dict = Depends(get_current_user)
):
    """
    Lista reservas.
    Los usuarios pueden ver sus propias reservas.
    El personal puede ver todas las reservas.
    """
    from app.models.user import UserRole
    from bson import ObjectId
    
    # Si no es staff, solo puede ver sus propias reservas
    if current_user["rol"] not in [UserRole.BIBLIOTECARIO, UserRole.ADMINISTRATIVO]:
        user_id = str(current_user["_id"])
    
    reservation_service = ReservationService(db)
    reservations = await reservation_service.get_reservations(
        skip=skip,
        limit=limit,
        user_id=user_id,
        document_id=document_id,
        estado=estado
    )
    
    # Enriquecer con información del documento
    enriched_reservations = []
    for res in reservations:
        # Obtener información del documento
        document = await db.documents.find_one({"_id": ObjectId(res["document_id"])})
        
        enriched_reservations.append(
            ReservationResponse(
                _id=str(res["_id"]),
                document_id=res["document_id"],
                user_id=res["user_id"],
                fecha_reserva=res["fecha_reserva"],
                fecha_creacion=res["fecha_creacion"],
                estado=res["estado"],
                document_titulo=document["titulo"] if document else None,
                document_id_fisico=document["id_fisico"] if document else None
            )
        )
    
    return enriched_reservations


@router.get("/{reservation_id}", response_model=ReservationResponse)
async def get_reservation(
    reservation_id: str,
    db=Depends(get_database),
    current_user: dict = Depends(get_current_user)
):
    """
    Obtiene una reserva específica por su ID.
    """
    from app.models.user import UserRole
    
    reservation_service = ReservationService(db)
    reservation = await reservation_service.get_reservation_by_id(reservation_id)
    
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reserva no encontrada"
        )
    
    # Verificar permisos
    is_staff = current_user["rol"] in [UserRole.BIBLIOTECARIO, UserRole.ADMINISTRATIVO]
    is_own_reservation = reservation["user_id"] == str(current_user["_id"])
    
    if not is_staff and not is_own_reservation:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para ver esta reserva"
        )
    
    return ReservationResponse(
        _id=str(reservation["_id"]),
        document_id=reservation["document_id"],
        user_id=reservation["user_id"],
        fecha_reserva=reservation["fecha_reserva"],
        fecha_creacion=reservation["fecha_creacion"],
        estado=reservation["estado"]
    )


@router.post("/{reservation_id}/cancel", response_model=ReservationResponse)
async def cancel_reservation(
    reservation_id: str,
    db=Depends(get_database),
    current_user: dict = Depends(get_current_user)
):
    """
    Cancela una reserva.
    Los usuarios pueden cancelar sus propias reservas.
    """
    from app.models.user import UserRole
    
    reservation_service = ReservationService(db)
    reservation = await reservation_service.get_reservation_by_id(reservation_id)
    
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reserva no encontrada"
        )
    
    # Verificar permisos
    is_staff = current_user["rol"] in [UserRole.BIBLIOTECARIO, UserRole.ADMINISTRATIVO]
    is_own_reservation = reservation["user_id"] == str(current_user["_id"])
    
    if not is_staff and not is_own_reservation:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para cancelar esta reserva"
        )
    
    cancelled_reservation = await reservation_service.cancel_reservation(reservation_id)
    
    return ReservationResponse(
        _id=str(cancelled_reservation["_id"]),
        document_id=cancelled_reservation["document_id"],
        user_id=cancelled_reservation["user_id"],
        fecha_reserva=cancelled_reservation["fecha_reserva"],
        fecha_creacion=cancelled_reservation["fecha_creacion"],
        estado=cancelled_reservation["estado"]
    )


@router.post("/{reservation_id}/complete", response_model=ReservationResponse)
async def complete_reservation(
    reservation_id: str,
    db=Depends(get_database),
    current_user: dict = Depends(get_bibliotecario_user)
):
    """
    Marca una reserva como completada.
    Requiere rol de bibliotecario o administrativo.
    """
    reservation_service = ReservationService(db)
    completed_reservation = await reservation_service.complete_reservation(reservation_id)
    
    if not completed_reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reserva no encontrada"
        )
    
    return ReservationResponse(
        _id=str(completed_reservation["_id"]),
        document_id=completed_reservation["document_id"],
        user_id=completed_reservation["user_id"],
        fecha_reserva=completed_reservation["fecha_reserva"],
        fecha_creacion=completed_reservation["fecha_creacion"],
        estado=completed_reservation["estado"]
    )

