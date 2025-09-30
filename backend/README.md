# Sistema de Biblioteca Municipal - Backend

Backend desarrollado con FastAPI para el sistema de préstamos de la Biblioteca Municipal de Estación Central.

## Características

- **Gestión de Usuarios**: Registro, autenticación y roles (Admin, Bibliotecario, Administrativo, Usuario)
- **Catálogo Digital**: Búsqueda y consulta de documentos y multimedia
- **Sistema de Préstamos**: Préstamos en sala y a domicilio con control de vencimientos
- **Reservas**: Sistema de reservas de documentos
- **Notificaciones**: Emails automáticos para verificación, recordatorios y sanciones
- **Monitoreo**: Dashboard Grafana con métricas en tiempo real
- **Logs Estructurados**: Sistema de logging con Loki y Prometheus
- **Mensajería**: Kafka para procesamiento asíncrono de eventos ([Documentación email](docs/email.md))

## Arquitectura

```bash
biblioteca-backend/
├── app/
│ ├── config/ # Configuración y base de datos
│ ├── models/ # Modelos de Pydantic
│ ├── schemas/ # Esquemas y tipos de datos
│ ├── services/ # Lógica de negocio
│ ├── routes/ # Endpoints de la API
│ ├── middleware/ # Middleware de autenticación y logging
│ ├── monitoring/ # Métricas y monitoreo
│ └── utils/ # Utilidades y helpers
├── scripts/ # Scripts de BD e inicialización
├── kafka/ # Configuración de Kafka
├── grafana/ # Dashboards y configuración
└── monitoring/ # Configuración de Prometheus y Loki
```

## Prerrequisitos

- Docker y Docker Compose
- Python 3.11+
- MongoDB Atlas (o local)
- Cuenta de email para notificaciones

## Instalación

1. Clonar el repositorio

```bash
git clone <repository-url>
cd biblioteca-backend
```

2. Configurar variables de entorno

Agregar `.env`

3. Construir y ejecutar con Docker

```bash
docker-compose up --build
```

## Usos

### Servicios disponibles

- API Backend: http://localhost:8000
- Documentación API: http://localhost:8000/docs
- Grafana: http://localhost:3000 (admin/admin123)
- Kafka UI: http://localhost:8080

### Usuarios de prueba

- Administrador: admin@biblioteca.cl / secret
- Bibliotecario: bibliotecario@biblioteca.cl / secret
- Administrativo: administrativo@biblioteca.cl / secret
- Usuario: usuario@biblioteca.cl / secret


## Ejemplos API

```bash
# Autenticación
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@biblioteca.cl&password=secret"

# Consultar catálogo
curl -X GET "http://localhost:8000/api/v1/documents/"

# Crear préstamo
curl -X POST "http://localhost:8000/api/v1/loans/" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "usuario_id": "user-id",
    "tipo_prestamo": "domicilio",
    "ejemplares_ids": ["ejemplar-id-1", "ejemplar-id-2"]
  }'
```

## Diagrama de clases

