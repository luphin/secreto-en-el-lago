"""
Modelos de reserva (reservation)
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
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


class ReservationStatus(str, Enum):
    """Estados de la reserva"""
    ACTIVA = "activa"
    COMPLETADA = "completada"
    EXPIRADA = "expirada"


class ReservationBase(BaseModel):
    """Esquema base de reserva"""
    document_id: str = Field(..., description="ID del documento reservado")
    user_id: str = Field(..., description="ID del usuario que reserva")
    fecha_reserva: datetime = Field(..., description="Fecha para la cual se reserva")


class ReservationCreate(ReservationBase):
    """Esquema para crear reserva"""
    pass


class ReservationInDB(ReservationBase):
    """Esquema de reserva en base de datos"""
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)
    estado: ReservationStatus = ReservationStatus.ACTIVA

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "document_id": "507f1f77bcf86cd799439011",
                "user_id": "507f1f77bcf86cd799439012",
                "fecha_reserva": "2025-10-10T10:00:00",
                "estado": "activa"
            }
        }


class ReservationResponse(BaseModel):
    """Esquema de respuesta de reserva"""
    id: str = Field(..., alias="_id")
    document_id: str
    user_id: str
    fecha_reserva: datetime
    fecha_creacion: datetime
    estado: ReservationStatus
    # Campos opcionales con información del documento
    document_titulo: Optional[str] = None
    document_id_fisico: Optional[str] = None

    class Config:
        populate_by_name = True

