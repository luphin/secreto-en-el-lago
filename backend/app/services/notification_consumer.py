"""
Servicio consumidor de Kafka para procesamiento de notificaciones por email
Este servicio se ejecuta como un worker independiente
"""
import asyncio
import json
import logging
from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaError
import httpx
from typing import Dict, Any

# Configuración
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
KAFKA_EMAIL_TOPIC = "email-notifications"
EMAIL_API_ENABLED = False  # Cambiar a True cuando tengas credenciales
EMAIL_API_KEY = ""  # Tu API key de SendGrid/Mailgun

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EmailService:
    """Servicio para enviar emails usando SendGrid/Mailgun"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = httpx.AsyncClient()
    
    async def send_email_sendgrid(self, recipient: str, subject: str, body: str) -> bool:
        """Envía email usando SendGrid API"""
        url = "https://api.sendgrid.com/v3/mail/send"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "personalizations": [{
                "to": [{"email": recipient}],
                "subject": subject
            }],
            "from": {"email": "noreply@bec.cl"},
            "content": [{
                "type": "text/plain",
                "value": body
            }]
        }
        
        try:
            response = await self.client.post(url, json=data, headers=headers)
            if response.status_code == 202:
                logger.info(f"✓ Email enviado a {recipient}")
                return True
            else:
                logger.error(f"✗ Error al enviar email: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"✗ Error al enviar email: {e}")
            return False
    
    async def send_email_console(self, recipient: str, subject: str, body: str):
        """Simula el envío de email mostrándolo en consola (para desarrollo)"""
        logger.info("=" * 80)
        logger.info("📧 EMAIL SIMULADO")
        logger.info("=" * 80)
        logger.info(f"Para: {recipient}")
        logger.info(f"Asunto: {subject}")
        logger.info("-" * 80)
        logger.info(body)
        logger.info("=" * 80)
        return True
    
    async def send_email(self, recipient: str, subject: str, body: str) -> bool:
        """Envía email (real o simulado según configuración)"""
        if EMAIL_API_ENABLED and self.api_key:
            return await self.send_email_sendgrid(recipient, subject, body)
        else:
            return await self.send_email_console(recipient, subject, body)
    
    async def close(self):
        """Cierra el cliente HTTP"""
        await self.client.aclose()


class NotificationConsumer:
    """Consumidor de notificaciones de Kafka"""
    
    def __init__(self):
        self.consumer: AIOKafkaConsumer = None
        self.email_service = EmailService(EMAIL_API_KEY)
        self.running = False
    
    async def start(self):
        """Inicia el consumidor"""
        try:
            self.consumer = AIOKafkaConsumer(
                KAFKA_EMAIL_TOPIC,
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                group_id='email-notification-workers',
                auto_offset_reset='earliest'
            )
            
            await self.consumer.start()
            self.running = True
            logger.info(f"✓ Consumidor iniciado. Escuchando tópico: {KAFKA_EMAIL_TOPIC}")
            
            await self.consume_messages()
            
        except KafkaError as e:
            logger.error(f"✗ Error al iniciar consumidor Kafka: {e}")
        finally:
            await self.stop()
    
    async def stop(self):
        """Detiene el consumidor"""
        self.running = False
        if self.consumer:
            await self.consumer.stop()
            logger.info("✓ Consumidor detenido")
        await self.email_service.close()
    
    async def consume_messages(self):
        """Consume mensajes del tópico"""
        try:
            async for message in self.consumer:
                await self.process_message(message.value)
        except asyncio.CancelledError:
            logger.info("Consumidor cancelado")
    
    async def process_message(self, event: Dict[str, Any]):
        """Procesa un mensaje de notificación"""
        try:
            recipient = event.get("recipient")
            subject = event.get("subject")
            body = event.get("body")
            template = event.get("template")
            data = event.get("data", {})
            
            if not recipient or not subject or not body:
                logger.warning(f"Mensaje incompleto: {event}")
                return
            
            # Aplicar plantilla si existe
            if template:
                body = self.apply_template(template, body, data)
            
            # Enviar email
            success = await self.email_service.send_email(recipient, subject, body)
            
            if success:
                logger.info(f"✓ Notificación procesada: {subject} -> {recipient}")
            else:
                logger.error(f"✗ Error al procesar notificación: {subject}")
                
        except Exception as e:
            logger.error(f"✗ Error al procesar mensaje: {e}")
    
    def apply_template(self, template: str, body: str, data: Dict[str, Any]) -> str:
        """Aplica una plantilla al cuerpo del email"""
        # Aquí podrías usar un motor de plantillas como Jinja2
        # Por ahora, solo retornamos el body original
        return body


async def main():
    """Función principal del worker"""
    logger.info("🚀 Iniciando Worker de Notificaciones...")
    
    consumer = NotificationConsumer()
    
    try:
        await consumer.start()
    except KeyboardInterrupt:
        logger.info("Deteniendo worker...")
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(main())

