"""
Modelos de usuario
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId
from enum import Enum


class PyObjectId(ObjectId):
    """Validador personalizado para ObjectId de MongoDB"""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")


class UserRole(str, Enum):
    """Roles de usuario"""
    LECTOR = "lector"
    BIBLIOTECARIO = "bibliotecario"
    ADMINISTRATIVO = "administrativo"


class UserBase(BaseModel):
    """Esquema base de usuario"""
    rut: str = Field(..., description="RUT del usuario sin puntos con guión")
    nombres: str = Field(..., min_length=1)
    apellidos: str = Field(..., min_length=1)
    direccion: str
    telefono: str
    email: EmailStr
    rol: UserRole = UserRole.LECTOR


class UserCreate(UserBase):
    """Esquema para crear usuario"""
    password: str = Field(..., min_length=6)
    foto_url: Optional[str] = None
    huella_ref: Optional[str] = None


class UserUpdate(BaseModel):
    """Esquema para actualizar usuario"""
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    foto_url: Optional[str] = None
    huella_ref: Optional[str] = None
    activo: Optional[bool] = None
    sancion_hasta: Optional[datetime] = None


class UserInDB(UserBase):
    """Esquema de usuario en base de datos"""
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    password: str
    activo: bool = False
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)
    foto_url: Optional[str] = None
    huella_ref: Optional[str] = None
    sancion_hasta: Optional[datetime] = None

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "rut": "12345678-9",
                "nombres": "Juan",
                "apellidos": "Pérez",
                "direccion": "Calle Principal 123",
                "telefono": "+56912345678",
                "email": "juan.perez@example.com",
                "rol": "lector"
            }
        }


class UserResponse(BaseModel):
    """Esquema de respuesta de usuario (sin contraseña)"""
    id: str = Field(..., alias="_id")
    rut: str
    nombres: str
    apellidos: str
    direccion: str
    telefono: str
    email: EmailStr
    rol: UserRole
    activo: bool
    fecha_creacion: datetime
    foto_url: Optional[str] = None
    huella_ref: Optional[str] = None
    sancion_hasta: Optional[datetime] = None

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "507f1f77bcf86cd799439011",
                "rut": "12345678-9",
                "nombres": "Juan",
                "apellidos": "Pérez",
                "email": "juan.perez@example.com",
                "rol": "lector",
                "activo": True
            }
        }


class UserLogin(BaseModel):
    """Esquema para login"""
    email: EmailStr
    password: str


class Token(BaseModel):
    """Esquema de respuesta de token"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Datos decodificados del token"""
    email: Optional[str] = None
    user_id: Optional[str] = None

