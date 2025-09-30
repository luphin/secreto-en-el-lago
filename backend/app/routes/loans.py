from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from app.services.loan_service import LoanService
from app.schemas.loan import LoanCreate, LoanResponse, LoanType
from app.middleware.auth import get_current_user, require_roles

router = APIRouter()

@router.post("/", response_model=LoanResponse, status_code=201)
async def create_loan(
    loan_data: LoanCreate,
    loan_service: LoanService = Depends(),
    current_user = Depends(require_roles([UserRole.LIBRARIAN]))
):
    """CU10: Registrar Préstamo - RF11, RF8"""
    try:
        return await loan_service.create_loan(loan_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{loan_id}", response_model=LoanResponse)
async def get_loan(
    loan_id: str,
    loan_service: LoanService = Depends(),
    current_user = Depends(require_roles([UserRole.ADMIN, UserRole.LIBRARIAN]))
):
    """Obtener préstamo por ID"""
    try:
        loan = await loan_service.get_loan(loan_id)
        if not loan:
            raise HTTPException(status_code=404, detail="Préstamo no encontrado")
        return loan
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{loan_id}/devolver")
async def return_loan_items(
    loan_id: str,
    ejemplares_ids: List[str],
    loan_service: LoanService = Depends(),
    current_user = Depends(require_roles([UserRole.LIBRARIAN]))
):
    """CU15: Ingresar Devolución - RF15"""
    try:
        success = await loan_service.return_loan_items(loan_id, ejemplares_ids)
        if not success:
            raise HTTPException(status_code=400, detail="No se pudieron devolver los items")
        return {"message": "Items devueltos exitosamente"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/usuario/{usuario_id}", response_model=List[LoanResponse])
async def get_user_loans(
    usuario_id: str,
    activos: bool = Query(True),
    loan_service: LoanService = Depends(),
    current_user = Depends(require_roles([UserRole.ADMIN, UserRole.LIBRARIAN]))
):
    """Obtener préstamos de un usuario"""
    try:
        loans = await loan_service.get_user_loans(usuario_id, activos)
        return loans
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/vencidos/", response_model=List[LoanResponse])
async def get_overdue_loans(
    loan_service: LoanService = Depends(),
    current_user = Depends(require_roles([UserRole.ADMIN, UserRole.LIBRARIAN]))
):
    """CU13: Revisar Préstamos Vencidos - RF14"""
    try:
        loans = await loan_service.get_overdue_loans()
        return loans
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{loan_id}/extender")
async def extend_loan(
    loan_id: str,
    dias_extension: int = Query(7, ge=1, le=30),
    loan_service: LoanService = Depends(),
    current_user = Depends(require_roles([UserRole.LIBRARIAN]))
):
    """Extender préstamo por días adicionales"""
    try:
        success = await loan_service.extend_loan(loan_id, dias_extension)
        if not success:
            raise HTTPException(status_code=404, detail="Préstamo no encontrado")
        return {"message": f"Préstamo extendido por {dias_extension} días"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sala/vencidos", response_model=List[LoanResponse])
async def get_overdue_sala_loans(
    loan_service: LoanService = Depends(),
    current_user = Depends(require_roles([UserRole.ADMINISTRATIVE]))
):
    """CU12: Revisar Préstamos Sala Vencidos - RF13"""
    try:
        # Filtrar solo préstamos en sala vencidos
        all_overdue = await loan_service.get_overdue_loans()
        sala_overdue = [loan for loan in all_overdue if loan.tipo_prestamo == LoanType.SALA]
        return sala_overdue
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
