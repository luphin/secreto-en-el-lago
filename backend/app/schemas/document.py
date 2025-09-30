from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum

class DocumentType(str, Enum):
    LIBRO = "libro"
    AUDIO = "audio"
    VIDEO = "video"
    REVISTA = "revista"
    PERIODICO = "periodico"

class DocumentCategory(str, Enum):
    LITERATURA_CHILENA = "literatura_chilena"
    LITERATURA_ESPANOLA = "literatura_espanola"
    LITERATURA_INGLESA = "literatura_inglesa"
    LITERATURA_UNIVERSAL = "literatura_universal"
    TECNICO_ESPANOL = "tecnico_espanol"
    TECNICO_INGLES = "tecnico_ingles"
    CIENCIAS = "ciencias"
    HISTORIA = "historia"
    FILOSOFIA = "filosofia"
    ARTE = "arte"
    PELICULA = "pelicula"
    DOCUMENTAL = "documental"
    MUSICA = "musica"
    AUDIOLIBRO = "audiolibro"
    SONIDOS = "sonidos"

class MediaFormat(str, Enum):
    CASSETTE = "casete"
    CD = "cd"
    DVD = "dvd"
    BLURAY = "bluray"
    DIGITAL = "digital"
    VINILO = "vinilo"

class DocumentStatus(str, Enum):
    DISPONIBLE = "disponible"
    PRESTADO = "prestado"
    RESERVADO = "reservado"
    MANTENCION = "mantencion"
    PERDIDO = "perdido"

class DocumentBase(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=500, description="Título del documento")
    autor: str = Field(..., min_length=1, max_length=200, description="Autor del documento")
    tipo: DocumentType = Field(..., description="Tipo de documento")
    categoria: DocumentCategory = Field(..., description="Categoría del documento")
    editorial: Optional[str] = Field(None, max_length=200, description="Editorial")
    edicion: Optional[str] = Field(None, max_length=100, description="Edición")
    ano_edicion: Optional[int] = Field(None, ge=1000, le=2100, description="Año de edición")
    isbn: Optional[str] = Field(None, max_length=20, description="ISBN")
    descripcion: Optional[str] = Field(None, description="Descripción del documento")
    formato_medio: Optional[MediaFormat] = Field(None, description="Formato del medio (solo multimedia)")
    duracion: Optional[int] = Field(None, ge=1, description="Duración en minutos (solo audio/video)")

class DocumentCreate(DocumentBase):
    numero_ejemplares: int = Field(1, ge=1, le=100, description="Número de ejemplares iniciales")

class DocumentUpdate(BaseModel):
    titulo: Optional[str] = Field(None, min_length=1, max_length=500)
    autor: Optional[str] = Field(None, min_length=1, max_length=200)
    editorial: Optional[str] = Field(None, max_length=200)
    edicion: Optional[str] = Field(None, max_length=100)
    ano_edicion: Optional[int] = Field(None, ge=1000, le=2100)
    descripcion: Optional[str] = Field(None)
    formato_medio: Optional[MediaFormat] = Field(None)
    duracion: Optional[int] = Field(None, ge=1)

class DocumentInDB(DocumentBase):
    id: str = Field(..., description="ID único del documento")
    numero_ejemplares: int = Field(..., ge=0, description="Número total de ejemplares")
    ejemplares_disponibles: int = Field(..., ge=0, description="Número de ejemplares disponibles")
    created_at: datetime = Field(..., description="Fecha de creación")
    updated_at: datetime = Field(..., description="Fecha de actualización")

    class Config:
        from_attributes = True

class DocumentResponse(DocumentBase):
    id: str = Field(..., description="ID único del documento")
    numero_ejemplares: int = Field(..., description="Número total de ejemplares")
    ejemplares_disponibles: int = Field(..., description="Número de ejemplares disponibles")
    created_at: datetime = Field(..., description="Fecha de creación")

    class Config:
        from_attributes = True
