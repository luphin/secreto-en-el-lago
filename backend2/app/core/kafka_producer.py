"""
Productor de eventos Kafka para notificaciones asíncronas
"""
import json
import logging
from typing import Dict, Any, Optional
from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaError

from app.core.config import settings

logger = logging.getLogger(__name__)


class KafkaProducerManager:
    """Gestor del productor de Kafka"""
    
    def __init__(self):
        self.producer: Optional[AIOKafkaProducer] = None
        self._started = False
    
    async def start(self):
        """Inicia el productor de Kafka"""
        if self._started:
            return
        
        try:
            self.producer = AIOKafkaProducer(
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                acks='all',
                retry_backoff_ms=500,
                request_timeout_ms=30000
            )
            await self.producer.start()
            self._started = True
            logger.info("✓ Productor Kafka iniciado correctamente")
        except KafkaError as e:
            logger.error(f"✗ Error al iniciar productor Kafka: {e}")
            logger.warning("⚠ Sistema funcionará sin notificaciones por email")
    
    async def stop(self):
        """Detiene el productor de Kafka"""
        if self.producer and self._started:
            await self.producer.stop()
            self._started = False
            logger.info("✓ Productor Kafka detenido")
    
    async def send_event(self, topic: str, event: Dict[str, Any]) -> bool:
        """
        Envía un evento al tópico de Kafka
        
        Args:
            topic: Nombre del tópico
            event: Diccionario con los datos del evento
            
        Returns:
            True si se envió correctamente, False en caso contrario
        """
        if not self.producer or not self._started:
            logger.warning(f"Productor Kafka no disponible. Evento no enviado: {event}")
            return False
        
        try:
            await self.producer.send_and_wait(topic, event)
            logger.info(f"✓ Evento enviado a Kafka: {topic}")
            return True
        except Exception as e:
            logger.error(f"✗ Error al enviar evento a Kafka: {e}")
            return False
    
    async def send_email_notification(
        self,
        recipient: str,
        subject: str,
        body: str,
        template: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Envía una notificación por email a través de Kafka
        
        Args:
            recipient: Email del destinatario
            subject: Asunto del email
            body: Cuerpo del email
            template: Nombre de la plantilla (opcional)
            data: Datos adicionales para la plantilla
            
        Returns:
            True si se envió correctamente, False en caso contrario
        """
        event = {
            "recipient": recipient,
            "subject": subject,
            "body": body,
            "template": template,
            "data": data or {}
        }
        return await self.send_event(settings.KAFKA_EMAIL_TOPIC, event)
    
    async def send_activation_email(self, user_email: str, user_name: str, activation_link: str) -> bool:
        """Envía email de activación de cuenta"""
        subject = "Activa tu cuenta en BEC"
        body = f"""
        Hola {user_name},
        
        Gracias por registrarte en el Sistema de Préstamo BEC.
        
        Para activar tu cuenta, haz clic en el siguiente enlace:
        {activation_link}
        
        Si no solicitaste esta cuenta, puedes ignorar este mensaje.
        
        Saludos,
        Biblioteca de Estación Central
        """
        return await self.send_email_notification(
            recipient=user_email,
            subject=subject,
            body=body,
            template="activation",
            data={"user_name": user_name, "activation_link": activation_link}
        )
    
    async def send_overdue_reminder(
        self,
        user_email: str,
        user_name: str,
        loan_details: Dict[str, Any]
    ) -> bool:
        """Envía recordatorio de préstamo vencido"""
        subject = "Recordatorio: Préstamo vencido"
        body = f"""
        Hola {user_name},
        
        Te recordamos que tienes un préstamo vencido:
        
        Documento: {loan_details.get('document_title', 'N/A')}
        Fecha de devolución: {loan_details.get('due_date', 'N/A')}
        Días de atraso: {loan_details.get('days_overdue', 0)}
        
        Por favor, devuelve el material lo antes posible para evitar sanciones.
        
        Saludos,
        Biblioteca de Estación Central
        """
        return await self.send_email_notification(
            recipient=user_email,
            subject=subject,
            body=body,
            template="overdue_reminder",
            data={"user_name": user_name, **loan_details}
        )
    
    async def send_sanction_notification(
        self,
        user_email: str,
        user_name: str,
        sanction_until: str,
        days_sanctioned: int
    ) -> bool:
        """Envía notificación de sanción"""
        subject = "Notificación de sanción"
        body = f"""
        Hola {user_name},
        
        Debido al retraso en la devolución de material, has recibido una sanción.
        
        Tu cuenta estará suspendida hasta: {sanction_until}
        Días de sanción: {days_sanctioned}
        
        Durante este período no podrás realizar nuevos préstamos.
        
        Saludos,
        Biblioteca de Estación Central
        """
        return await self.send_email_notification(
            recipient=user_email,
            subject=subject,
            body=body,
            template="sanction",
            data={
                "user_name": user_name,
                "sanction_until": sanction_until,
                "days_sanctioned": days_sanctioned
            }
        )


# Instancia global del productor
kafka_producer = KafkaProducerManager()

