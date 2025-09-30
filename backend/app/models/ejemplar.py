from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.schemas.ejemplar import EjemplarStatus

class EjemplarBase(BaseModel):
    codigo_ubicacion: str = Field(..., min_length=1, max_length=50)
    documento_id: str
    estado: EjemplarStatus = EjemplarStatus.DISPONIBLE
    observaciones: Optional[str] = None

class EjemplarCreate(EjemplarBase):
    pass

class EjemplarUpdate(BaseModel):
    estado: Optional[EjemplarStatus] = None
    observaciones: Optional[str] = None

class EjemplarInDB(EjemplarBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class EjemplarResponse(EjemplarBase):
    id: str
    created_at: datetime
