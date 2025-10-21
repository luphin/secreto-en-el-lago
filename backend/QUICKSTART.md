# Guía de Inicio Rápido - Sistema BEC

Esta guía te ayudará a poner en marcha el Sistema de Préstamo BEC en menos de 5 minutos.

## 📋 Prerrequisitos

Antes de comenzar, asegúrate de tener instalado:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (versión 20.10 o superior)
- [Git](https://git-scm.com/downloads)

## 🚀 Pasos de Instalación

### 1. Clonar el Repositorio

```bash
git clone <repository-url>
cd backend
```

### 2. Iniciar el Sistema

#### En Linux/Mac:

```bash
chmod +x start.sh
./start.sh
```

#### En Windows:

```bash
start.bat
```

O manualmente:

```bash
# Crear archivo de configuración
copy env.example .env

# Iniciar todos los servicios
docker-compose up -d
```

### 3. Inicializar la Base de Datos (Opcional)

Para cargar datos de ejemplo:

```bash
# Instalar todas las dependencias del proyecto
pip install -r requirements.txt

# O si prefieres usar Python 3 explícitamente
pip3 install -r requirements.txt

# Ejecutar script de inicialización
python3 scripts/init_db.py
```

Esto creará:
- 3 usuarios de prueba (admin, bibliotecario, lector)
- 5 documentos bibliográficos
- 10 ejemplares disponibles

## 🎉 ¡Listo!

El sistema ya está corriendo. Accede a:

- **API**: http://localhost:8000
- **Documentación Interactiva**: http://localhost:8000/docs

## 🔐 Usuarios de Prueba

Después de ejecutar el script de inicialización, puedes usar:

### Administrativo
- **Email**: admin@bec.cl
- **Password**: admin123

### Bibliotecario
- **Email**: bibliotecaria@bec.cl
- **Password**: biblio123

### Lector
- **Email**: lector@example.com
- **Password**: lector123

## 🧪 Probar la API

### 1. Iniciar Sesión

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "lector@example.com",
    "password": "lector123"
  }'
```

Esto te devolverá un `access_token` que deberás usar en las siguientes peticiones.

### 2. Ver Catálogo (No requiere autenticación)

```bash
curl "http://localhost:8000/api/v1/documents/"
```

### 3. Ver Mi Perfil

```bash
curl "http://localhost:8000/api/v1/users/me" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjhkZTEzNzYxZThhY2QxYTIxZDE1ZmUyIiwiZW1haWwiOiJsZWN0b3JAZXhhbXBsZS5jb20iLCJleHAiOjE3NTkzODYzMDEsInR5cGUiOiJhY2Nlc3MifQ.0mHNJLiiU4dhIpwUlpVIFNeKPN7rKcV-yS4olrJqlh0"
```

## 📚 Explorar la API

La forma más fácil de explorar todas las funcionalidades es usando la documentación interactiva:

1. Visita: http://localhost:8000/docs
2. Haz clic en "Authorize" (🔒)
3. Inicia sesión con alguno de los usuarios de prueba
4. Explora todos los endpoints disponibles

## 🐛 Solución de Problemas

### Puerto ya en uso

Si el puerto 8000 ya está en uso, puedes cambiarlo en `docker-compose.yml`:

```yaml
services:
  backend:
    ports:
      - "8001:8000"  # Cambiar el primer número
```

### MongoDB no inicia

Asegúrate de tener suficiente espacio en disco y que el puerto 27017 esté libre.

### Ver logs

```bash
# Ver logs de todos los servicios
docker-compose logs -f

# Ver logs solo del backend
docker-compose logs -f backend
```

## 🛑 Detener el Sistema

```bash
docker-compose down
```

Para detener y eliminar todos los datos:

```bash
docker-compose down -v
```

## 📖 Siguientes Pasos

- Lee la [documentación completa](README.md)
- Explora el [plan de desarrollo](plan.md)
- Revisa los [endpoints disponibles](http://localhost:8000/docs)

## 💡 Consejos

1. **Desarrollo Local**: Si vas a modificar el código, los cambios se reflejarán automáticamente gracias al hot-reload de FastAPI.

2. **Base de Datos**: Los datos persisten entre reinicios. Usa `docker-compose down -v` si quieres empezar desde cero.

3. **Monitoreo**: Accede a Grafana (http://localhost:3000) para ver métricas y logs del sistema.

4. **Almacenamiento**: MinIO está disponible en http://localhost:9001 para gestionar archivos.

## 🆘 ¿Necesitas Ayuda?

- Revisa los logs: `docker-compose logs -f`
- Verifica el estado: `docker-compose ps`
- Reinicia un servicio: `docker-compose restart backend`

---

¡Disfruta usando el Sistema de Préstamo BEC! 📚✨

