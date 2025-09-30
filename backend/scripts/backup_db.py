#!/usr/bin/env python3
"""
Script para crear backup de la base de datos
"""

import asyncio
import os
import json
import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from bson import json_util

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config.settings import settings

async def backup_database():
    """Crear backup de todas las colecciones"""
    try:
        client = AsyncIOMotorClient(settings.mongodb_url)
        db = client[settings.database_name]
        
        # Crear directorio de backup si no existe
        backup_dir = "backups"
        os.makedirs(backup_dir, exist_ok=True)
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(backup_dir, f"backup_{timestamp}.json")
        
        collections = [
            "users", "documents", "ejemplares", "loans", 
            "requests", "notifications", "sanciones", "system_alerts"
        ]
        
        backup_data = {}
        
        print("💾 Creando backup de la base de datos...")
        
        for collection_name in collections:
            print(f"  📦 Respaldando colección: {collection_name}")
            cursor = db[collection_name].find({})
            documents = await cursor.to_list(length=None)
            backup_data[collection_name] = documents
        
        # Guardar backup en archivo JSON
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, default=json_util.default, indent=2, ensure_ascii=False)
        
        print(f"✅ Backup creado exitosamente: {backup_file}")
        print(f"📊 Total de colecciones respaldadas: {len(collections)}")
        
    except Exception as e:
        print(f"❌ Error creando backup: {e}")
        sys.exit(1)
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(backup_database())
