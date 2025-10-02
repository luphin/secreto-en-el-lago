"""
Configuración de la aplicación
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """Configuración principal de la aplicación"""
    
    # Información del proyecto
    PROJECT_NAME: str = "Sistema de Préstamo BEC"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    
    # MongoDB
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "bec_biblioteca"
    
    # Seguridad
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Kafka (para notificaciones asíncronas)
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    KAFKA_EMAIL_TOPIC: str = "email-notifications"
    KAFKA_OVERDUE_TOPIC: str = "overdue-checks"
    
    # Almacenamiento de archivos (S3/MinIO)
    STORAGE_ENDPOINT: str = "http://localhost:9000"
    STORAGE_ACCESS_KEY: str = "minioadmin"
    STORAGE_SECRET_KEY: str = "minioadmin"
    STORAGE_BUCKET_NAME: str = "bec-biometrics"
    
    # Email service (para notificaciones)
    EMAIL_ENABLED: bool = False
    EMAIL_API_KEY: str = ""
    EMAIL_FROM: str = "noreply@bec.cl"
    
    # Préstamos - Configuración de negocio
    LOAN_DAYS_HOME: int = 7  # Días de préstamo a domicilio
    LOAN_HOURS_ROOM: int = 4  # Horas de préstamo en sala
    SANCTION_MULTIPLIER: int = 2  # Días de sanción = días de atraso * multiplicador
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )


settings = Settings()

