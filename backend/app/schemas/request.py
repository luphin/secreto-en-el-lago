from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum

class RequestStatus(str, Enum):
    PENDIENTE = "pendiente"
    PROCESADA = "procesada"
    CANCELADA = "cancelada"
    RECHAZADA = "rechazada"

class RequestType(str, Enum):
    PRESTAMO = "prestamo"
    RESERVA = "reserva"

class RequestBase(BaseModel):
    usuario_id: str = Field(..., description="ID del usuario")
    tipo_solicitud: RequestType = Field(..., description="Tipo de solicitud")
    fecha_solicitud: datetime = Field(..., description="Fecha de la solicitud")
    hora_solicitud: str = Field(..., description="Hora de la solicitud")
    fecha_reserva: Optional[datetime] = Field(None, description="Fecha de reserva (solo para reservas)")

class RequestCreate(BaseModel):
    usuario_id: str = Field(..., description="ID del usuario")
    tipo_solicitud: RequestType = Field(..., description="Tipo de solicitud")
    documentos_ids: List[str] = Field(..., min_items=1, description="IDs de los documentos")
    fecha_reserva: Optional[datetime] = Field(None, description="Fecha de reserva (solo para reservas)")

class RequestUpdate(BaseModel):
    estado: Optional[RequestStatus] = Field(None, description="Estado de la solicitud")

class RequestItem(BaseModel):
    documento_id: str = Field(..., description="ID del documento")
    estado: RequestStatus = Field(default=RequestStatus.PENDIENTE, description="Estado del ítem")

class RequestInDB(RequestBase):
    id: str = Field(..., description="ID único de la solicitud")
    items: List[RequestItem] = Field(..., description="Items de la solicitud")
    estado: RequestStatus = Field(..., description="Estado de la solicitud")
    procesada_por: Optional[str] = Field(None, description="ID del bibliotecario que procesó")
    fecha_procesamiento: Optional[datetime] = Field(None, description="Fecha de procesamiento")
    created_at: datetime = Field(..., description="Fecha de creación")
    updated_at: datetime = Field(..., description="Fecha de actualización")

    class Config:
        from_attributes = True

class RequestResponse(RequestBase):
    id: str = Field(..., description="ID único de la solicitud")
    items: List[RequestItem] = Field(..., description="Items de la solicitud")
    estado: RequestStatus = Field(..., description="Estado de la solicitud")
    created_at: datetime = Field(..., description="Fecha de creación")

    class Config:
        from_attributes = True