```mermaid
classDiagram
    class Usuario {
        +String id
        +String rut
        +String nombres
        +String apellidos
        +String email
        +String telefono
        +String direccion
        +UserRole rol
        +UserStatus estado
        +Boolean email_verificado
        +DateTime created_at
        +registrar()
        +autenticar()
        +actualizar()
    }

    class Documento {
        +String id
        +String titulo
        +String autor
        +DocumentType tipo
        +DocumentCategory categoria
        +MediaFormat formato_medio
        +String editorial
        +Integer ano_edicion
        +Integer numero_ejemplares
        +Integer ejemplares_disponibles
        +DateTime created_at
        +crear()
        +actualizar()
        +buscar()
    }

    class Ejemplar {
        +String id
        +String documento_id
        +String codigo_ubicacion
        +EjemplarStatus estado
        +DateTime created_at
        +marcar_prestado()
        +marcar_disponible()
    }

    class Prestamo {
        +String id
        +String usuario_id
        +LoanType tipo_prestamo
        +DateTime fecha_prestamo
        +DateTime fecha_devolucion
        +LoanStatus estado_general
        +List~LoanItem~ items
        +crear()
        +devolver()
        +extender()
        +calcular_vencimiento()
    }

    class Solicitud {
        +String id
        +String usuario_id
        +RequestType tipo_solicitud
        +RequestStatus estado
        +DateTime fecha_solicitud
        +List~RequestItem~ items
        +crear()
        +procesar()
        +cancelar()
    }

    class Sancion {
        +String id
        +String usuario_id
        +String prestamo_id
        +SancionType tipo
        +Integer dias_sancion
        +DateTime fecha_inicio
        +DateTime fecha_fin
        +SancionStatus estado
        +aplicar()
        +verificar()
    }

    class Notificacion {
        +String id
        +String usuario_id
        +NotificationType tipo
        +String asunto
        +String mensaje
        +NotificationStatus estado
        +enviar()
    }

    %% Relaciones principales
    Usuario "1" -- "*" Prestamo : realiza
    Usuario "1" -- "*" Solicitud : crea
    Usuario "1" -- "*" Sancion : recibe
    Usuario "1" -- "*" Notificacion : recibe
    
    Documento "1" -- "*" Ejemplar : contiene
    Ejemplar "1" -- "*" Prestamo : prestado_en
    Documento "1" -- "*" Solicitud : solicitado_en
    
    Prestamo "1" -- "*" Sancion : genera
    Prestamo "1" -- "*" Notificacion : notifica

    %% Relaciones con Enums
    Usuario --> UserRole : utiliza
    Usuario --> UserStatus : utiliza
    
    Documento --> DocumentType : utiliza
    Documento --> DocumentCategory : utiliza
    Documento --> MediaFormat : utiliza
    Documento --> DocumentStatus : utiliza
    
    Ejemplar --> EjemplarStatus : utiliza
    
    Prestamo --> LoanType : utiliza
    Prestamo --> LoanStatus : utiliza
    
    Solicitud --> RequestType : utiliza
    Solicitud --> RequestStatus : utiliza
    
    Sancion --> SancionType : utiliza
    Sancion --> SancionStatus : utiliza
    
    Notificacion --> NotificationType : utiliza
    Notificacion --> NotificationStatus : utiliza

    %% Definición de Enumeraciones
    class UserRole {
        <<enumeration>>
        ADMIN
        LIBRARIAN
        ADMINISTRATIVE
        USER
    }

    class UserStatus {
        <<enumeration>>
        PENDING
        ACTIVE
        INACTIVE
        SUSPENDED
    }

    class DocumentType {
        <<enumeration>>
        LIBRO
        AUDIO
        VIDEO
        REVISTA
        PERIODICO
    }

    class DocumentCategory {
        <<enumeration>>
        LITERATURA_CHILENA
        LITERATURA_ESPANOLA
        LITERATURA_INGLESA
        LITERATURA_UNIVERSAL
        TECNICO_ESPANOL
        TECNICO_INGLES
        CIENCIAS
        HISTORIA
        FILOSOFIA
        ARTE
        PELICULA
        DOCUMENTAL
        MUSICA
        AUDIOLIBRO
        SONIDOS
    }

    class MediaFormat {
        <<enumeration>>
        CASSETTE
        CD
        DVD
        BLURAY
        DIGITAL
        VINILO
    }

    class DocumentStatus {
        <<enumeration>>
        DISPONIBLE
        PRESTADO
        RESERVADO
        MANTENCION
        PERDIDO
    }

    class EjemplarStatus {
        <<enumeration>>
        DISPONIBLE
        PRESTADO_SALA
        PRESTADO_DOMICILIO
        RESERVADO
        MANTENCION
        PERDIDO
    }

    class LoanType {
        <<enumeration>>
        SALA
        DOMICILIO
    }

    class LoanStatus {
        <<enumeration>>
        ACTIVO
        DEVUELTO
        VENCIDO
        MORA
    }

    class RequestType {
        <<enumeration>>
        PRESTAMO
        RESERVA
    }

    class RequestStatus {
        <<enumeration>>
        PENDIENTE
        PROCESADA
        CANCELADA
        RECHAZADA
    }

    class SancionType {
        <<enumeration>>
        RETRASO
        PERDIDA
        DANIO
    }

    class SancionStatus {
        <<enumeration>>
        ACTIVA
        CUMPLIDA
        CANCELADA
    }

    class NotificationType {
        <<enumeration>>
        PRESTAMO_VENCIDO
        RESERVA_DISPONIBLE
        CUENTA_ACTIVADA
        BIENVENIDA
        SANCION
    }

    class NotificationStatus {
        <<enumeration>>
        PENDIENTE
        ENVIADA
        FALLIDA
    }

    %% Relaciones de composición/agregación
    Prestamo *-- LoanItem : contiene
    Solicitud *-- RequestItem : contiene

    class LoanItem {
        +String ejemplar_id
        +DateTime fecha_devolucion
        +String hora_devolucion
        +LoanStatus estado
    }

    class RequestItem {
        +String documento_id
        +RequestStatus estado
    }
```

## Troubleshooting

### Problemas comunes

1. Error de conexión a MongoDB

- Verificar `MONGODB_URL` en .env
- Verificar red y firewall

2. Error de mail

- Verificar credenciales SMTP
- Usar "App Password" en Gmail

3. Kaftka no inicia

- Verificar que Docker tenga suficientes recursos
- Revisar logs: `docker-compose logs kafka`

## Logs

```bash
# Ver logs de la aplicación
docker-compose logs app

# Ver logs de Kafka
docker-compose logs kafka

# Ver logs de Grafana
docker-compose logs grafana
```
