#!/usr/bin/env python3
"""
Script para crear índices en la base de datos
Útil para ejecutar después de cambios en el esquema
"""

import asyncio
import os
import sys
from motor.motor_asyncio import AsyncIOMotorClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config.settings import settings

async def create_all_indexes():
    """Crear todos los índices necesarios"""
    try:
        client = AsyncIOMotorClient(settings.mongodb_url)
        db = client[settings.database_name]
        
        print("🔍 Creando índices...")
        
        # Índices para usuarios
        await db.users.create_index("email", unique=True)
        await db.users.create_index("rut", unique=True)
        await db.users.create_index("status")
        await db.users.create_index("role")
        print("✅ Índices de usuarios creados")
        
        # Índices para documentos
        await db.documents.create_index("titulo")
        await db.documents.create_index("autor")
        await db.documents.create_index("tipo")
        await db.documents.create_index("categoria")
        await db.documents.create_index([("titulo", "text"), ("autor", "text")])
        print("✅ Índices de documentos creados")
        
        # Índices para ejemplares
        await db.ejemplares.create_index("documento_id")
        await db.ejemplares.create_index("estado")
        await db.ejemplares.create_index("codigo_ubicacion", unique=True)
        print("✅ Índices de ejemplares creados")
        
        # Índices para préstamos
        await db.loans.create_index("usuario_id")
        await db.loans.create_index("estado_general")
        await db.loans.create_index("fecha_devolucion")
        await db.loans.create_index([("usuario_id", 1), ("estado_general", 1)])
        print("✅ Índices de préstamos creados")
        
        # Índices para solicitudes
        await db.requests.create_index("usuario_id")
        await db.requests.create_index("tipo_solicitud")
        await db.requests.create_index("estado")
        await db.requests.create_index("fecha_solicitud")
        print("✅ Índices de solicitudes creados")
        
        # Índices para notificaciones
        await db.notifications.create_index("email")
        await db.notifications.create_index("estado")
        await db.notifications.create_index("created_at")
        print("✅ Índices de notificaciones creados")
        
        # Índices para sanciones
        await db.sanciones.create_index("usuario_id")
        await db.sanciones.create_index("estado")
        await db.sanciones.create_index("fecha_fin")
        print("✅ Índices de sanciones creados")
        
        print("\n🎉 Todos los índices creados exitosamente!")
        
    except Exception as e:
        print(f"❌ Error creando índices: {e}")
        sys.exit(1)
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(create_all_indexes())
