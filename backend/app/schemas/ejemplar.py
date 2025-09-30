from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum

class EjemplarStatus(str, Enum):
    DISPONIBLE = "disponible"
    PRESTADO_SALA = "prestado_sala"
    PRESTADO_DOMICILIO = "prestado_domicilio"
    RESERVADO = "reservado"
    MANTENCION = "mantencion"
    PERDIDO = "perdido"

class EjemplarBase(BaseModel):
    codigo_ubicacion: str = Field(..., min_length=1, max_length=50, description="Código de ubicación")
    documento_id: str = Field(..., description="ID del documento al que pertenece")
    estado: EjemplarStatus = Field(default=EjemplarStatus.DISPONIBLE, description="Estado del ejemplar")
    observaciones: Optional[str] = Field(None, max_length=500, description="Observaciones del ejemplar")

class EjemplarCreate(EjemplarBase):
    pass

class EjemplarUpdate(BaseModel):
    estado: Optional[EjemplarStatus] = Field(None, description="Estado del ejemplar")
    observaciones: Optional[str] = Field(None, max_length=500, description="Observaciones del ejemplar")

class EjemplarInDB(EjemplarBase):
    id: str = Field(..., description="ID único del ejemplar")
    created_at: datetime = Field(..., description="Fecha de creación")
    updated_at: datetime = Field(..., description="Fecha de actualización")

    class Config:
        from_attributes = True

class EjemplarResponse(EjemplarBase):
    id: str = Field(..., description="ID único del ejemplar")
    created_at: datetime = Field(..., description="Fecha de creación")

    class Config:
        from_attributes = True
