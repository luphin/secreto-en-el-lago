#!/bin/bash

# Script para iniciar el sistema BEC completo

echo "🚀 Iniciando Sistema de Préstamo BEC..."

# Verificar que Docker esté instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker no está instalado"
    exit 1
fi

# Verificar que Docker Compose esté instalado
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Error: Docker Compose no está instalado"
    exit 1
fi

# Crear archivo .env si no existe
if [ ! -f .env ]; then
    echo "📝 Creando archivo .env desde env.example..."
    cp env.example .env
    echo "⚠️  Por favor, edita el archivo .env con tus configuraciones"
fi

# Iniciar servicios con Docker Compose
echo "🐳 Iniciando contenedores Docker..."
docker-compose up -d

# Esperar a que MongoDB esté listo
echo "⏳ Esperando a que MongoDB esté listo..."
sleep 5

# Verificar estado de los contenedores
echo ""
echo "📊 Estado de los servicios:"
docker-compose ps

echo ""
echo "✨ Sistema iniciado correctamente!"
echo ""
echo "📚 URLs de acceso:"
echo "  - API Backend: http://localhost:8000"
echo "  - Documentación: http://localhost:8000/docs"
echo "  - MongoDB: localhost:27017"
echo "  - MinIO Console: http://localhost:9001"
echo "  - Grafana: http://localhost:3000"
echo ""
echo "🔧 Para inicializar la base de datos con datos de ejemplo, ejecuta:"
echo "  python scripts/init_db.py"
echo ""
echo "📋 Para ver los logs:"
echo "  docker-compose logs -f backend"
echo ""
echo "🛑 Para detener el sistema:"
echo "  docker-compose down"
echo ""

