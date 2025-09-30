from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.schemas.document import DocumentType, DocumentCategory, MediaFormat, DocumentStatus

class DocumentBase(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=500)
    autor: str = Field(..., min_length=1, max_length=200)
    tipo: DocumentType
    categoria: DocumentCategory
    editorial: Optional[str] = None
    edicion: Optional[str] = None
    ano_edicion: Optional[int] = None
    isbn: Optional[str] = None
    descripcion: Optional[str] = None
    formato_medio: Optional[MediaFormat] = None
    duracion: Optional[int] = None

class DocumentCreate(DocumentBase):
    numero_ejemplares: int = Field(1, ge=1)

class DocumentUpdate(BaseModel):
    titulo: Optional[str] = None
    autor: Optional[str] = None
    editorial: Optional[str] = None
    edicion: Optional[str] = None
    ano_edicion: Optional[int] = None
    descripcion: Optional[str] = None
    formato_medio: Optional[MediaFormat] = None
    duracion: Optional[int] = None

class DocumentInDB(DocumentBase):
    id: str
    numero_ejemplares: int
    ejemplares_disponibles: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class DocumentResponse(DocumentBase):
    id: str
    numero_ejemplares: int
    ejemplares_disponibles: int
    created_at: datetime
