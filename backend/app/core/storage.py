"""
Gestión de almacenamiento de archivos con MinIO
"""
import logging
from typing import Optional, BinaryIO
from datetime import timedelta
import io
from minio import Minio
from minio.error import S3Error

from app.core.config import settings

logger = logging.getLogger(__name__)


class StorageManager:
    """Gestor de almacenamiento de archivos con MinIO"""
    
    def __init__(self):
        self.client: Optional[Minio] = None
        self.bucket_name = settings.STORAGE_BUCKET_NAME
        self._initialized = False
    
    def initialize(self):
        """Inicializa la conexión con MinIO"""
        if self._initialized:
            return
        
        try:
            # Extraer host y puerto del endpoint
            endpoint = settings.STORAGE_ENDPOINT.replace("http://", "").replace("https://", "")
            secure = settings.STORAGE_ENDPOINT.startswith("https://")
            
            self.client = Minio(
                endpoint,
                access_key=settings.STORAGE_ACCESS_KEY,
                secret_key=settings.STORAGE_SECRET_KEY,
                secure=secure
            )
            
            # Crear bucket si no existe
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                logger.info(f"✓ Bucket '{self.bucket_name}' creado en MinIO")
            
            self._initialized = True
            logger.info("✓ Conexión a MinIO establecida")
        except S3Error as e:
            logger.error(f"✗ Error al conectar con MinIO: {e}")
            logger.warning("⚠ Sistema funcionará sin almacenamiento de archivos")
    
    async def upload_file(
        self,
        file_data: BinaryIO,
        object_name: str,
        content_type: str = "application/octet-stream"
    ) -> Optional[str]:
        """
        Sube un archivo a MinIO
        
        Args:
            file_data: Datos del archivo
            object_name: Nombre del objeto en el storage
            content_type: Tipo MIME del archivo
            
        Returns:
            URL del archivo subido o None si falla
        """
        if not self.client or not self._initialized:
            logger.warning("Cliente MinIO no disponible")
            return None
        
        try:
            # Obtener tamaño del archivo
            file_data.seek(0, 2)  # Ir al final
            file_size = file_data.tell()
            file_data.seek(0)  # Volver al inicio
            
            # Subir archivo
            self.client.put_object(
                self.bucket_name,
                object_name,
                file_data,
                file_size,
                content_type=content_type
            )
            
            # Generar URL pública (temporal)
            url = self.client.presigned_get_object(
                self.bucket_name,
                object_name,
                expires=timedelta(days=365)  # URL válida por 1 año
            )
            
            logger.info(f"✓ Archivo subido: {object_name}")
            return url
        except S3Error as e:
            logger.error(f"✗ Error al subir archivo: {e}")
            return None
    
    async def upload_photo(self, file_data: BinaryIO, user_id: str) -> Optional[str]:
        """Sube una foto de usuario"""
        object_name = f"photos/{user_id}.jpg"
        return await self.upload_file(file_data, object_name, "image/jpeg")
    
    async def upload_fingerprint(self, file_data: BinaryIO, user_id: str) -> Optional[str]:
        """Sube datos de huella digital"""
        object_name = f"fingerprints/{user_id}.dat"
        return await self.upload_file(file_data, object_name, "application/octet-stream")
    
    async def delete_file(self, object_name: str) -> bool:
        """
        Elimina un archivo de MinIO
        
        Args:
            object_name: Nombre del objeto a eliminar
            
        Returns:
            True si se eliminó correctamente
        """
        if not self.client or not self._initialized:
            logger.warning("Cliente MinIO no disponible")
            return False
        
        try:
            self.client.remove_object(self.bucket_name, object_name)
            logger.info(f"✓ Archivo eliminado: {object_name}")
            return True
        except S3Error as e:
            logger.error(f"✗ Error al eliminar archivo: {e}")
            return False
    
    async def get_file_url(self, object_name: str, expires: timedelta = timedelta(hours=1)) -> Optional[str]:
        """
        Obtiene una URL temporal para acceder a un archivo
        
        Args:
            object_name: Nombre del objeto
            expires: Tiempo de expiración de la URL
            
        Returns:
            URL temporal o None si falla
        """
        if not self.client or not self._initialized:
            logger.warning("Cliente MinIO no disponible")
            return None
        
        try:
            url = self.client.presigned_get_object(
                self.bucket_name,
                object_name,
                expires=expires
            )
            return url
        except S3Error as e:
            logger.error(f"✗ Error al generar URL: {e}")
            return None


# Instancia global del gestor de almacenamiento
storage_manager = StorageManager()

