import aiosmtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
from datetime import datetime
import structlog
from app.config.settings import settings

logger = structlog.get_logger()

class EmailService:
    def __init__(self):
        self.host = settings.email_host
        self.port = settings.email_port
        self.username = settings.email_username
        self.password = settings.email_password

    async def send_email(self, to_email: str, subject: str, html_content: str) -> bool:
        try:
            message = MimeMultipart("alternative")
            message["From"] = self.username
            message["To"] = to_email
            message["Subject"] = subject

            # Create HTML part
            html_part = MimeText(html_content, "html")
            message.attach(html_part)

            await aiosmtplib.send(
                message,
                hostname=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                use_tls=True
            )

            logger.info("Email enviado exitosamente", to_email=to_email, subject=subject)
            return True

        except Exception as e:
            logger.error("Error enviando email", to_email=to_email, error=str(e))
            return False

    async def send_verification_email(self, to_email: str, verification_token: str) -> bool:
        subject = "Verifica tu cuenta - Biblioteca Municipal"
        verification_url = f"https://tudominio.com/verify-email?token={verification_token}"
        
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                    <h2 style="color: #2c5aa0; text-align: center;">Bienvenido a la Biblioteca Municipal</h2>
                    <p>Gracias por registrarte en nuestro sistema. Para activar tu cuenta, por favor verifícala haciendo clic en el siguiente enlace:</p>
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{verification_url}" style="background-color: #2c5aa0; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block;">
                            Verificar Cuenta
                        </a>
                    </div>
                    <p style="font-size: 12px; color: #666; text-align: center;">
                        Este enlace expirará en 24 horas.<br>
                        Si no solicitaste este registro, por favor ignora este mensaje.
                    </p>
                </div>
            </body>
        </html>
        """
        
        return await self.send_email(to_email, subject, html_content)

    async def send_welcome_email(self, to_email: str) -> bool:
        subject = "¡Bienvenido a la Biblioteca Municipal!"
        
        html_content = """
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                    <h2 style="color: #2c5aa0; text-align: center;">¡Cuenta Verificada Exitosamente!</h2>
                    <p>Tu cuenta ha sido verificada y ahora puedes disfrutar de todos nuestros servicios:</p>
                    <ul>
                        <li>📚 Consulta nuestro catálogo en línea</li>
                        <li>🏠 Solicita préstamos a domicilio</li>
                        <li>📅 Reserva documentos</li>
                        <li>🪑 Accede a nuestra sala de lectura</li>
                        <li>🔍 Utiliza nuestros tótems de consulta</li>
                    </ul>
                    <p style="text-align: center; font-weight: bold;">¡Te esperamos en la biblioteca!</p>
                    <hr style="margin: 20px 0;">
                    <p style="font-size: 12px; color: #666;">
                        Horario de atención: Lunes a Viernes 9:00 - 20:00, Sábados 10:00 - 14:00<br>
                        Dirección: Plaza Central 123, Estación Central
                    </p>
                </div>
            </body>
        </html>
        """
        
        return await self.send_email(to_email, subject, html_content)

    async def send_loan_reminder_email(self, to_email: str, loan_details: dict) -> bool:
        subject = "Recordatorio de Préstamo - Biblioteca Municipal"
        
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                    <h2 style="color: #2c5aa0; text-align: center;">Recordatorio de Préstamo</h2>
                    <p>Tienes los siguientes documentos con fecha de devolución próxima:</p>
                    <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 15px 0;">
                        <p><strong>Documento:</strong> {loan_details['titulo']}</p>
                        <p><strong>Autor:</strong> {loan_details['autor']}</p>
                        <p><strong>Fecha de devolución:</strong> {loan_details['fecha_devolucion']}</p>
                        <p><strong>Tipo de préstamo:</strong> {loan_details['tipo_prestamo']}</p>
                    </div>
                    <p style="color: #d35400; font-weight: bold;">
                        ⚠️ Por favor, realiza la devolución a tiempo para evitar sanciones.
                    </p>
                </div>
            </body>
        </html>
        """
        
        return await self.send_email(to_email, subject, html_content)

    async def send_overdue_email(self, to_email: str, loan_details: dict) -> bool:
        subject = "Préstamo Vencido - Biblioteca Municipal"
        
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e74c3c; border-radius: 10px;">
                    <h2 style="color: #e74c3c; text-align: center;">Préstamo Vencido</h2>
                    <p>Tienes los siguientes documentos con devolución vencida:</p>
                    <div style="background-color: #fdedec; padding: 15px; border-radius: 5px; margin: 15px 0;">
                        <p><strong>Documento:</strong> {loan_details['titulo']}</p>
                        <p><strong>Autor:</strong> {loan_details['autor']}</p>
                        <p><strong>Fecha de devolución:</strong> {loan_details['fecha_devolucion']}</p>
                        <p><strong>Días de retraso:</strong> {loan_details['dias_retraso']}</p>
                    </div>
                    <p style="color: #e74c3c; font-weight: bold;">
                        🚨 Por favor, realiza la devolución inmediatamente para evitar sanciones adicionales.
                    </p>
                    <p style="font-size: 12px; color: #666;">
                        Recuerda que los retrasos en la devolución pueden resultar en suspensión temporal de tus privilegios de préstamo.
                    </p>
                </div>
            </body>
        </html>
        """
        
        return await self.send_email(to_email, subject, html_content)

    async def send_sanction_email(self, to_email: str, dias_sancion: int, motivo: str) -> bool:
        subject = "Notificación de Sanción - Biblioteca Municipal"
        
        fecha_fin = (datetime.utcnow() + timedelta(days=dias_sancion)).strftime("%d/%m/%Y")
        
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e74c3c; border-radius: 10px;">
                    <h2 style="color: #e74c3c; text-align: center;">Notificación de Sanción</h2>
                    <p>Se ha aplicado una sanción a tu cuenta por la siguiente razón:</p>
                    <div style="background-color: #fdedec; padding: 15px; border-radius: 5px; margin: 15px 0;">
                        <p><strong>Motivo:</strong> {motivo}</p>
                        <p><strong>Duración de la sanción:</strong> {dias_sancion} días</p>
                        <p><strong>Fecha de fin de sanción:</strong> {fecha_fin}</p>
                    </div>
                    <p style="color: #e74c3c; font-weight: bold;">
                        Durante este período no podrás realizar nuevos préstamos en la biblioteca.
                    </p>
                    <p style="font-size: 12px; color: #666;">
                        Si consideras que esto es un error, por favor contacta a la administración de la biblioteca.
                    </p>
                </div>
            </body>
        </html>
        """
        
        return await self.send_email(to_email, subject, html_content)

    async def send_reservation_available_email(self, to_email: str, reservation_details: dict) -> bool:
        subject = "Reserva Disponible - Biblioteca Municipal"
        
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #27ae60; border-radius: 10px;">
                    <h2 style="color: #27ae60; text-align: center;">¡Tu Reserva está Disponible!</h2>
                    <p>El documento que reservaste ya está disponible para retiro:</p>
                    <div style="background-color: #eafaf1; padding: 15px; border-radius: 5px; margin: 15px 0;">
                        <p><strong>Documento:</strong> {reservation_details['titulo']}</p>
                        <p><strong>Autor:</strong> {reservation_details['autor']}</p>
                        <p><strong>Código:</strong> {reservation_details['codigo_ubicacion']}</p>
                    </div>
                    <p style="color: #27ae60; font-weight: bold;">
                        ✅ Tienes 48 horas para retirar tu reserva en el mesón principal.
                    </p>
                    <p style="font-size: 12px; color: #666;">
                        Pasado este tiempo, la reserva será cancelada y el documento estará disponible para otros usuarios.
                    </p>
                </div>
            </body>
        </html>
        """
        
        return await self.send_email(to_email, subject, html_content)

    async def send_password_reset_email(self, to_email: str, reset_token: str) -> bool:
        subject = "Restablecer Contraseña - Biblioteca Municipal"
        reset_url = f"https://tudominio.com/reset-password?token={reset_token}"
        
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                    <h2 style="color: #2c5aa0; text-align: center;">Restablecer Contraseña</h2>
                    <p>Has solicitado restablecer tu contraseña. Haz clic en el siguiente enlace para crear una nueva contraseña:</p>
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{reset_url}" style="background-color: #2c5aa0; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block;">
                            Restablecer Contraseña
                        </a>
                    </div>
                    <p style="font-size: 12px; color: #666; text-align: center;">
                        Este enlace expirará en 1 hora.<br>
                        Si no solicitaste este cambio, por favor ignora este mensaje.
                    </p>
                </div>
            </body>
        </html>
        """
        
        return await self.send_email(to_email, subject, html_content)
