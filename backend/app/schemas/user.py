from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    LIBRARIAN = "librarian"
    ADMINISTRATIVE = "administrative"
    USER = "user"

class UserStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspendido"

class UserBase(BaseModel):
    rut: str = Field(..., min_length=9, max_length=12, description="RUT del usuario")
    names: str = Field(..., min_length=1, max_length=100, description="Nombres del usuario")
    last_names: str = Field(..., min_length=1, max_length=100, description="Apellidos del usuario")
    email: EmailStr = Field(..., description="Email del usuario")
    phone: str = Field(..., min_length=8, max_length=15, description="Teléfono del usuario")
    address: str = Field(..., min_length=1, max_length=200, description="Dirección del usuario")
    role: UserRole = Field(default=UserRole.USER, description="Rol del usuario")

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=100, description="Contraseña del usuario")
    fingerprint_data: Optional[str] = Field(None, description="Datos de huella digital")
    photo_data: Optional[str] = Field(None, description="Datos de foto")

class UserUpdate(BaseModel):
    names: Optional[str] = Field(None, min_length=1, max_length=100)
    last_names: Optional[str] = Field(None, min_length=1, max_length=100)
    phone: Optional[str] = Field(None, min_length=8, max_length=15)
    address: Optional[str] = Field(None, min_length=1, max_length=200)
    fingerprint_data: Optional[str] = Field(None)
    photo_data: Optional[str] = Field(None)

class UserInDB(UserBase):
    id: str = Field(..., description="ID único del usuario")
    hashed_password: str = Field(..., description="Contraseña hasheada")
    fingerprint_data: Optional[str] = Field(None)
    photo_data: Optional[str] = Field(None)
    status: UserStatus = Field(..., description="Estado del usuario")
    email_verified: bool = Field(default=False, description="Email verificado")
    created_at: datetime = Field(..., description="Fecha de creación")
    updated_at: datetime = Field(..., description="Fecha de actualización")
    suspension_end: Optional[datetime] = Field(None, description="Fin de suspensión")

    class Config:
        from_attributes = True

class UserResponse(UserBase):
    id: str = Field(..., description="ID único del usuario")
    status: UserStatus = Field(..., description="Estado del usuario")
    email_verified: bool = Field(..., description="Email verificado")
    created_at: datetime = Field(..., description="Fecha de creación")

    class Config:
        from_attributes = True
