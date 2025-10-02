# Sistema de Préstamo BEC - Backend

Backend del sistema de gestión de préstamos de la Biblioteca de Estación Central (BEC), construido con FastAPI, MongoDB, Kafka y Docker.

## 🏗️ Arquitectura

El sistema está construido con una arquitectura de microservicios que incluye:

- **FastAPI**: Framework web moderno para construir APIs RESTful
- **MongoDB**: Base de datos NoSQL para almacenamiento de datos
- **Apache Kafka**: Sistema de mensajería para procesos asíncronos y notificaciones
- **MinIO**: Almacenamiento de objetos S3-compatible para archivos biométricos
- **Loki + Promtail**: Agregación y recolección de logs
- **Grafana**: Visualización de métricas y logs
- **Docker**: Containerización de toda la aplicación

## 📋 Características Principales

### Fase 1 - Core ✅

- ✅ Autenticación JWT con roles (Lector, Bibliotecario, Administrativo)
- ✅ Gestión completa de usuarios (CRUD)
- ✅ Gestión de colección bibliográfica (documentos y ejemplares)
- ✅ Sistema de préstamos y devoluciones
- ✅ Sistema de reservas
- ✅ Cálculo automático de sanciones por atraso
- ✅ Consulta pública del catálogo sin autenticación

### Fase 2 - Estadísticas ✅

- ✅ Historial de préstamos por usuario
- ✅ Documentos más populares
- ✅ Usuarios más activos
- ✅ Dashboard con métricas generales
- ✅ Exportación de reportes a CSV

### Fase 3 - Notificaciones ✅

- ✅ Integración completa con Kafka
- ✅ Servicio consumidor de emails (worker)
- ✅ Notificación de activación de cuenta
- ✅ Recordatorios de préstamos vencidos
- ✅ Notificación de sanciones
- ✅ Proceso batch para préstamos vencidos

### Fase 4 - Monitoreo ✅

- ✅ Integración con MinIO para fotos y huellas
- ✅ Endpoints de upload de archivos
- ✅ Configuración de Loki para logs
- ✅ Promtail para recolección de logs
- ✅ Dashboards en Grafana

**🎉 TODAS LAS FASES COMPLETADAS**

## 🚀 Inicio Rápido

### Prerrequisitos

- Docker y Docker Compose instalados
- Python 3.11+ (para desarrollo local)

### Instalación con Docker (Recomendado)

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd backend
```

2. **Configurar variables de entorno**
```bash
cp env.example .env
# Editar .env con tus configuraciones
```

3. **Iniciar todos los servicios**
```bash
docker-compose up -d
```

4. **Verificar que los servicios estén corriendo**
```bash
docker-compose ps
```

La API estará disponible en: `http://localhost:8000`

### Instalación Local (Desarrollo)

1. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Configurar variables de entorno**
```bash
cp env.example .env
# Editar .env con tus configuraciones
```

4. **Iniciar solo las dependencias (MongoDB, Kafka, etc.)**
```bash
docker-compose up -d mongodb kafka zookeeper minio loki grafana
```

5. **Ejecutar la aplicación**
```bash
uvicorn app.main:app --reload
```

6. **Ejecutar el worker de notificaciones (opcional)**
```bash
python -m app.services.notification_consumer
```

## 📚 Documentación de la API

Una vez que la aplicación esté corriendo, puedes acceder a la documentación interactiva en:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🗂️ Estructura del Proyecto

