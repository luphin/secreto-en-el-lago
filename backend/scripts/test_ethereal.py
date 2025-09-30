#!/usr/bin/env python3
"""
Script para probar la configuración de Ethereal Email
"""

import asyncio
import os
import sys
from app.services.email_service import EmailService

async def test_ethereal_email():
    """Prueba el envío de email con Ethereal"""
    email_service = EmailService()
    
    test_email = "test@biblioteca.cl"  # Puede ser cualquier email
    subject = "📧 Prueba de Ethereal Email"
    html_content = """
    <html>
        <body>
            <h2>¡Prueba exitosa! 🎉</h2>
            <p>Este email fue enviado usando <strong>Ethereal Email</strong>.</p>
            <p>Puedes verlo en tu inbox de Ethereal.</p>
            <hr>
            <p><em>Sistema Biblioteca Municipal</em></p>
        </body>
    </html>
    """
    
    print("🚀 Enviando email de prueba via Ethereal...")
    success = await email_service.send_email(test_email, subject, html_content)
    
    if success:
        print("✅ Email enviado exitosamente!")
        print(f"📨 Revisa tu inbox en: https://ethereal.email/")
        print(f"🔑 Usuario: {email_service.username}")
    else:
        print("❌ Error enviando email")
    
    return success

if __name__ == "__main__":
    success = asyncio.run(test_ethereal_email())
    sys.exit(0 if success else 1)
