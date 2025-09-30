from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from enum import Enum


class NotificationType(str, Enum):
    PRESTAMO_VENCIDO = "prestamo_vencido"
    RESERVA_DISPONIBLE = "reserva_disponible"
    CUENTA_ACTIVADA = "cuenta_activada"
    BIENVENIDA = "bienvenida"
    SANCION = "sancion"


class NotificationStatus(str, Enum):
    PENDIENTE = "pendiente"
    ENVIADA = "enviada"
    FALLIDA = "fallida"


class NotificationBase(BaseModel):
    usuario_id: str
    tipo: NotificationType
    asunto: str
    mensaje: str
    email: EmailStr


class NotificationCreate(NotificationBase):
    pass


class NotificationInDB(NotificationBase):
    id: str
    estado: NotificationStatus
    intentos: int = 0
    enviada_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class NotificationResponse(NotificationBase):
    id: str
    estado: NotificationStatus
    created_at: datetime