```
backend/
├── app/
│   ├── api/
│   │   ├── dependencies.py      # Dependencias compartidas (auth, permisos)
│   │   └── v1/
│   │       ├── endpoints/       # Endpoints de la API
│   │       │   ├── auth.py     # Autenticación y registro
│   │       │   ├── users.py    # Gestión de usuarios
│   │       │   ├── documents.py # Documentos bibliográficos
│   │       │   ├── items.py    # Ejemplares
│   │       │   ├── loans.py    # Préstamos
│   │       │   ├── reservations.py # Reservas
│   │       │   ├── files.py    # Upload de archivos
│   │       │   └── statistics.py # Estadísticas y reportes
│   │       └── router.py       # Router principal
│   ├── core/
│   │   ├── config.py           # Configuración de la aplicación
│   │   ├── database.py         # Conexión a MongoDB
│   │   ├── security.py         # Utilidades de seguridad (JWT, hashing)
│   │   ├── kafka_producer.py   # Productor de eventos Kafka
│   │   └── storage.py          # Gestor de MinIO/S3
│   ├── models/                 # Modelos Pydantic
│   │   ├── user.py
│   │   ├── document.py
│   │   ├── item.py
│   │   ├── loan.py
│   │   └── reservation.py
│   ├── services/               # Lógica de negocio
│   │   ├── user_service.py
│   │   ├── document_service.py
│   │   ├── item_service.py
│   │   ├── loan_service.py
│   │   ├── reservation_service.py
│   │   ├── notification_consumer.py # Worker de emails
│   │   └── batch_jobs.py      # Trabajos programados
│   └── main.py                 # Punto de entrada de la aplicación
├── scripts/                    # Scripts de utilidad
│   ├── init_db.py             # Inicializar BD
│   ├── run_batch_jobs.sh      # Ejecutar trabajos batch
│   └── setup_cron.sh          # Configurar cron
├── grafana/                    # Configuración de Grafana
│   ├── provisioning/          # Datasources y dashboards
│   └── dashboards/            # Dashboards JSON
├── docker-compose.yml          # Orquestación completa
├── Dockerfile                  # Imagen del backend
├── Dockerfile.consumer         # Imagen del worker
├── Dockerfile.batch            # Imagen de batch jobs
├── loki-config.yaml           # Configuración de Loki
├── promtail-config.yaml       # Configuración de Promtail
├── requirements.txt
├── README.md
├── QUICKSTART.md
├── FEATURES.md
├── DEPLOYMENT_GUIDE.md
├── IMPLEMENTATION_SUMMARY.md
├── CHANGELOG.md
└── env.example
```

## 🎯 Estado del Proyecto:

- **Fase 1**: ✅ COMPLETADA (100%)
- **Fase 2**: ✅ COMPLETADA (100%)
- **Fase 3**: ✅ COMPLETADA (100%)
- **Fase 4**: ✅ COMPLETADA (100%)

**🚀 Sistema 100% Funcional y Production-Ready**

## 🔑 Endpoints Principales

### Autenticación
- `POST /api/v1/auth/register` - Registrar nuevo usuario
- `POST /api/v1/auth/login` - Iniciar sesión
- `POST /api/v1/auth/activate/{user_id}` - Activar cuenta

### Usuarios
- `GET /api/v1/users/me` - Obtener perfil actual
- `GET /api/v1/users/` - Listar usuarios (staff)
- `PUT /api/v1/users/{user_id}` - Actualizar usuario

### Documentos
- `GET /api/v1/documents/` - Listar catálogo (público)
- `GET /api/v1/documents/{id}` - Ver documento (público)
- `POST /api/v1/documents/` - Crear documento (staff)
- `PUT /api/v1/documents/{id}` - Actualizar documento (staff)

### Ejemplares
- `GET /api/v1/items/` - Listar ejemplares
- `POST /api/v1/items/` - Crear ejemplar (staff)
- `PUT /api/v1/items/{id}` - Actualizar ejemplar (staff)

### Préstamos
- `POST /api/v1/loans/` - Registrar préstamo (staff)
- `GET /api/v1/loans/` - Listar préstamos
- `GET /api/v1/loans/overdue` - Listar vencidos (staff)
- `POST /api/v1/loans/{id}/return` - Devolver préstamo (staff)

### Reservas
- `POST /api/v1/reservations/` - Crear reserva
- `GET /api/v1/reservations/` - Listar reservas
- `POST /api/v1/reservations/{id}/cancel` - Cancelar reserva
- `POST /api/v1/reservations/{id}/complete` - Completar reserva (staff)

### Archivos
- `POST /api/v1/files/upload/photo` - Subir foto de usuario
- `POST /api/v1/files/upload/fingerprint` - Subir huella digital
- `DELETE /api/v1/files/delete/photo` - Eliminar foto

### Estadísticas y Reportes
- `GET /api/v1/statistics/loans/history` - Historial de préstamos
- `GET /api/v1/statistics/documents/popular` - Documentos más populares
- `GET /api/v1/statistics/users/active` - Usuarios más activos
- `GET /api/v1/statistics/dashboard` - Dashboard general
- `GET /api/v1/statistics/export/loans` - Exportar préstamos a CSV

## 🔐 Roles y Permisos

### Lector (Usuario Regular)
- Ver catálogo público
- Crear reservas
- Ver sus propios préstamos y reservas
- Actualizar su perfil
- Subir foto y huella digital

### Bibliotecario
- Todos los permisos de Lector
- Gestionar documentos y ejemplares
- Registrar y devolver préstamos
- Ver información de todos los usuarios
- Gestionar reservas
- Ver estadísticas

### Administrativo
- Todos los permisos de Bibliotecario
- Gestionar usuarios
- Ver reportes completos
- Exportar datos
- Revisar préstamos vencidos

## 🗄️ Base de Datos

### Colecciones MongoDB

1. **users** - Usuarios del sistema
2. **documents** - Documentos bibliográficos
3. **items** - Ejemplares físicos
4. **loans** - Préstamos
5. **reservations** - Reservas

