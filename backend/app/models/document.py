"""
Modelos de documento bibliográfico
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


class DocumentType(str, Enum):
    """Tipos de documento"""
    LIBRO = "libro"
    AUDIO = "audio"
    VIDEO = "video"


class DocumentBase(BaseModel):
    """Esquema base de documento"""
    id_fisico: str = Field(..., min_length=1, description="Identificador físico único del documento")
    titulo: str = Field(..., min_length=1)
    autor: str = Field(..., min_length=1)
    editorial: str
    edicion: str
    ano_edicion: int
    tipo: DocumentType
    categoria: str
    tipo_medio: Optional[str] = None  # DVD, CD, etc.


class DocumentCreate(DocumentBase):
    """Esquema para crear documento"""
    pass


class DocumentUpdate(BaseModel):
    """Esquema para actualizar documento"""
    id_fisico: Optional[str] = None
    titulo: Optional[str] = None
    autor: Optional[str] = None
    editorial: Optional[str] = None
    edicion: Optional[str] = None
    ano_edicion: Optional[int] = None
    tipo: Optional[DocumentType] = None
    categoria: Optional[str] = None
    tipo_medio: Optional[str] = None


class DocumentInDB(DocumentBase):
    """Esquema de documento en base de datos"""
    id: Optional[PyObjectId] = Field(default=None, alias="_id")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "id_fisico": "LIB-001-2024",
                "titulo": "Cien años de soledad",
                "autor": "Gabriel García Márquez",
                "editorial": "Editorial Sudamericana",
                "edicion": "Primera",
                "ano_edicion": 1967,
                "tipo": "libro",
                "categoria": "Novela"
            }
        }


class DocumentResponse(BaseModel):
    """Esquema de respuesta de documento"""
    id: str = Field(..., alias="_id")
    id_fisico: str
    titulo: str
    autor: str
    editorial: str
    edicion: str
    ano_edicion: int
    tipo: DocumentType
    categoria: str
    tipo_medio: Optional[str] = None
    items_disponibles: int = 0  # Se calcula dinámicamente

    class Config:
        populate_by_name = True

