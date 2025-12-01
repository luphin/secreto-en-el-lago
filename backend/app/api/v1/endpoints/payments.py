from fastapi import APIRouter, HTTPException
from app.services.payment_service import PaymentService
from pydantic import BaseModel, EmailStr
from typing import List
import traceback

router = APIRouter()

class PaymentItem(BaseModel):
    title: str
    quantity: int
    unit_price: float
    currency_id: str = "CLP"

class PaymentRequest(BaseModel):
    items: List[PaymentItem]
    email: EmailStr

@router.post("/create_preference")
async def create_payment_preference(payment_data: PaymentRequest):
    try:
        # Convertir items Pydantic a dicts
        items_list = [item.model_dump() for item in payment_data.items]
        
        print(f"DEBUG: Intentando crear pago para {payment_data.email}")
        
        result = PaymentService.create_preference(items_list, payment_data.email)
        
        return {
            "preferenceId": result["id"], 
            "init_point": result["init_point"],
            "sandbox_init_point": result["sandbox_init_point"]
        }
    except Exception as e:
        print("ERROR CRÍTICO EN MERCADO PAGO:")
        print(e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
