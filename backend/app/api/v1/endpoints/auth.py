"""
Endpoints de autenticación
"""
from fastapi import APIRouter, Depends, HTTPException, status
from app.core.database import get_database
from app.core.security import create_access_token, create_refresh_token
from app.models.user import UserLogin, Token, UserCreate, UserResponse
from app.services.user_service import UserService

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db=Depends(get_database)):
    """
    Registra un nuevo usuario en el sistema.
    La cuenta se crea inactiva y requiere activación.
    """
    user_service = UserService(db)
    
    # Verificar si el email ya existe
    existing_user = await user_service.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    # Verificar si el RUT ya existe
    existing_rut = await user_service.get_user_by_rut(user.rut)
    if existing_rut:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El RUT ya está registrado"
        )
    
    # Crear usuario
    new_user = await user_service.create_user(user)
    
    # Enviar email de activación a través de Kafka
    from app.core.kafka_producer import kafka_producer
    activation_link = f"http://localhost:8000/api/v1/auth/activate/{new_user['_id']}"
    await kafka_producer.send_activation_email(
        user_email=new_user["email"],
        user_name=f"{new_user['nombres']} {new_user['apellidos']}",
        activation_link=activation_link
    )
    
    return UserResponse(
        _id=str(new_user["_id"]),
        rut=new_user["rut"],
        nombres=new_user["nombres"],
        apellidos=new_user["apellidos"],
        direccion=new_user["direccion"],
        telefono=new_user["telefono"],
        email=new_user["email"],
        rol=new_user["rol"],
        activo=new_user["activo"],
        fecha_creacion=new_user["fecha_creacion"],
        foto_url=new_user.get("foto_url"),
        huella_ref=new_user.get("huella_ref"),
        sancion_hasta=new_user.get("sancion_hasta")
    )


@router.post("/login", response_model=Token)
async def login(user_login: UserLogin, db=Depends(get_database)):
    """
    Autentica un usuario y retorna tokens de acceso y refresco.
    """
    user_service = UserService(db)
    
    # Autenticar usuario
    user = await user_service.authenticate_user(user_login.email, user_login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos"
        )
    
    if not user.get("activo"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cuenta no activada. Por favor revise su email."
        )
    
    # Crear tokens
    access_token = create_access_token(
        data={"user_id": str(user["_id"]), "email": user["email"]}
    )
    refresh_token = create_refresh_token(
        data={"user_id": str(user["_id"]), "email": user["email"]}
    )
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.post("/activate/{user_id}", response_model=dict)
async def activate_account(user_id: str, db=Depends(get_database)):
    """
    Activa la cuenta de un usuario.
    En producción, esto debería requerir un token de activación enviado por email.
    """
    user_service = UserService(db)
    
    user = await user_service.activate_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    return {"message": "Cuenta activada exitosamente"}

