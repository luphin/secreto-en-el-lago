from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from app.schemas.loan import LoanType, LoanStatus

class LoanBase(BaseModel):
    usuario_id: str
    tipo_prestamo: LoanType
    fecha_prestamo: datetime
    hora_prestamo: str
    fecha_devolucion: datetime
    hora_devolucion: str
    fecha_devolucion_real: Optional[datetime] = None
    hora_devolucion_real: Optional[str] = None

class LoanCreate(BaseModel):
    usuario_id: str
    tipo_prestamo: LoanType
    ejemplares_ids: List[str] = Field(..., min_items=1)
    duracion_dias: Optional[int] = Field(None, ge=1)

class LoanUpdate(BaseModel):
    fecha_devolucion_real: Optional[datetime] = None
    hora_devolucion_real: Optional[str] = None

class LoanItem(BaseModel):
    ejemplar_id: str
    fecha_devolucion: datetime
    hora_devolucion: str
    estado: LoanStatus = LoanStatus.ACTIVO

class LoanInDB(LoanBase):
    id: str
    items: List[LoanItem]
    estado_general: LoanStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class LoanResponse(LoanBase):
    id: str
    items: List[LoanItem]
    estado_general: LoanStatus
    created_at: datetime
