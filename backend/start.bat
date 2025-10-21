@echo off
REM Script para iniciar el sistema BEC completo en Windows

echo 🚀 Iniciando Sistema de Préstamo BEC...

REM Verificar que Docker esté instalado
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Docker no está instalado
    exit /b 1
)

REM Verificar que Docker Compose esté instalado
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Docker Compose no está instalado
    exit /b 1
)

REM Crear archivo .env si no existe
if not exist .env (
    echo 📝 Creando archivo .env desde env.example...
    copy env.example .env
    echo ⚠️  Por favor, edita el archivo .env con tus configuraciones
)

REM Iniciar servicios con Docker Compose
echo 🐳 Iniciando contenedores Docker...
docker-compose up -d

REM Esperar a que MongoDB esté listo
echo ⏳ Esperando a que MongoDB esté listo...
timeout /t 5 /nobreak >nul

REM Verificar estado de los contenedores
echo.
echo 📊 Estado de los servicios:
docker-compose ps

echo.
echo ✨ Sistema iniciado correctamente!
echo.
echo 📚 URLs de acceso:
echo   - API Backend: http://localhost:8000
echo   - Documentación: http://localhost:8000/docs
echo   - MongoDB: localhost:27017
echo   - MinIO Console: http://localhost:9001
echo   - Grafana: http://localhost:3000
echo.
echo 🔧 Para inicializar la base de datos con datos de ejemplo, ejecuta:
echo   python scripts\init_db.py
echo.
echo 📋 Para ver los logs:
echo   docker-compose logs -f backend
echo.
echo 🛑 Para detener el sistema:
echo   docker-compose down
echo.

pause

