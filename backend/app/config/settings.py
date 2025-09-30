from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # MongoDB
    mongodb_url: str
    database_name: str = "biblioteca_municipal"

    # JWT
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 30

    # Email
    email_host: str
    email_port: int
    email_username: str
    email_password: str
    email_name: Optional[str] = "Biblioteca Municipal"
    email_simulation: bool = False

    # Kafka
    kafka_bootstrap_servers: str = "localhost:9092"
    kafka_topic_loans: str = "library-loans"
    kafka_topic_notifications: str = "library-notifications"

    # Application
    debug: bool = False
    allowed_hosts: str = "localhost,127.0.0.1"
    
    # Grafana
    grafana_password: Optional[str] = "admin"

    class Config:
        env_file = ".env"
        extra = "ignore"  # Ignorar campos extra del .env que no están definidos


settings = Settings()
