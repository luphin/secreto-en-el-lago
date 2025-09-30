import asyncio
import json
import structlog
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError
from app.config.settings import settings

logger = structlog.get_logger()

class KafkaManager:
    def __init__(self):
        self.admin_client = None
        self._connect_admin()

    def _connect_admin(self):
        try:
            self.admin_client = KafkaAdminClient(
                bootstrap_servers=settings.kafka_bootstrap_servers,
                client_id='biblioteca-admin'
            )
            logger.info("Kafka Admin Client conectado exitosamente")
        except Exception as e:
            logger.error("Error conectando Kafka Admin Client", error=str(e))
            self.admin_client = None

    async def create_topics(self):
        """Crea los topics necesarios para la aplicación"""
        if not self.admin_client:
            logger.error("Admin client no disponible, no se pueden crear topics")
            return

        topics = [
            NewTopic(
                name=settings.kafka_topic_loans,
                num_partitions=3,
                replication_factor=1
            ),
            NewTopic(
                name=settings.kafka_topic_notifications,
                num_partitions=2,
                replication_factor=1
            ),
            NewTopic(
                name='system-events',
                num_partitions=1,
                replication_factor=1
            ),
            NewTopic(
                name='user-activity',
                num_partitions=2,
                replication_factor=1
            ),
            NewTopic(
                name='document-activity',
                num_partitions=2,
                replication_factor=1
            )
        ]

        try:
            self.admin_client.create_topics(new_topics=topics, validate_only=False)
            logger.info("Todos los topics de Kafka creados exitosamente")
        except TopicAlreadyExistsError:
            logger.info("Los topics de Kafka ya existen")
        except Exception as e:
            logger.error("Error creando topics de Kafka", error=str(e))

    async def get_topic_info(self, topic: str) -> dict:
        """Obtiene información de un topic específico"""
        if not self.admin_client:
            return {"error": "Admin client no disponible"}

        try:
            # Obtener metadata del topic
            cluster_metadata = self.admin_client.describe_topics([topic])
            return cluster_metadata
        except Exception as e:
            logger.error("Error obteniendo información del topic", topic=topic, error=str(e))
            return {"error": str(e)}

    async def list_topics(self) -> list:
        """Lista todos los topics disponibles"""
        if not self.admin_client:
            return []

        try:
            topics = self.admin_client.list_topics()
            return topics
        except Exception as e:
            logger.error("Error listando topics", error=str(e))
            return []

    async def delete_topic(self, topic: str) -> bool:
        """Elimina un topic específico"""
        if not self.admin_client:
            return False

        try:
            self.admin_client.delete_topics([topic])
            logger.info("Topic eliminado", topic=topic)
            return True
        except Exception as e:
            logger.error("Error eliminando topic", topic=topic, error=str(e))
            return False

    def close(self):
        """Cierra la conexión del admin client"""
        if self.admin_client:
            self.admin_client.close()
            logger.info("Kafka Admin Client cerrado")

# Singleton para el manager
kafka_manager = KafkaManager()
