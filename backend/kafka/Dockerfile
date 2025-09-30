FROM bitnami/kafka:latest

# Exponer puertos necesarios
EXPOSE 9092 9093

# Health check para verificar que Kafka está funcionando
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD kafka-topics.sh --bootstrap-server localhost:9092 --list

# Los configurations se pasan via environment variables en docker-compose
