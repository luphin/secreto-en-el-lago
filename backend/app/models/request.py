from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from app.schemas.request import RequestType, RequestStatus

class RequestBase(BaseModel):
    usuario_id: str
    tipo_solicitud: RequestType
    fecha_solicitud: datetime
    hora_solicitud: str
    fecha_reserva: Optional[datetime] = None

class RequestCreate(BaseModel):
    usuario_id: str
    tipo_solicitud: RequestType
    documentos_ids: List[str] = Field(..., min_items=1)
    fecha_reserva: Optional[datetime] = None

class RequestUpdate(BaseModel):
    estado: Optional[RequestStatus] = None

class RequestItem(BaseModel):
    documento_id: str
    estado: RequestStatus = RequestStatus.PENDIENTE

class RequestInDB(RequestBase):
    id: str
    items: List[RequestItem]
    estado: RequestStatus
    procesada_por: Optional[str] = None
    fecha_procesamiento: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class RequestResponse(RequestBase):
    id: str
    items: List[RequestItem]
    estado: RequestStatus
    created_at: datetime
