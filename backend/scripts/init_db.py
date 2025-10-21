"""
Script para inicializar la base de datos con datos de ejemplo
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta
import sys
import os

# Agregar el directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings
from app.core.security import get_password_hash


async def init_database():
    """Inicializa la base de datos con datos de ejemplo"""
    
    # Conectar a MongoDB
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.MONGODB_DB_NAME]
    
    print("🔄 Limpiando colecciones existentes...")
    await db.users.delete_many({})
    await db.documents.delete_many({})
    await db.items.delete_many({})
    await db.loans.delete_many({})
    await db.reservations.delete_many({})
    
    print("👥 Creando usuarios de ejemplo...")
    
    # Usuarios de ejemplo
    users = [
        {
            "rut": "12345678-9",
            "nombres": "Admin",
            "apellidos": "Sistema",
            "direccion": "Av. Principal 123",
            "telefono": "+56912345678",
            "email": "admin@bec.cl",
            "password": get_password_hash("admin123"),
            "rol": "administrativo",
            "activo": True,
            "fecha_creacion": datetime.utcnow()
        },
        {
            "rut": "98765432-1",
            "nombres": "María",
            "apellidos": "Bibliotecaria",
            "direccion": "Calle Secundaria 456",
            "telefono": "+56987654321",
            "email": "bibliotecaria@bec.cl",
            "password": get_password_hash("biblio123"),
            "rol": "bibliotecario",
            "activo": True,
            "fecha_creacion": datetime.utcnow()
        },
        {
            "rut": "11111111-1",
            "nombres": "Juan",
            "apellidos": "Lector",
            "direccion": "Pasaje Los Libros 789",
            "telefono": "+56911111111",
            "email": "lector@example.com",
            "password": get_password_hash("lector123"),
            "rol": "lector",
            "activo": True,
            "fecha_creacion": datetime.utcnow()
        }
    ]
    
    result = await db.users.insert_many(users)
    print(f"✅ {len(result.inserted_ids)} usuarios creados")
    
    print("📚 Creando documentos de ejemplo...")
    
    # Documentos de ejemplo
    documents = [
        {
            "titulo": "Cien años de soledad",
            "autor": "Gabriel García Márquez",
            "editorial": "Editorial Sudamericana",
            "edicion": "Primera",
            "ano_edicion": 1967,
            "tipo": "libro",
            "categoria": "Novela"
        },
        {
            "titulo": "El Principito",
            "autor": "Antoine de Saint-Exupéry",
            "editorial": "Reynal & Hitchcock",
            "edicion": "Primera",
            "ano_edicion": 1943,
            "tipo": "libro",
            "categoria": "Fábula"
        },
        {
            "titulo": "1984",
            "autor": "George Orwell",
            "editorial": "Secker & Warburg",
            "edicion": "Primera",
            "ano_edicion": 1949,
            "tipo": "libro",
            "categoria": "Ciencia Ficción"
        },
        {
            "titulo": "Don Quijote de la Mancha",
            "autor": "Miguel de Cervantes",
            "editorial": "Francisco de Robles",
            "edicion": "Primera",
            "ano_edicion": 1605,
            "tipo": "libro",
            "categoria": "Novela"
        },
        {
            "titulo": "La Odisea",
            "autor": "Homero",
            "editorial": "Antigüedad Clásica",
            "edicion": "Traducción moderna",
            "ano_edicion": 2020,
            "tipo": "libro",
            "categoria": "Épica"
        }
    ]
    
    result = await db.documents.insert_many(documents)
    document_ids = result.inserted_ids
    print(f"✅ {len(document_ids)} documentos creados")
    
    print("📖 Creando ejemplares...")
    
    # Crear 2-3 ejemplares por documento
    items = []
    for doc_id in document_ids:
        for i in range(2):
            items.append({
                "document_id": str(doc_id),
                "estado": "disponible",
                "ubicacion": f"Estantería {(len(items) // 2) + 1}, Nivel {(i % 3) + 1}"
            })
    
    result = await db.items.insert_many(items)
    print(f"✅ {len(result.inserted_ids)} ejemplares creados")
    
    print("\n" + "="*50)
    print("✨ Base de datos inicializada correctamente!")
    print("="*50)
    print("\n📝 Usuarios de prueba:")
    print("\n1. Administrativo:")
    print("   Email: admin@bec.cl")
    print("   Password: admin123")
    print("\n2. Bibliotecario:")
    print("   Email: bibliotecaria@bec.cl")
    print("   Password: biblio123")
    print("\n3. Lector:")
    print("   Email: lector@example.com")
    print("   Password: lector123")
    print("\n" + "="*50)
    
    client.close()


if __name__ == "__main__":
    print("🚀 Inicializando base de datos BEC...")
    asyncio.run(init_database())

