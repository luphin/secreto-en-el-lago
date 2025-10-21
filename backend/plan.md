### **Plan de Desarrollo Backend: Sistema de Préstamo BEC**

[cite\_start]Este documento describe la planificación para la construcción del backend del sistema de la Biblioteca de Estación Central (BEC), basado en los requerimientos del "Caso 16" [cite: 1] y utilizando una arquitectura moderna orientada a servicios.

-----

### **1. Requerimientos y Características**

Los requerimientos se extraen directamente de las funcionalidades y casos de uso descritos en el documento proporcionado.

#### **1.1. Requerimientos Funcionales Clave**

  * **Gestión de Usuarios y Autenticación:**
      * [cite\_start]Autenticación de personal (Bibliotecarios, Administrativos) y usuarios (lectores)[cite: 34, 37].
      * [cite\_start]Registro de ficha de usuario, incluyendo datos básicos y biométricos (foto, huella digital)[cite: 27, 38].
      * [cite\_start]Proceso de activación de cuenta de usuario mediante validación por correo electrónico[cite: 39].
  * **Gestión de la Colección:**
      * [cite\_start]Administración (CRUD) de la colección bibliográfica, registrando información detallada de cada documento como título, autor, tipo, y ubicación[cite: 35].
  * **Catálogo y Búsqueda:**
      * [cite\_start]Consulta de catálogo electrónico sin necesidad de autenticación[cite: 36].
      * [cite\_start]Búsqueda de documentos por filtros como nombre, autor o categoría[cite: 40].
      * [cite\_start]Visualización de la disponibilidad en tiempo real de los ejemplares[cite: 28, 41].
  * **Proceso de Préstamo y Devolución:**
      * [cite\_start]Solicitud de préstamo desde tótems (requiere autenticación del usuario)[cite: 29, 37, 42].
      * [cite\_start]Reservas de ejemplares para fechas futuras[cite: 43].
      * [cite\_start]Registro del préstamo en el mesón, validado con RUT y huella digital del usuario[cite: 45].
      * [cite\_start]Cálculo automático de fechas y horas de devolución[cite: 46].
      * [cite\_start]Registro de la devolución de documentos, con un estado de transición para permitir el reordenamiento en estanterías[cite: 50].
  * **Gestión de Morosidad y Sanciones:**
      * [cite\_start]Revisión de préstamos vencidos (en sala y a domicilio) por parte del personal administrativo[cite: 48, 49].
      * [cite\_start]Envío automatizado de correos electrónicos a usuarios morosos[cite: 32, 49].
      * [cite\_start]Cálculo y aplicación de sanciones (en tiempo) para devoluciones con atraso[cite: 51].

#### **1.2. Requerimientos No Funcionales**

  * **Arquitectura y Plataforma:**
      * [cite\_start]El sistema será desarrollado en un ambiente web [cite: 58] con una arquitectura de microservicios o servicios desacoplados.
      * Todo el entorno de desarrollo y producción estará containerizado con Docker para garantizar la portabilidad y consistencia.
  * **Seguridad:**
      * [cite\_start]Implementación de medidas de seguridad como cifrado de contraseñas y control de sesiones de usuario[cite: 64].
      * [cite\_start]Validación estricta de todas las entradas de datos en la API[cite: 65].
  * **Observabilidad y Monitoreo:**
      * Centralización de logs de todos los servicios para facilitar la depuración y el monitoreo.
      * Visualización de métricas y logs del sistema a través de Grafana.
  * **Rendimiento y Escalabilidad:**
      * [cite\_start]El sistema debe ser capaz de manejar la creciente demanda de usuarios[cite: 20].
      * [cite\_start]Las consultas al catálogo y la verificación de disponibilidad deben ser eficientes y rápidas[cite: 28].

-----

### **2. Arquitectura Propuesta**

Se propone una arquitectura de microservicios desacoplados, orquestada con Docker, donde cada componente tiene una responsabilidad única.

#### **Componentes Clave:**

1.  **API Gateway:** Un único punto de entrada para todas las solicitudes de los clientes (tótems, aplicaciones de personal). Podría ser gestionado por un servicio como Nginx o Traefik.
2.  **Servicio Principal (Backend FastAPI):** El núcleo de la aplicación. Expondrá una API RESTful para gestionar las operaciones principales:
      * `Autenticación`: Endpoints para login, registro y gestión de tokens (JWT).
      * `Gestión de Usuarios`: CRUD para los datos de los lectores y el personal.
      * `Gestión de Colección`: CRUD para documentos y ejemplares.
      * `Operaciones de Préstamo`: Lógica de negocio para solicitar, registrar, devolver y reservar documentos.
3.  **Base de Datos (MongoDB Atlas):**
      * Base de datos NoSQL en la nube, seleccionada por su flexibilidad de esquema (ideal para variados tipos de documentos) y escalabilidad.
      * Los datos biométricos como **fotos y huellas digitales no se almacenarán directamente en la base de datos**. En su lugar, se guardarán en un servicio de almacenamiento de objetos (como AWS S3 o MinIO) y MongoDB almacenará únicamente la URL o el identificador del archivo.
