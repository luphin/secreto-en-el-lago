from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from app.schemas.user import UserRole, UserStatus

class UserBase(BaseModel):
    rut: str
    names: str
    last_names: str
    email: EmailStr
    phone: str
    address: str
    role: UserRole = UserRole.USER

class UserCreate(UserBase):
    password: str
    fingerprint_data: Optional[str] = None
    photo_data: Optional[str] = None

class UserUpdate(BaseModel):
    names: Optional[str] = None
    last_names: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    fingerprint_data: Optional[str] = None
    photo_data: Optional[str] = None

class UserInDB(UserBase):
    id: str
    hashed_password: str
    fingerprint_data: Optional[str] = None
    photo_data: Optional[str] = None
    status: UserStatus
    email_verified: bool = False
    created_at: datetime
    updated_at: datetime
    suspension_end: Optional[datetime] = None

    class Config:
        from_attributes = True

class UserResponse(UserBase):
    id: str
    status: UserStatus
    email_verified: bool
    created_at: datetime
