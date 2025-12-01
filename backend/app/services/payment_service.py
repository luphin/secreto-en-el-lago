import mercadopago
from app.core.config import settings
import sys
import json

# Inicializar SDK con el access token configurado
def get_sdk():
    return mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)

class PaymentService:
    @staticmethod
    def create_preference(items: list, payer_email: str, back_urls: dict = None):
        """
        Crea una preferencia de pago en Mercado Pago
        """
        token = settings.MERCADOPAGO_ACCESS_TOKEN
        
        if not token:
             raise Exception("MERCADOPAGO_ACCESS_TOKEN no está configurado")
             
        sdk = get_sdk()
        
        # URLs por defecto si no se proporcionan
        # IMPORTANTE: Mercado Pago requiere back_urls válidas si auto_return='approved'
        if not back_urls:
            base_url = "http://localhost:3000"
            back_urls = {
                "success": f"{base_url}/payment/success",
                "failure": f"{base_url}/payment/failure",
                "pending": f"{base_url}/payment/pending"
            }

        print(f"DEBUG: Configurando preference con back_urls: {back_urls}", file=sys.stderr)

        preference_data = {
            "items": items,
            "payer": {
                "email": payer_email
            },
            "back_urls": back_urls,
            #"auto_return": "approved",
            # Excluir pagos en efectivo si se desea solo online, opcional
            # "payment_methods": { ... }
        }

        preference_response = sdk.preference().create(preference_data)
        
        if preference_response["status"] == 201:
            return preference_response["response"]
        else:
            # IMPRIMIR RESPUESTA COMPLETA PARA DEBUG
            print("RESPUESTA COMPLETA DE MERCADO PAGO:", file=sys.stderr)
            print(json.dumps(preference_response, indent=2), file=sys.stderr)
            
            # Manejar error adecuadamente
            raise Exception(f"Error creando preferencia: {preference_response.get('message', 'Unknown error')}")