4.  **Cola de Mensajes (Apache Kafka):**
      * Se utilizará para desacoplar procesos asíncronos y mejorar la resiliencia del sistema.
      * **Tópicos propuestos:**
          * `email-notifications`: Para eventos como "activar cuenta" o "recordatorio de devolución". [cite\_start]Un servicio consumidor se encargará de procesar estos mensajes y enviar los correos[cite: 32, 39].
          * `overdue-checks`: Para activar procesos nocturnos (batch) que verifiquen préstamos vencidos y generen notificaciones o sanciones.
5.  **Servicio de Notificaciones (Consumidor Kafka):**
      * Un pequeño servicio (worker) que escucha el tópico `email-notifications` de Kafka. [cite\_start]Su única función es tomar los mensajes y utilizar una API de correo electrónico (como SendGrid o Mailgun) para enviar las comunicaciones[cite: 63].
6.  **Monitoreo y Logging (Loki + Grafana):**
      * **Loki** se utilizará como el sistema de agregación de logs. Todos los contenedores Docker se configurarán para enviar sus logs a Loki.
      * **Grafana** se conectará a Loki para visualizar, consultar y crear alertas sobre los logs, proporcionando una visión centralizada del estado del sistema.
7.  **Contenerización (Docker + Docker Compose):**
      * Toda la aplicación (API FastAPI, consumidor de Kafka, etc.) será definida en archivos `Dockerfile`.
      * `docker-compose.yml` se utilizará para orquestar todos los servicios en el entorno de desarrollo local, facilitando el levantamiento de toda la pila tecnológica con un solo comando.

-----

### **3. Estructura de la Base de Datos (MongoDB)**

[cite\_start]Se proponen las siguientes colecciones, inspiradas en las estructuras de datos del documento de referencia[cite: 75, 76, 77, 78, 79, 80, 81, 82].

**1. `users`**

```json
{
  "_id": "ObjectId",
  "rut": "string",
  "nombres": "string",
  "apellidos": "string",
  "direccion": "string",
  "telefono": "string",
  "email": "string",
  "password": "(hashed)",
  "rol": ["lector", "bibliotecario", "administrativo"],
  "activo": "boolean",
  "fecha_creacion": "Date",
  "foto_url": "string", // URL al archivo en S3/MinIO
  "huella_ref": "string", // Referencia o URL al archivo de huella
  "sancion_hasta": "Date" // Fecha hasta la cual el usuario está sancionado
}
```

**2. `documents`**

```json
{
  "_id": "ObjectId",
  "titulo": "string",
  "autor": "string",
  "editorial": "string",
  "edicion": "string",
  "ano_edicion": "integer",
  "tipo": ["libro", "audio", "video"],
  "categoria": "string",
  "tipo_medio": "string" // ej: DVD, CD, etc.
}
```

**3. `items` (Ejemplares)**

```json
{
  "_id": "ObjectId",
  "document_id": "ObjectId", // Referencia a la colección 'documents'
  "estado": ["disponible", "prestado", "en_restauracion", "reservado"],
  "ubicacion": "string" // ej: "Estantería 5, Nivel 3"
}
```

**4. `loans` (Préstamos)**

```json
{
  "_id": "ObjectId",
  "item_id": "ObjectId", // Referencia al ejemplar
  "user_id": "ObjectId", // Referencia al usuario
  "tipo_prestamo": ["sala", "domicilio"],
  "fecha_prestamo": "Date",
  "fecha_devolucion_pactada": "Date",
  "fecha_devolucion_real": "Date", // Null hasta que se devuelve
  "estado": ["activo", "devuelto", "vencido"]
}
```

**5. `reservations`**

```json
{
  "_id": "ObjectId",
  "document_id": "ObjectId", // Se reserva el documento, no un item específico
  "user_id": "ObjectId",
  "fecha_reserva": "Date", // Fecha para la cual se reserva
  "estado": ["activa", "completada", "expirada"]
}
```

-----

### **4. Fases de Desarrollo (Roadmap Sugerido)**

1.  **Fase 1: Fundación y Core**
      * Configuración del entorno Dockerizado (Docker Compose).
      * Definición de las colecciones en MongoDB Atlas.
      * Implementación del servicio de **Usuarios y Autenticación** (registro, login JWT, gestión de roles).
      * Implementación del CRUD para la **Gestión de la Colección** (`documents` e `items`).
2.  **Fase 2: Lógica de Préstamos**
      * Implementación de los endpoints para **Consultar Catálogo** con filtros avanzados.
      * Desarrollo de la lógica para **Solicitar, Registrar y Devolver Préstamos**.
      * Implementación de la funcionalidad de **Reservas**.
3.  **Fase 3: Procesos Asíncronos y Notificaciones**
      * Configuración de Kafka y el servicio consumidor de notificaciones.
      * Integración de eventos en el servicio principal para publicar mensajes en Kafka (ej: al registrar un usuario, al vencer un préstamo).
      * [cite\_start]Desarrollo del proceso batch para **revisar préstamos vencidos y enviar recordatorios**[cite: 49].
4.  **Fase 4: Sanciones y Monitoreo**
      * [cite\_start]Implementación de la lógica para **calcular y aplicar sanciones** a los usuarios[cite: 51].
      * Configuración de la ingesta de logs en Loki.
      * Creación de dashboards en Grafana para visualizar el estado de la aplicación y las métricas de negocio (ej: préstamos por día, documentos más solicitados).