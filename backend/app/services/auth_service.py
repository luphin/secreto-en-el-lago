from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import jwt
from passlib.context import CryptContext
from motor.motor_asyncio import AsyncIOMotorDatabase
import uuid
import structlog

from app.config.settings import settings
from app.config.database import get_database
from app.models.user import UserCreate, UserInDB, UserResponse, UserStatus, UserRole
from app.services.email_service import EmailService
from app.services.kafka_service import KafkaService

logger = structlog.get_logger()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, db: AsyncIOMotorDatabase = None):
        self.db = db or get_database()
        self.email_service = EmailService()
        self.kafka_service = KafkaService()
        self.collection = self.db.users

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.jwt_expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
        return encoded_jwt

    def create_verification_token(self, email: str) -> str:
        expire = datetime.utcnow() + timedelta(hours=24)
        to_encode = {"email": email, "exp": expire, "type": "verification"}
        token = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
        return token

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        try:
            payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
            return payload
        except jwt.JWTError:
            return None

    async def register_user(self, user_data: UserCreate) -> UserInDB:
        # Verificar si el usuario ya existe
        existing_user = await self.collection.find_one({
            "$or": [
                {"email": user_data.email},
                {"rut": user_data.rut}
            ]
        })
        
        if existing_user:
            raise ValueError("El usuario ya existe con ese email o RUT")

        # Crear usuario
        user_id = str(uuid.uuid4())
        hashed_password = self.get_password_hash(user_data.password)
        
        user_dict = {
            "id": user_id,
            "rut": user_data.rut,
            "names": user_data.names,
            "last_names": user_data.last_names,
            "email": user_data.email,
            "phone": user_data.phone,
            "address": user_data.address,
            "role": user_data.role.value,
            "hashed_password": hashed_password,
            "fingerprint_data": user_data.fingerprint_data,
            "photo_data": user_data.photo_data,
            "status": UserStatus.PENDING.value,
            "email_verified": False,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        # Insertar en la base de datos
        await self.collection.insert_one(user_dict)
        
        # Crear token de verificación
        verification_token = self.create_verification_token(user_data.email)
        
        # Enviar email de verificación
        await self.email_service.send_verification_email(user_data.email, verification_token)
        
        # Log via Kafka
        await self.kafka_service.send_user_registered_event(user_id, user_data.email)
        
        logger.info("Usuario registrado exitosamente", user_id=user_id, email=user_data.email)
        
        return UserInDB(**user_dict)

    async def authenticate_user(self, email: str, password: str) -> Dict[str, str]:
        user = await self.collection.find_one({"email": email})
        
        if not user:
            raise ValueError("Credenciales inválidas")
        
        if not self.verify_password(password, user["hashed_password"]):
            raise ValueError("Credenciales inválidas")
        
        if user["status"] != UserStatus.ACTIVE.value:
            raise ValueError("La cuenta no está activa")
        
        if not user["email_verified"]:
            raise ValueError("El email no ha sido verificado")

        # Crear tokens
        access_token = self.create_access_token(data={"sub": user["email"], "user_id": user["id"]})
        refresh_token = self.create_access_token(
            data={"sub": user["email"], "type": "refresh"}, 
            expires_delta=timedelta(days=7)
        )

        # Actualizar última conexión
        await self.collection.update_one(
            {"id": user["id"]},
            {"$set": {"updated_at": datetime.utcnow()}}
        )

        logger.info("Usuario autenticado", user_id=user["id"], email=email)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    async def verify_email(self, token: str) -> bool:
        payload = self.verify_token(token)
        if not payload or payload.get("type") != "verification":
            raise ValueError("Token de verificación inválido")
        
        email = payload.get("email")
        if not email:
            raise ValueError("Token de verificación inválido")

        result = await self.collection.update_one(
            {"email": email},
            {
                "$set": {
                    "email_verified": True,
                    "status": UserStatus.ACTIVE.value,
                    "updated_at": datetime.utcnow()
                }
            }
        )

        if result.modified_count == 0:
            raise ValueError("No se pudo verificar el email")

        # Enviar email de bienvenida
        await self.email_service.send_welcome_email(email)
        
        logger.info("Email verificado exitosamente", email=email)
        return True

    async def refresh_token(self, refresh_token: str) -> Dict[str, str]:
        payload = self.verify_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise ValueError("Token de refresh inválido")
        
        email = payload.get("sub")
        user = await self.collection.find_one({"email": email})
        
        if not user:
            raise ValueError("Usuario no encontrado")
        
        # Crear nuevo access token
        access_token = self.create_access_token(data={"sub": user["email"], "user_id": user["id"]})
        
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    async def get_user_by_email(self, email: str) -> Optional[UserInDB]:
        user = await self.collection.find_one({"email": email})
        if user:
            return UserInDB(**user)
        return None

    async def get_user_by_id(self, user_id: str) -> Optional[UserInDB]:
        user = await self.collection.find_one({"id": user_id})
        if user:
            return UserInDB(**user)
        return None
