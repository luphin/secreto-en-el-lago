#!/usr/bin/env python3
"""
Script de inicialización de la base de datos para el Sistema de Biblioteca Municipal
Crea las colecciones necesarias y datos iniciales
"""

import asyncio
import os
import sys
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import uuid

# Agregar el directorio raíz al path para importar los modelos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config.settings import settings
from app.schemas.user import UserRole
from app.schemas.document import DocumentType, DocumentCategory, MediaFormat

class DatabaseInitializer:
    def __init__(self):
        self.client = None
        self.db = None
        
    async def connect(self):
        """Conectar a la base de datos"""
        try:
            self.client = AsyncIOMotorClient(settings.mongodb_url)
            self.db = self.client[settings.database_name]
            print("✅ Conectado a MongoDB Atlas")
            return True
        except Exception as e:
            print(f"❌ Error conectando a MongoDB: {e}")
            return False

    async def create_collections(self):
        """Crear las colecciones necesarias"""
        collections = [
            "users", "documents", "ejemplares", "loans", 
            "requests", "notifications", "sanciones", "system_alerts"
        ]
        
        existing_collections = await self.db.list_collection_names()
        
        for collection in collections:
            if collection not in existing_collections:
                await self.db.create_collection(collection)
                print(f"✅ Colección '{collection}' creada")
            else:
                print(f"📁 Colección '{collection}' ya existe")

    async def create_indexes(self):
        """Crear índices para optimizar consultas"""
        # Índices para usuarios
        await self.db.users.create_index("email", unique=True)
        await self.db.users.create_index("rut", unique=True)
        await self.db.users.create_index("status")
        await self.db.users.create_index("role")
        
        # Índices para documentos
        await self.db.documents.create_index("titulo")
        await self.db.documents.create_index("autor")
        await self.db.documents.create_index("tipo")
        await self.db.documents.create_index("categoria")
        await self.db.documents.create_index([("titulo", "text"), ("autor", "text")])
        
        # Índices para ejemplares
        await self.db.ejemplares.create_index("documento_id")
        await self.db.ejemplares.create_index("estado")
        await self.db.ejemplares.create_index("codigo_ubicacion", unique=True)
        
        # Índices para préstamos
        await self.db.loans.create_index("usuario_id")
        await self.db.loans.create_index("estado_general")
        await self.db.loans.create_index("fecha_devolucion")
        await self.db.loans.create_index([("usuario_id", 1), ("estado_general", 1)])
        
        # Índices para solicitudes
        await self.db.requests.create_index("usuario_id")
        await self.db.requests.create_index("tipo_solicitud")
        await self.db.requests.create_index("estado")
        await self.db.requests.create_index("fecha_solicitud")
        
        print("✅ Índices creados exitosamente")

    async def create_initial_users(self):
        """Crear usuarios iniciales del sistema"""
        users_data = [
            {
                "id": str(uuid.uuid4()),
                "rut": "12345678-9",
                "names": "Admin",
                "last_names": "Sistema",
                "email": "admin@biblioteca.cl",
                "phone": "+56912345678",
                "address": "Plaza Central 123, Estación Central",
                "role": UserRole.ADMIN.value,
                "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # password: secret
                "status": "active",
                "email_verified": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "id": str(uuid.uuid4()),
                "rut": "18765432-1",
                "names": "Ana",
                "last_names": "Bibliotecaria",
                "email": "bibliotecario@biblioteca.cl",
                "phone": "+56987654321",
                "address": "Av. Principal 456, Estación Central",
                "role": UserRole.LIBRARIAN.value,
                "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
                "status": "active",
                "email_verified": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "id": str(uuid.uuid4()),
                "rut": "20456789-2",
                "names": "Carlos",
                "last_names": "Administrativo",
                "email": "administrativo@biblioteca.cl",
                "phone": "+56955556666",
                "address": "Calle Secundaria 789, Estación Central",
                "role": UserRole.ADMINISTRATIVE.value,
                "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
                "status": "active",
                "email_verified": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "id": str(uuid.uuid4()),
                "rut": "15678901-3",
                "names": "María",
                "last_names": "González Pérez",
                "email": "usuario@biblioteca.cl",
                "phone": "+56944445555",
                "address": "Pasaje Los Olivos 321, Estación Central",
                "role": UserRole.USER.value,
                "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
                "status": "active",
                "email_verified": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        ]

        for user in users_data:
            existing_user = await self.db.users.find_one({"email": user["email"]})
            if not existing_user:
                await self.db.users.insert_one(user)
                print(f"✅ Usuario creado: {user['email']}")
            else:
                print(f"📋 Usuario ya existe: {user['email']}")

    async def create_sample_documents(self):
        """Crear documentos de ejemplo"""
        documents_data = [
            {
                "id": str(uuid.uuid4()),
                "titulo": "Cien años de soledad",
                "autor": "Gabriel García Márquez",
                "tipo": DocumentType.LIBRO.value,
                "categoria": DocumentCategory.LITERATURA_UNIVERSAL.value,
                "editorial": "Sudamericana",
                "edicion": "Primera edición",
                "ano_edicion": 1967,
                "isbn": "978-8437604947",
                "descripcion": "Novela del realismo mágico que narra la historia de la familia Buendía en Macondo",
                "numero_ejemplares": 5,
                "ejemplares_disponibles": 5,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "id": str(uuid.uuid4()),
                "titulo": "Poema de Chile",
                "autor": "Gabriela Mistral",
                "tipo": DocumentType.LIBRO.value,
                "categoria": DocumentCategory.LITERATURA_CHILENA.value,
                "editorial": "Editorial Universitaria",
                "edicion": "Edición especial",
                "ano_edicion": 1967,
                "isbn": "978-9561112581",
                "descripcion": "Colección de poemas que recorren la geografía y cultura de Chile",
                "numero_ejemplares": 3,
                "ejemplares_disponibles": 3,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "id": str(uuid.uuid4()),
                "titulo": "Introducción a la Programación con Python",
                "autor": "John Smith",
                "tipo": DocumentType.LIBRO.value,
                "categoria": DocumentCategory.TECNICO_ESPANOL.value,
                "editorial": "Tech Publishing",
                "edicion": "Segunda edición",
                "ano_edicion": 2022,
                "isbn": "978-0123456789",
                "descripcion": "Guía completa para aprender programación desde cero usando Python",
                "numero_ejemplares": 4,
                "ejemplares_disponibles": 4,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "id": str(uuid.uuid4()),
                "titulo": "The Lord of the Rings: The Fellowship of the Ring",
                "autor": "J.R.R. Tolkien",
                "tipo": DocumentType.LIBRO.value,
                "categoria": DocumentCategory.LITERATURA_INGLESA.value,
                "editorial": "George Allen & Unwin",
                "edicion": "Collector's edition",
                "ano_edicion": 1954,
                "isbn": "978-0544003415",
                "descripcion": "Primera parte de la épica trilogía de la Tierra Media",
                "numero_ejemplares": 2,
                "ejemplares_disponibles": 2,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "id": str(uuid.uuid4()),
                "titulo": "Historia de Chile",
                "autor": "Sergio Villalobos",
                "tipo": DocumentType.LIBRO.value,
                "categoria": DocumentCategory.HISTORIA.value,
                "editorial": "Editorial Universitaria",
                "edicion": "Tercera edición",
                "ano_edicion": 2018,
                "isbn": "978-9561123458",
                "descripcion": "Compendio histórico completo de Chile desde la prehistoria hasta el siglo XXI",
                "numero_ejemplares": 3,
                "ejemplares_disponibles": 3,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "id": str(uuid.uuid4()),
                "titulo": "Documental: Naturaleza Chilena",
                "autor": "National Geographic",
                "tipo": DocumentType.VIDEO.value,
                "categoria": DocumentCategory.DOCUMENTAL.value,
                "formato_medio": MediaFormat.DVD.value,
                "duracion": 120,
                "descripcion": "Documental sobre la diversidad natural de Chile",
                "numero_ejemplares": 2,
                "ejemplares_disponibles": 2,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "id": str(uuid.uuid4()),
                "titulo": "Música Folclórica Chilena",
                "autor": "Varios Artistas",
                "tipo": DocumentType.AUDIO.value,
                "categoria": DocumentCategory.MUSICA.value,
                "formato_medio": MediaFormat.CD.value,
                "duracion": 75,
                "descripcion": "Colección de música folclórica tradicional chilena",
                "numero_ejemplares": 3,
                "ejemplares_disponibles": 3,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        ]

        for doc in documents_data:
            existing_doc = await self.db.documents.find_one({"titulo": doc["titulo"], "autor": doc["autor"]})
            if not existing_doc:
                await self.db.documents.insert_one(doc)
                print(f"✅ Documento creado: {doc['titulo']}")
                
                # Crear ejemplares para este documento
                await self._create_ejemplares_for_document(doc["id"], doc["numero_ejemplares"])
            else:
                print(f"📋 Documento ya existe: {doc['titulo']}")

    async def _create_ejemplares_for_document(self, document_id: str, num_ejemplares: int):
        """Crear ejemplares para un documento"""
        for i in range(num_ejemplares):
            ejemplar = {
                "id": str(uuid.uuid4()),
                "documento_id": document_id,
                "codigo_ubicacion": f"DOC-{document_id[:8]}-{i+1:03d}",
                "estado": "disponible",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            await self.db.ejemplares.insert_one(ejemplar)
        print(f"  📚 {num_ejemplares} ejemplares creados para documento {document_id[:8]}")

    async def create_sample_loans(self):
        """Crear algunos préstamos de ejemplo"""
        # Obtener usuario de prueba
        user = await self.db.users.find_one({"email": "usuario@biblioteca.cl"})
        if not user:
            print("❌ Usuario de prueba no encontrado para crear préstamos")
            return

        # Obtener algunos ejemplares disponibles
        ejemplares = await self.db.ejemplares.find({"estado": "disponible"}).limit(2).to_list(length=2)
        
        if len(ejemplares) < 2:
            print("❌ No hay suficientes ejemplares disponibles para crear préstamos de ejemplo")
            return

        loan_data = {
            "id": str(uuid.uuid4()),
            "usuario_id": user["id"],
            "tipo_prestamo": "domicilio",
            "fecha_prestamo": datetime.utcnow() - timedelta(days=5),
            "hora_prestamo": "10:00",
            "fecha_devolucion": datetime.utcnow() + timedelta(days=2),
            "hora_devolucion": "20:00",
            "items": [
                {
                    "ejemplar_id": ejemplares[0]["id"],
                    "fecha_devolucion": datetime.utcnow() + timedelta(days=2),
                    "hora_devolucion": "20:00",
                    "estado": "activo"
                },
                {
                    "ejemplar_id": ejemplares[1]["id"],
                    "fecha_devolucion": datetime.utcnow() + timedelta(days=2),
                    "hora_devolucion": "20:00",
                    "estado": "activo"
                }
            ],
            "estado_general": "activo",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        await self.db.loans.insert_one(loan_data)
        
        # Actualizar estado de los ejemplares
        for ejemplar in ejemplares:
            await self.db.ejemplares.update_one(
                {"id": ejemplar["id"]},
                {"$set": {"estado": "prestado_domicilio", "updated_at": datetime.utcnow()}}
            )
        
        # Actualizar contadores de documentos
        for ejemplar in ejemplares:
            await self.db.documents.update_one(
                {"id": ejemplar["documento_id"]},
                {"$inc": {"ejemplares_disponibles": -1}}
            )

        print("✅ Préstamo de ejemplo creado")

    async def initialize(self):
        """Ejecutar toda la inicialización"""
        print("🚀 Iniciando inicialización de la base de datos...")
        
        if not await self.connect():
            return False

        try:
            # Crear colecciones
            await self.create_collections()
            
            # Crear índices
            await self.create_indexes()
            
            # Crear datos iniciales
            await self.create_initial_users()
            await self.create_sample_documents()
            await self.create_sample_loans()
            
            print("\n🎉 Inicialización completada exitosamente!")
            return True
            
        except Exception as e:
            print(f"❌ Error durante la inicialización: {e}")
            return False
        finally:
            if self.client:
                self.client.close()

async def main():
    """Función principal"""
    initializer = DatabaseInitializer()
    success = await initializer.initialize()
    
    if success:
        print("\n📊 Resumen de la base de datos:")
        print(f"   📚 Documentos: {await initializer.db.documents.count_documents({})}")
        print(f"   👥 Usuarios: {await initializer.db.users.count_documents({})}")
        print(f"   📖 Ejemplares: {await initializer.db.ejemplares.count_documents({})}")
        print(f"   🔄 Préstamos: {await initializer.db.loans.count_documents({})}")
        sys.exit(0)
    else:
        print("\n💥 La inicialización falló")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
