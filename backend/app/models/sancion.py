from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum


class SancionType(str, Enum):
    RETRASO = "retraso"
    PERDIDA = "perdida"
    DANIO = "danio"


class SancionStatus(str, Enum):
    ACTIVA = "activa"
    CUMPLIDA = "cumplida"
    CANCELADA = "cancelada"


class SancionBase(BaseModel):
    usuario_id: str
    tipo: SancionType
    prestamo_id: str
    dias_sancion: int = Field(..., ge=1)
    fecha_inicio: datetime
    fecha_fin: datetime
    descripcion: str


class SancionCreate(SancionBase):
    pass


class SancionUpdate(BaseModel):
    estado: Optional[SancionStatus] = None


class SancionInDB(SancionBase):
    id: str
    estado: SancionStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SancionResponse(SancionBase):
    id: str
    estado: SancionStatus
    created_at: datetime
