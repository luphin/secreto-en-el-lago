"""
Dependencias compartidas para los endpoints de la API
"""
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.database import get_database
from app.core.security import decode_token
from app.services.user_service import UserService
from app.models.user import UserRole

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Obtiene el usuario actual desde el token JWT"""
    token = credentials.credentials
    payload = decode_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )
    
    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tipo de token inválido"
        )
    
    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )
    
    # Obtener usuario de la base de datos
    db = get_database()
    user_service = UserService(db)
    user = await user_service.get_user_by_id(user_id)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado"
        )
    
    if not user.get("activo"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cuenta no activada"
        )
    
    return user


async def get_current_active_user(
    current_user: dict = Depends(get_current_user)
):
    """Verifica que el usuario actual esté activo"""
    if not current_user.get("activo"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    return current_user


def require_role(allowed_roles: list[UserRole]):
    """Factory de dependencia que requiere roles específicos"""
    async def role_checker(current_user: dict = Depends(get_current_user)):
        user_role = current_user.get("rol")
        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tiene permisos para realizar esta acción"
            )
        return current_user
    return role_checker


# Dependencias específicas por rol
async def get_bibliotecario_user(
    current_user: dict = Depends(
        require_role([UserRole.BIBLIOTECARIO, UserRole.ADMINISTRATIVO])
    )
):
    """Requiere rol de bibliotecario o administrativo"""
    return current_user


async def get_administrativo_user(
    current_user: dict = Depends(require_role([UserRole.ADMINISTRATIVO]))
):
    """Requiere rol de administrativo"""
    return current_user

