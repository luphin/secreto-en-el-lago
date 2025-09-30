from kafka import KafkaProducer, KafkaConsumer
import json
import asyncio
import structlog
from app.config.settings import settings

logger = structlog.get_logger()

class KafkaService:
    def __init__(self):
        self.bootstrap_servers = settings.kafka_bootstrap_servers
        self.producer = None
        self._connect_producer()

    def _connect_producer(self):
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                key_serializer=lambda v: json.dumps(v).encode('utf-8'),
                retries=3
            )
            logger.info("Kafka producer conectado exitosamente")
        except Exception as e:
            logger.error("Error conectando Kafka producer", error=str(e))
            self.producer = None

    async def send_loan_created_event(self, loan_id: str, user_id: str):
        event = {
            "event_type": "loan_created",
            "loan_id": loan_id,
            "user_id": user_id,
            "timestamp": self._get_current_timestamp()
        }
        await self._send_message(settings.kafka_topic_loans, event, loan_id)

    async def send_loan_returned_event(self, loan_id: str, user_id: str):
        event = {
            "event_type": "loan_returned",
            "loan_id": loan_id,
            "user_id": user_id,
            "timestamp": self._get_current_timestamp()
        }
        await self._send_message(settings.kafka_topic_loans, event, loan_id)

    async def send_overdue_loan_event(self, loan_id: str, user_id: str, days_overdue: int):
        event = {
            "event_type": "loan_overdue",
            "loan_id": loan_id,
            "user_id": user_id,
            "days_overdue": days_overdue,
            "timestamp": self._get_current_timestamp()
        }
        await self._send_message(settings.kafka_topic_loans, event, loan_id)

    async def send_user_registered_event(self, user_id: str, email: str):
        event = {
            "event_type": "user_registered",
            "user_id": user_id,
            "email": email,
            "timestamp": self._get_current_timestamp()
        }
        await self._send_message(settings.kafka_topic_notifications, event, user_id)

    async def send_email_notification_event(self, to_email: str, subject: str, notification_type: str):
        event = {
            "event_type": "email_notification",
            "to_email": to_email,
            "subject": subject,
            "notification_type": notification_type,
            "timestamp": self._get_current_timestamp()
        }
        await self._send_message(settings.kafka_topic_notifications, event, to_email)

    async def send_system_alert_event(self, alert_type: str, message: str, severity: str = "warning"):
        event = {
            "event_type": "system_alert",
            "alert_type": alert_type,
            "message": message,
            "severity": severity,
            "timestamp": self._get_current_timestamp()
        }
        await self._send_message(settings.kafka_topic_notifications, event, alert_type)

    async def _send_message(self, topic: str, message: dict, key: str = None):
        if not self.producer:
            logger.warning("Kafka producer no disponible, mensaje no enviado", topic=topic)
            return

        try:
            future = self.producer.send(
                topic,
                key=key,
                value=message
            )
            # Esperar de manera asíncrona
            await asyncio.get_event_loop().run_in_executor(None, future.get, 10)  # 10 segundos timeout
            logger.debug("Mensaje enviado a Kafka", topic=topic, key=key)
        except Exception as e:
            logger.error("Error enviando mensaje a Kafka", topic=topic, error=str(e))

    def _get_current_timestamp(self):
        from datetime import datetime
        return datetime.utcnow().isoformat()

    async def close(self):
        if self.producer:
            self.producer.close()
            logger.info("Kafka producer cerrado")

# Consumer para procesar eventos (se puede ejecutar en un proceso separado)
class KafkaEventConsumer:
    def __init__(self, topic: str, group_id: str):
        self.topic = topic
        self.group_id = group_id
        self.consumer = None
        self._connect_consumer()

    def _connect_consumer(self):
        try:
            self.consumer = KafkaConsumer(
                self.topic,
                bootstrap_servers=settings.kafka_bootstrap_servers,
                group_id=self.group_id,
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                auto_offset_reset='earliest',
                enable_auto_commit=True
            )
            logger.info(f"Kafka consumer conectado para topic: {self.topic}")
        except Exception as e:
            logger.error(f"Error conectando Kafka consumer para topic {self.topic}", error=str(e))
            self.consumer = None

    async def process_events(self, message_handler):
        if not self.consumer:
            logger.error("Consumer no disponible")
            return

        for message in self.consumer:
            try:
                await message_handler(message.value)
                logger.debug("Mensaje procesado exitosamente", topic=message.topic)
            except Exception as e:
                logger.error("Error procesando mensaje", topic=message.topic, error=str(e))

    def close(self):
        if self.consumer:
            self.consumer.close()
            logger.info("Kafka consumer cerrado")