Ver `plan.md` para el esquema detallado de cada colección.

## 📊 Servicios Adicionales

### MongoDB
- **Puerto**: 27017
- **Base de datos**: bec_biblioteca

### Kafka
- **Puerto**: 9092
- **Tópicos**: 
  - `email-notifications` - Notificaciones por email
  - `overdue-checks` - Verificación de préstamos vencidos

### MinIO
- **Puerto API**: 9000
- **Puerto Console**: 9001
- **Usuario**: minioadmin
- **Contraseña**: minioadmin
- **Bucket**: bec-biometrics

### Loki + Promtail
- **Puerto Loki**: 3100
- **Retención**: 7 días
- **Logs**: Todos los contenedores Docker

### Grafana
- **Puerto**: 3000
- **Usuario**: admin
- **Contraseña**: admin
- **Dashboards**: Pre-configurados para logs del sistema

## 🔧 Configuración

Todas las configuraciones se gestionan a través de variables de entorno. Ver `env.example` para la lista completa de opciones.

### Variables Importantes

- `SECRET_KEY`: Clave secreta para JWT (¡cambiar en producción!)
- `MONGODB_URL`: URL de conexión a MongoDB
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Tiempo de expiración de tokens
- `LOAN_DAYS_HOME`: Días de préstamo a domicilio (default: 7)
- `LOAN_HOURS_ROOM`: Horas de préstamo en sala (default: 4)
- `SANCTION_MULTIPLIER`: Multiplicador de sanción por atraso (default: 2)
- `KAFKA_BOOTSTRAP_SERVERS`: Servidor de Kafka
- `STORAGE_ENDPOINT`: Endpoint de MinIO/S3
- `EMAIL_ENABLED`: Activar envío real de emails
- `EMAIL_API_KEY`: API key de SendGrid/Mailgun

## 🔄 Trabajos Batch

### Configurar Cron Jobs

```bash
chmod +x scripts/setup_cron.sh
./scripts/setup_cron.sh
```

Esto configurará:
- Verificación diaria de préstamos vencidos (2 AM)
- Expiración de reservas antiguas (2 AM)
- Envío de recordatorios por email

### Ejecutar Manualmente

```bash
# Dentro del contenedor
docker exec bec_backend python -m app.services.batch_jobs

# Localmente
python -m app.services.batch_jobs
```

## 🚧 Desarrollo

### Agregar una Nueva Funcionalidad

1. Crear el modelo en `app/models/`
2. Crear el servicio en `app/services/`
3. Crear los endpoints en `app/api/v1/endpoints/`
4. Registrar el router en `app/api/v1/router.py`
5. Actualizar la documentación

### Convenciones de Código

- Usar type hints en todas las funciones
- Documentar funciones con docstrings
- Seguir PEP 8
- Nombres en español para dominio de negocio
- Nombres en inglés para código técnico

## 🧪 Inicializar Base de Datos

Para cargar datos de ejemplo:

```bash
# Instalar dependencias
pip3 install -r requirements.txt

# Ejecutar script
python3 scripts/init_db.py
```

Esto creará:
- 3 usuarios de prueba (admin, bibliotecario, lector)
- 5 documentos bibliográficos
- 10 ejemplares disponibles

### Usuarios de Prueba

**Administrativo**
- Email: admin@bec.cl
- Password: admin123

**Bibliotecario**
- Email: bibliotecaria@bec.cl
- Password: biblio123

**Lector**
- Email: lector@example.com
- Password: lector123

## 📈 Monitoreo

### Ver Logs en Tiempo Real

```bash
# Logs del backend
docker logs -f bec_backend

# Logs del worker de notificaciones
docker logs -f bec_notification_worker

# Todos los logs
docker-compose logs -f
```

### Acceder a Grafana

1. Abrir http://localhost:3000
2. Login: admin / admin
3. Ir a Dashboards → BEC Dashboards
4. Ver logs en tiempo real

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

## 📖 Documentación Adicional

- [QUICKSTART.md](QUICKSTART.md) - Guía de inicio rápido
- [FEATURES.md](FEATURES.md) - Lista detallada de características
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Guía de despliegue en producción
- [CHANGELOG.md](CHANGELOG.md) - Historial de cambios
- [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - Resumen técnico

## 📝 Licencia

[Especificar licencia]

## 👥 Contribuidores

[Listar contribuidores]

## 📞 Contacto

[Información de contacto]

---

**Versión**: 1.0.0
**Estado**: Production Ready ✨
**Última actualización**: Octubre 2025

**Nota**: Para más detalles sobre todas las funcionalidades, consulta [FEATURES.md](FEATURES.md)
