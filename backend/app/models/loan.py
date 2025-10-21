"""
Modelos de préstamo (loan)
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


class LoanType(str, Enum):
    """Tipos de préstamo"""
    SALA = "sala"
    DOMICILIO = "domicilio"


class LoanStatus(str, Enum):
    """Estados del préstamo"""
    ACTIVO = "activo"
    DEVUELTO = "devuelto"
    VENCIDO = "vencido"


class LoanBase(BaseModel):
    """Esquema base de préstamo"""
    item_id: str = Field(..., description="ID del ejemplar prestado")
    user_id: str = Field(..., description="ID del usuario que realiza el préstamo")
    tipo_prestamo: LoanType


class LoanCreate(LoanBase):
    """Esquema para crear préstamo"""
    pass


class LoanInDB(LoanBase):
    """Esquema de préstamo en base de datos"""
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    fecha_prestamo: datetime = Field(default_factory=datetime.utcnow)
    fecha_devolucion_pactada: datetime
    fecha_devolucion_real: Optional[datetime] = None
    estado: LoanStatus = LoanStatus.ACTIVO

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "item_id": "507f1f77bcf86cd799439011",
                "user_id": "507f1f77bcf86cd799439012",
                "tipo_prestamo": "domicilio",
                "estado": "activo"
            }
        }


class LoanResponse(BaseModel):
    """Esquema de respuesta de préstamo"""
    id: str = Field(..., alias="_id")
    item_id: str
    user_id: str
    tipo_prestamo: LoanType
    fecha_prestamo: datetime
    fecha_devolucion_pactada: datetime
    fecha_devolucion_real: Optional[datetime]
    estado: LoanStatus

    class Config:
        populate_by_name = True


class LoanReturn(BaseModel):
    """Esquema para devolver un préstamo"""
    loan_id: str

