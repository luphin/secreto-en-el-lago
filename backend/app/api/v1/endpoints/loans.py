"""
Endpoints de gestión de préstamos
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query

from app.core.database import get_database
from app.models.loan import LoanCreate, LoanResponse, LoanStatus, LoanReturn
from app.services.loan_service import LoanService
from app.api.dependencies import get_current_user, get_bibliotecario_user

router = APIRouter()


@router.post("/", response_model=LoanResponse, status_code=status.HTTP_201_CREATED)
async def create_loan(
    loan: LoanCreate,
    db=Depends(get_database),
    current_user: dict = Depends(get_bibliotecario_user)
):
    """
    Registra un nuevo préstamo.
    Requiere rol de bibliotecario o administrativo.
    """
    loan_service = LoanService(db)
    new_loan = await loan_service.create_loan(loan)
    
    if not new_loan:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede crear el préstamo. Verifique que el ejemplar esté disponible y el usuario no esté sancionado."
        )
    
    return LoanResponse(
        _id=str(new_loan["_id"]),
        item_id=new_loan["item_id"],
        user_id=new_loan["user_id"],
        tipo_prestamo=new_loan["tipo_prestamo"],
        fecha_prestamo=new_loan["fecha_prestamo"],
        fecha_devolucion_pactada=new_loan["fecha_devolucion_pactada"],
        fecha_devolucion_real=new_loan.get("fecha_devolucion_real"),
        estado=new_loan["estado"]
    )


@router.get("/", response_model=List[LoanResponse])
async def list_loans(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    user_id: Optional[str] = None,
    estado: Optional[LoanStatus] = None,
    db=Depends(get_database),
    current_user: dict = Depends(get_current_user)
):
    """
    Lista préstamos.
    Los usuarios pueden ver sus propios préstamos.
    El personal puede ver todos los préstamos.
    """
    from app.models.user import UserRole
    from bson import ObjectId
    
    # Si no es staff, solo puede ver sus propios préstamos
    if current_user["rol"] not in [UserRole.BIBLIOTECARIO, UserRole.ADMINISTRATIVO]:
        user_id = str(current_user["_id"])
    
    loan_service = LoanService(db)
    loans = await loan_service.get_loans(
        skip=skip,
        limit=limit,
        user_id=user_id,
        estado=estado
    )
    
    # Enriquecer con información del documento
    enriched_loans = []
    for loan in loans:
        # Obtener el item para luego obtener el documento
        item = await db.items.find_one({"_id": ObjectId(loan["item_id"])})
        document_titulo = None
        document_id_fisico = None
        
        if item:
            document_id = item["document_id"]
            # El document_id puede ser un ObjectId o un ID físico (string)
            try:
                document = await db.documents.find_one({"_id": ObjectId(document_id)})
            except:
                document = await db.documents.find_one({"id_fisico": document_id})
            
            if document:
                document_titulo = document["titulo"]
                document_id_fisico = document["id_fisico"]
        
        enriched_loans.append(
            LoanResponse(
                _id=str(loan["_id"]),
                item_id=loan["item_id"],
                user_id=loan["user_id"],
                tipo_prestamo=loan["tipo_prestamo"],
                fecha_prestamo=loan["fecha_prestamo"],
                fecha_devolucion_pactada=loan["fecha_devolucion_pactada"],
                fecha_devolucion_real=loan.get("fecha_devolucion_real"),
                estado=loan["estado"],
                document_titulo=document_titulo,
                document_id_fisico=document_id_fisico
            )
        )
    
    return enriched_loans


@router.get("/overdue", response_model=List[LoanResponse])
async def list_overdue_loans(
    db=Depends(get_database),
    current_user: dict = Depends(get_bibliotecario_user)
):
    """
    Lista préstamos vencidos.
    Requiere rol de bibliotecario o administrativo.
    """
    loan_service = LoanService(db)
    loans = await loan_service.get_overdue_loans()
    
    return [
        LoanResponse(
            _id=str(loan["_id"]),
            item_id=loan["item_id"],
            user_id=loan["user_id"],
            tipo_prestamo=loan["tipo_prestamo"],
            fecha_prestamo=loan["fecha_prestamo"],
            fecha_devolucion_pactada=loan["fecha_devolucion_pactada"],
            fecha_devolucion_real=loan.get("fecha_devolucion_real"),
            estado=loan["estado"]
        )
        for loan in loans
    ]


@router.get("/{loan_id}", response_model=LoanResponse)
async def get_loan(
    loan_id: str,
    db=Depends(get_database),
    current_user: dict = Depends(get_current_user)
):
    """
    Obtiene un préstamo específico por su ID.
    """
    from app.models.user import UserRole
    
    loan_service = LoanService(db)
    loan = await loan_service.get_loan_by_id(loan_id)
    
    if not loan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Préstamo no encontrado"
        )
    
    # Verificar permisos
    is_staff = current_user["rol"] in [UserRole.BIBLIOTECARIO, UserRole.ADMINISTRATIVO]
    is_own_loan = loan["user_id"] == str(current_user["_id"])
    
    if not is_staff and not is_own_loan:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para ver este préstamo"
        )
    
    return LoanResponse(
        _id=str(loan["_id"]),
        item_id=loan["item_id"],
        user_id=loan["user_id"],
        tipo_prestamo=loan["tipo_prestamo"],
        fecha_prestamo=loan["fecha_prestamo"],
        fecha_devolucion_pactada=loan["fecha_devolucion_pactada"],
        fecha_devolucion_real=loan.get("fecha_devolucion_real"),
        estado=loan["estado"]
    )


@router.post("/{loan_id}/return", response_model=LoanResponse)
async def return_loan(
    loan_id: str,
    db=Depends(get_database),
    current_user: dict = Depends(get_bibliotecario_user)
):
    """
    Procesa la devolución de un préstamo.
    Requiere rol de bibliotecario o administrativo.
    """
    loan_service = LoanService(db)
    returned_loan = await loan_service.return_loan(loan_id)
    
    if not returned_loan:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede procesar la devolución. Verifique que el préstamo exista y esté activo."
        )
    
    return LoanResponse(
        _id=str(returned_loan["_id"]),
        item_id=returned_loan["item_id"],
        user_id=returned_loan["user_id"],
        tipo_prestamo=returned_loan["tipo_prestamo"],
        fecha_prestamo=returned_loan["fecha_prestamo"],
        fecha_devolucion_pactada=returned_loan["fecha_devolucion_pactada"],
        fecha_devolucion_real=returned_loan.get("fecha_devolucion_real"),
        estado=returned_loan["estado"]
    )

