import asyncio
import json
import structlog
import uuid
from datetime import datetime
from kafka import KafkaConsumer
from typing import Callable, Dict, Any
from app.config.settings import settings
from app.services.email_service import EmailService
from app.services.loan_service import LoanService
from app.config.database import get_database

logger = structlog.get_logger()

class KafkaConsumerService:
    def __init__(self):
        self.email_service = EmailService()
        self.db = None
        self.loan_service = None
        self.running = False
        
    async def start_consumers(self):
        """Inicia todos los consumers de Kafka"""
        # Inicializar servicios que requieren DB después de que la DB esté conectada
        self.db = get_database()
        if self.db is not None:
            self.loan_service = LoanService(self.db)
        
        self.running = True
        
        # Iniciar consumers en background tasks
        asyncio.create_task(self._consume_loan_events())
        asyncio.create_task(self._consume_notification_events())
        asyncio.create_task(self._consume_system_events())
        
        logger.info("Todos los Kafka consumers iniciados")

    async def stop_consumers(self):
        """Detiene todos los consumers"""
        self.running = False
        logger.info("Kafka consumers detenidos")

    async def _consume_loan_events(self):
        """Consumer para eventos de préstamos"""
        consumer = KafkaConsumer(
            settings.kafka_topic_loans,
            bootstrap_servers=settings.kafka_bootstrap_servers,
            group_id='loan-processor',
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            session_timeout_ms=30000,
            heartbeat_interval_ms=10000
        )

        logger.info("Iniciando consumer de eventos de préstamos")
        
        try:
            for message in consumer:
                if not self.running:
                    break
                    
                try:
                    await self._process_loan_event(message.value)
                    logger.debug("Evento de préstamo procesado", event_type=message.value.get('event_type'))
                except Exception as e:
                    logger.error("Error procesando evento de préstamo", error=str(e), event=message.value)
        except Exception as e:
            logger.error("Error en consumer de préstamos", error=str(e))
        finally:
            consumer.close()

    async def _consume_notification_events(self):
        """Consumer para eventos de notificaciones"""
        consumer = KafkaConsumer(
            settings.kafka_topic_notifications,
            bootstrap_servers=settings.kafka_bootstrap_servers,
            group_id='notification-processor',
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            session_timeout_ms=30000,
            heartbeat_interval_ms=10000
        )

        logger.info("Iniciando consumer de eventos de notificaciones")
        
        try:
            for message in consumer:
                if not self.running:
                    break
                    
                try:
                    await self._process_notification_event(message.value)
                    logger.debug("Evento de notificación procesado", event_type=message.value.get('event_type'))
                except Exception as e:
                    logger.error("Error procesando evento de notificación", error=str(e), event=message.value)
        except Exception as e:
            logger.error("Error en consumer de notificaciones", error=str(e))
        finally:
            consumer.close()

    async def _consume_system_events(self):
        """Consumer para eventos del sistema"""
        consumer = KafkaConsumer(
            'system-events',
            bootstrap_servers=settings.kafka_bootstrap_servers,
            group_id='system-monitor',
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True
        )

        logger.info("Iniciando consumer de eventos del sistema")
        
        try:
            for message in consumer:
                if not self.running:
                    break
                    
                try:
                    await self._process_system_event(message.value)
                except Exception as e:
                    logger.error("Error procesando evento del sistema", error=str(e), event=message.value)
        except Exception as e:
            logger.error("Error en consumer del sistema", error=str(e))
        finally:
            consumer.close()

    async def _process_loan_event(self, event: Dict[str, Any]):
        """Procesa eventos relacionados con préstamos"""
        event_type = event.get('event_type')
        
        if event_type == 'loan_overdue':
            await self._handle_overdue_loan(event)
        elif event_type == 'loan_created':
            await self._handle_loan_created(event)
        elif event_type == 'loan_returned':
            await self._handle_loan_returned(event)
        else:
            logger.warning("Tipo de evento de préstamo no reconocido", event_type=event_type)

    async def _process_notification_event(self, event: Dict[str, Any]):
        """Procesa eventos de notificaciones"""
        event_type = event.get('event_type')
        
        if event_type == 'email_notification':
            await self._handle_email_notification(event)
        elif event_type == 'user_registered':
            await self._handle_user_registered(event)
        elif event_type == 'system_alert':
            await self._handle_system_alert(event)
        else:
            logger.warning("Tipo de evento de notificación no reconocido", event_type=event_type)

    async def _process_system_event(self, event: Dict[str, Any]):
        """Procesa eventos del sistema"""
        # Aquí se pueden procesar métricas, logs, alertas del sistema
        logger.info("Evento del sistema recibido", event_type=event.get('event_type'), event=event)

    async def _handle_overdue_loan(self, event: Dict[str, Any]):
        """Maneja préstamos vencidos"""
        loan_id = event.get('loan_id')
        user_id = event.get('user_id')
        days_overdue = event.get('days_overdue', 0)
        
        # Obtener información del préstamo
        loan = await self.loan_service.get_loan(loan_id)
        if not loan:
            logger.warning("Préstamo no encontrado para evento de vencimiento", loan_id=loan_id)
            return

        # Obtener información del usuario
        user = await self.db.users.find_one({"id": user_id})
        if not user:
            logger.warning("Usuario no encontrado para evento de préstamo vencido", user_id=user_id)
            return

        # Obtener información de los documentos
        document_titles = []
        for item in loan.items:
            ejemplar = await self.db.ejemplares.find_one({"id": item.ejemplar_id})
            if ejemplar:
                document = await self.db.documents.find_one({"id": ejemplar['documento_id']})
                if document:
                    document_titles.append(document['titulo'])

        # Enviar email de préstamo vencido
        loan_details = {
            'titulo': ', '.join(document_titles) if document_titles else 'Documento no disponible',
            'autor': 'Varios autores' if len(document_titles) > 1 else 'Autor no disponible',
            'fecha_devolucion': loan.fecha_devolucion.strftime('%d/%m/%Y'),
            'dias_retraso': days_overdue
        }

        await self.email_service.send_overdue_email(user['email'], loan_details)
        
        logger.info("Email de préstamo vencido enviado", user_id=user_id, loan_id=loan_id, days_overdue=days_overdue)

    async def _handle_loan_created(self, event: Dict[str, Any]):
        """Maneja creación de préstamos"""
        loan_id = event.get('loan_id')
        user_id = event.get('user_id')
        
        # Aquí se puede agregar lógica adicional cuando se crea un préstamo
        # como enviar confirmación, actualizar dashboards, etc.
        
        logger.info("Procesando creación de préstamo", loan_id=loan_id, user_id=user_id)

    async def _handle_loan_returned(self, event: Dict[str, Any]):
        """Maneja devolución de préstamos"""
        loan_id = event.get('loan_id')
        user_id = event.get('user_id')
        
        # Lógica adicional para devoluciones
        # como liberar reservas, actualizar estadísticas, etc.
        
        logger.info("Procesando devolución de préstamo", loan_id=loan_id, user_id=user_id)

    async def _handle_email_notification(self, event: Dict[str, Any]):
        """Maneja notificaciones por email"""
        to_email = event.get('to_email')
        subject = event.get('subject')
        notification_type = event.get('notification_type')
        
        # Registrar la notificación en la base de datos
        notification_id = str(uuid.uuid4())
        notification_data = {
            "id": notification_id,
            "email": to_email,
            "subject": subject,
            "tipo": notification_type,
            "estado": "procesado",
            "created_at": datetime.utcnow()
        }
        
        await self.db.notifications.insert_one(notification_data)
        logger.info("Notificación registrada en BD", email=to_email, type=notification_type)

    async def _handle_user_registered(self, event: Dict[str, Any]):
        """Maneja registro de usuarios"""
        user_id = event.get('user_id')
        email = event.get('email')
        
        # Aquí se puede agregar lógica post-registro
        # como agregar a listas de mailing, segmentación, etc.
        
        logger.info("Procesando registro de usuario", user_id=user_id, email=email)

    async def _handle_system_alert(self, event: Dict[str, Any]):
        """Maneja alertas del sistema"""
        alert_type = event.get('alert_type')
        message = event.get('message')
        severity = event.get('severity', 'warning')
        
        # Registrar alerta en base de datos para monitoreo
        alert_id = str(uuid.uuid4())
        alert_data = {
            "id": alert_id,
            "tipo": alert_type,
            "mensaje": message,
            "severidad": severity,
            "timestamp": datetime.utcnow(),
            "resuelta": False
        }
        
        await self.db.system_alerts.insert_one(alert_data)
        
        # Enviar email a administradores para alertas críticas
        if severity in ['critical', 'error']:
            admin_emails = await self._get_admin_emails()
            for admin_email in admin_emails:
                await self.email_service.send_email(
                    admin_email,
                    f"Alerta del Sistema - {alert_type}",
                    f"<h3>Alerta del Sistema</h3><p><strong>Tipo:</strong> {alert_type}</p><p><strong>Mensaje:</strong> {message}</p><p><strong>Severidad:</strong> {severity}</p>"
                )

        logger.info("Alerta del sistema procesada", alert_type=alert_type, severity=severity)

    async def _get_admin_emails(self) -> list:
        """Obtiene emails de administradores para notificaciones críticas"""
        admins = await self.db.users.find({
            "role": {"$in": ["admin", "librarian"]},
            "status": "active"
        }).to_list(length=None)
        
        return [admin['email'] for admin in admins]

# Singleton para el servicio de consumer
kafka_consumer_service = KafkaConsumerService()
