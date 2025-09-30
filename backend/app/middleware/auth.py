from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from app.config.settings import settings
from app.services.auth_service import AuthService
from app.schemas.user import UserResponse, UserRole

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends()
) -> UserResponse:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token = credentials.credentials
        payload = auth_service.verify_token(token)
        if payload is None:
            raise credentials_exception
        
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        
        user = await auth_service.get_user_by_email(email)
        if user is None:
            raise credentials_exception
        
        return UserResponse(**user.dict())
    
    except JWTError:
        raise credentials_exception

def require_roles(allowed_roles: list[UserRole]):
    """Dependency para verificar roles de usuario"""
    def role_checker(current_user: UserResponse = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tiene permisos para realizar esta acción"
            )
        return current_user
    return role_checker

# Dependencies específicas por rol
require_admin = require_roles([UserRole.ADMIN])
require_librarian = require_roles([UserRole.LIBRARIAN])
require_administrative = require_roles([UserRole.ADMINISTRATIVE])
require_staff = require_roles([UserRole.ADMIN, UserRole.LIBRARIAN, UserRole.ADMINISTRATIVE])
