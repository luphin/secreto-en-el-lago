"""
Configuración y gestión de la conexión a MongoDB
"""
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)


class Database:
    """Singleton para la conexión a MongoDB"""
    client: AsyncIOMotorClient = None
    db = None


db_instance = Database()


async def connect_to_mongo():
    """Conecta a MongoDB al inicio de la aplicación"""
    try:
        logger.info(f"Conectando a MongoDB: {settings.MONGODB_URL}")
        db_instance.client = AsyncIOMotorClient(settings.MONGODB_URL)
        db_instance.db = db_instance.client[settings.MONGODB_DB_NAME]
        
        # Verificar la conexión
        await db_instance.client.admin.command('ping')
        logger.info("✓ Conexión a MongoDB establecida exitosamente")
        
        # Crear índices
        await create_indexes()
        
    except ConnectionFailure as e:
        logger.error(f"✗ Error al conectar a MongoDB: {e}")
        raise


async def close_mongo_connection():
    """Cierra la conexión a MongoDB al apagar la aplicación"""
    if db_instance.client:
        logger.info("Cerrando conexión a MongoDB")
        db_instance.client.close()
        logger.info("✓ Conexión a MongoDB cerrada")


async def create_indexes():
    """Crea índices en las colecciones para optimizar consultas"""
    try:
        # Índices para users
        await db_instance.db.users.create_index("email", unique=True)
        await db_instance.db.users.create_index("rut", unique=True)
        await db_instance.db.users.create_index("rol")
        
        # Índices para documents
        await db_instance.db.documents.create_index("titulo")
        await db_instance.db.documents.create_index("autor")
        await db_instance.db.documents.create_index("categoria")
        await db_instance.db.documents.create_index([
            ("titulo", "text"),
            ("autor", "text"),
            ("categoria", "text")
        ])
        
        # Índices para items
        await db_instance.db.items.create_index("document_id")
        await db_instance.db.items.create_index("estado")
        
        # Índices para loans
        await db_instance.db.loans.create_index("user_id")
        await db_instance.db.loans.create_index("item_id")
        await db_instance.db.loans.create_index("estado")
        await db_instance.db.loans.create_index("fecha_devolucion_pactada")
        
        # Índices para reservations
        await db_instance.db.reservations.create_index("user_id")
        await db_instance.db.reservations.create_index("document_id")
        await db_instance.db.reservations.create_index("estado")
        
        logger.info("✓ Índices creados exitosamente")
    except Exception as e:
        logger.error(f"Error al crear índices: {e}")


def get_database():
    """Retorna la instancia de la base de datos"""
    return db_instance.db

