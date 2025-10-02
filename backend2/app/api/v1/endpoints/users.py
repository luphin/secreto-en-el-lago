"""
Endpoints de gestión de usuarios
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query

from app.core.database import get_database
from app.models.user import UserResponse, UserUpdate, UserRole
from app.services.user_service import UserService
from app.api.dependencies import get_current_user, get_bibliotecario_user

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """
    Obtiene la información del usuario autenticado actual.
    """
    return UserResponse(
        _id=str(current_user["_id"]),
        rut=current_user["rut"],
        nombres=current_user["nombres"],
        apellidos=current_user["apellidos"],
        direccion=current_user["direccion"],
        telefono=current_user["telefono"],
        email=current_user["email"],
        rol=current_user["rol"],
        activo=current_user["activo"],
        fecha_creacion=current_user["fecha_creacion"],
        foto_url=current_user.get("foto_url"),
        huella_ref=current_user.get("huella_ref"),
        sancion_hasta=current_user.get("sancion_hasta")
    )


@router.get("/", response_model=List[UserResponse])
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    rol: Optional[UserRole] = None,
    db=Depends(get_database),
    current_user: dict = Depends(get_bibliotecario_user)
):
    """
    Lista todos los usuarios (requiere rol de bibliotecario o administrativo).
    """
    user_service = UserService(db)
    users = await user_service.get_users(skip=skip, limit=limit, rol=rol)
    
    return [
        UserResponse(
            _id=str(user["_id"]),
            rut=user["rut"],
            nombres=user["nombres"],
            apellidos=user["apellidos"],
            direccion=user["direccion"],
            telefono=user["telefono"],
            email=user["email"],
            rol=user["rol"],
            activo=user["activo"],
            fecha_creacion=user["fecha_creacion"],
            foto_url=user.get("foto_url"),
            huella_ref=user.get("huella_ref"),
            sancion_hasta=user.get("sancion_hasta")
        )
        for user in users
    ]


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    db=Depends(get_database),
    current_user: dict = Depends(get_bibliotecario_user)
):
    """
    Obtiene un usuario por su ID (requiere rol de bibliotecario o administrativo).
    """
    user_service = UserService(db)
    user = await user_service.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    return UserResponse(
        _id=str(user["_id"]),
        rut=user["rut"],
        nombres=user["nombres"],
        apellidos=user["apellidos"],
        direccion=user["direccion"],
        telefono=user["telefono"],
        email=user["email"],
        rol=user["rol"],
        activo=user["activo"],
        fecha_creacion=user["fecha_creacion"],
        foto_url=user.get("foto_url"),
        huella_ref=user.get("huella_ref"),
        sancion_hasta=user.get("sancion_hasta")
    )


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_update: UserUpdate,
    db=Depends(get_database),
    current_user: dict = Depends(get_current_user)
):
    """
    Actualiza un usuario. Los usuarios pueden actualizar su propia información.
    El personal puede actualizar cualquier usuario.
    """
    # Verificar permisos
    is_staff = current_user["rol"] in [UserRole.BIBLIOTECARIO, UserRole.ADMINISTRATIVO]
    is_own_profile = str(current_user["_id"]) == user_id
    
    if not is_staff and not is_own_profile:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para actualizar este usuario"
        )
    
    user_service = UserService(db)
    updated_user = await user_service.update_user(user_id, user_update)
    
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    return UserResponse(
        _id=str(updated_user["_id"]),
        rut=updated_user["rut"],
        nombres=updated_user["nombres"],
        apellidos=updated_user["apellidos"],
        direccion=updated_user["direccion"],
        telefono=updated_user["telefono"],
        email=updated_user["email"],
        rol=updated_user["rol"],
        activo=updated_user["activo"],
        fecha_creacion=updated_user["fecha_creacion"],
        foto_url=updated_user.get("foto_url"),
        huella_ref=updated_user.get("huella_ref"),
        sancion_hasta=updated_user.get("sancion_hasta")
    )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    db=Depends(get_database),
    current_user: dict = Depends(get_bibliotecario_user)
):
    """
    Elimina un usuario (requiere rol de bibliotecario o administrativo).
    """
    user_service = UserService(db)
    deleted = await user_service.delete_user(user_id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    return None

