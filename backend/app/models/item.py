"""
Modelos de ejemplar (item)
"""
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


class ItemStatus(str, Enum):
    """Estados del ejemplar"""
    DISPONIBLE = "disponible"
    PRESTADO = "prestado"
    EN_RESTAURACION = "en_restauracion"
    RESERVADO = "reservado"


class ItemBase(BaseModel):
    """Esquema base de ejemplar"""
    document_id: str = Field(..., description="ID del documento al que pertenece")
    ubicacion: str = Field(..., description="Ubicación física en la biblioteca")
    estado: ItemStatus = ItemStatus.DISPONIBLE


class ItemCreate(ItemBase):
    """Esquema para crear ejemplar"""
    pass


class ItemUpdate(BaseModel):
    """Esquema para actualizar ejemplar"""
    ubicacion: Optional[str] = None
    estado: Optional[ItemStatus] = None


class ItemInDB(ItemBase):
    """Esquema de ejemplar en base de datos"""
    id: Optional[PyObjectId] = Field(default=None, alias="_id")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "document_id": "507f1f77bcf86cd799439011",
                "estado": "disponible",
                "ubicacion": "Estantería 5, Nivel 3"
            }
        }


class ItemResponse(BaseModel):
    """Esquema de respuesta de ejemplar"""
    id: str = Field(..., alias="_id")
    document_id: str
    ubicacion: str
    estado: ItemStatus

    class Config:
        populate_by_name = True

