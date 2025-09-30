from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.services.user_service import UserService
from app.schemas.user import UserResponse, UserUpdate, UserStatus, UserRole
from app.middleware.auth import get_current_user, require_roles

router = APIRouter()

def get_user_service() -> UserService:
    """Dependency para obtener una instancia de UserService"""
    return UserService()

@router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[UserStatus] = None,
    role: Optional[UserRole] = None,
    user_service: UserService = Depends(get_user_service),
    current_user: UserResponse = Depends(require_roles([UserRole.ADMIN, UserRole.LIBRARIAN]))
):
    """Obtener lista de usuarios (solo administradores y bibliotecarios)"""
    try:
        return await user_service.get_users(skip=skip, limit=limit, status=status, role=role)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    user_service: UserService = Depends(get_user_service),
    current_user: UserResponse = Depends(require_roles([UserRole.ADMIN, UserRole.LIBRARIAN]))
):
    """Obtener usuario por ID"""
    try:
        user = await user_service.get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_update: UserUpdate,
    user_service: UserService = Depends(get_user_service),
    current_user: UserResponse = Depends(require_roles([UserRole.ADMIN, UserRole.LIBRARIAN]))
):
    """Actualizar información de usuario"""
    try:
        updated_user = await user_service.update_user(user_id, user_update)
        if not updated_user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return updated_user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{user_id}/status")
async def update_user_status(
    user_id: str,
    status: UserStatus,
    user_service: UserService = Depends(get_user_service),
    current_user: UserResponse = Depends(require_roles([UserRole.ADMIN]))
):
    """Actualizar estado de usuario (solo admin)"""
    try:
        success = await user_service.update_user_status(user_id, status)
        if not success:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return {"message": f"Estado del usuario actualizado a {status.value}"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{user_id}/suspend")
async def suspend_user(
    user_id: str,
    days: int = Query(7, ge=1, le=365),
    user_service: UserService = Depends(get_user_service),
    current_user: UserResponse = Depends(require_roles([UserRole.ADMIN]))
):
    """Suspender usuario por días específicos"""
    try:
        success = await user_service.suspend_user(user_id, days)
        if not success:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return {"message": f"Usuario suspendido por {days} días"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search/{query}")
async def search_users(
    query: str,
    user_service: UserService = Depends(get_user_service),
    current_user: UserResponse = Depends(require_roles([UserRole.ADMIN, UserRole.LIBRARIAN]))
):
    """Buscar usuarios por nombre, email o RUT"""
    try:
        users = await user_service.search_users(query)
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/with-active-loans/")
async def get_users_with_active_loans(
    user_service: UserService = Depends(get_user_service),
    current_user: UserResponse = Depends(require_roles([UserRole.ADMIN, UserRole.LIBRARIAN]))
):
    """Obtener usuarios con préstamos activos"""
    try:
        users = await user_service.get_users_with_active_loans()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
