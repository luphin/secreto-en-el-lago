from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.services.auth_service import AuthService
from app.schemas.user import UserCreate, UserResponse
from app.middleware.auth import get_current_user, get_auth_service

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, auth_service: AuthService = Depends(get_auth_service)):
    """CU3: Registrar Ficha Usuario - RF5"""
    try:
        return await auth_service.register_user(user_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service)
):
    """CU1: Autenticar Usuarios - RF1"""
    try:
        return await auth_service.authenticate_user(form_data.username, form_data.password)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.post("/verify-email")
async def verify_email(token: str, auth_service: AuthService = Depends(get_auth_service)):
    """CU5: Activar Cuenta - RF6"""
    try:
        success = await auth_service.verify_email(token)
        if success:
            return {"message": "Email verificado exitosamente"}
        else:
            raise HTTPException(status_code=400, detail="No se pudo verificar el email")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/refresh-token")
async def refresh_token(refresh_token: str, auth_service: AuthService = Depends(get_auth_service)):
    """Refresh token para autenticación"""
    try:
        return await auth_service.refresh_token(refresh_token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: UserResponse = Depends(get_current_user)):
    """Obtener información del usuario actual"""
    return current_user

@router.post("/logout")
async def logout(current_user: UserResponse = Depends(get_current_user)):
    """Cerrar sesión del usuario"""
    # En una implementación real, podrías invalidar el token
    return {"message": "Sesión cerrada exitosamente"}
