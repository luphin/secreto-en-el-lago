from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum

class LoanType(str, Enum):
    SALA = "sala"
    DOMICILIO = "domicilio"

class LoanStatus(str, Enum):
    ACTIVO = "activo"
    DEVUELTO = "devuelto"
    VENCIDO = "vencido"
    MORA = "mora"

class LoanBase(BaseModel):
    usuario_id: str = Field(..., description="ID del usuario")
    tipo_prestamo: LoanType = Field(..., description="Tipo de préstamo")
    fecha_prestamo: datetime = Field(..., description="Fecha del préstamo")
    hora_prestamo: str = Field(..., description="Hora del préstamo")
    fecha_devolucion: datetime = Field(..., description="Fecha de devolución estimada")
    hora_devolucion: str = Field(..., description="Hora de devolución estimada")
    fecha_devolucion_real: Optional[datetime] = Field(None, description="Fecha real de devolución")
    hora_devolucion_real: Optional[str] = Field(None, description="Hora real de devolución")

class LoanCreate(BaseModel):
    usuario_id: str = Field(..., description="ID del usuario")
    tipo_prestamo: LoanType = Field(..., description="Tipo de préstamo")
    ejemplares_ids: List[str] = Field(..., min_items=1, description="IDs de los ejemplares")
    duracion_dias: Optional[int] = Field(None, ge=1, le=30, description="Duración en días (solo domicilio)")

class LoanUpdate(BaseModel):
    fecha_devolucion_real: Optional[datetime] = Field(None, description="Fecha real de devolución")
    hora_devolucion_real: Optional[str] = Field(None, description="Hora real de devolución")

class LoanItem(BaseModel):
    ejemplar_id: str = Field(..., description="ID del ejemplar")
    fecha_devolucion: datetime = Field(..., description="Fecha de devolución")
    hora_devolucion: str = Field(..., description="Hora de devolución")
    estado: LoanStatus = Field(default=LoanStatus.ACTIVO, description="Estado del ítem")

class LoanInDB(LoanBase):
    id: str = Field(..., description="ID único del préstamo")
    items: List[LoanItem] = Field(..., description="Items del préstamo")
    estado_general: LoanStatus = Field(..., description="Estado general del préstamo")
    created_at: datetime = Field(..., description="Fecha de creación")
    updated_at: datetime = Field(..., description="Fecha de actualización")

    class Config:
        from_attributes = True

class LoanResponse(LoanBase):
    id: str = Field(..., description="ID único del préstamo")
    items: List[LoanItem] = Field(..., description="Items del préstamo")
    estado_general: LoanStatus = Field(..., description="Estado general del préstamo")
    created_at: datetime = Field(..., description="Fecha de creación")

    class Config:
        from_attributes = True
