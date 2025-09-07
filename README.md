# secreto-en-el-lago
LPWWW202502 Secreto en el lago


``` mermaid
---
config:
  look: classic
  theme: default
---
graph TD
    A[Cliente]
    subgraph Microservicios
        direction LR
        B[API Gateway]
        C[Servicio de Autenticación]
        D[Servicio de Chat]
        E[Servicio de Notificaciones]
        F[Servicio de Archivos]
        G[Servicio de Búsqueda]
        L[Servicio de Calendario]
    end
    subgraph Base de Datos
        H[Usuarios]
        I[Mensajes]
        J[Búsqueda]
        M[Calendario]
    end
    subgraph Almacenamiento
        K[Cloud]
    end
    A -- HTTP/S y WebSockets --> B
    A -- Subir Archivo LaTeX --> B
    B -- Petición de Autenticación --> C
    B -- Solicitud de Mensajes --> D
    B -- Petición de Archivos --> F
    B -- Consulta de Búsqueda --> G
    B -- Subir Archivo Calendario --> L
    C -- Lee/Escribe --> H
    D -- Lee/Escribe --> I
    F -- Lee/Escribe --> K
    G -- Lee/Escribe --> J
    L -- Lee archivo y guarda en --> M
    L -- "Programar Notificación" --> E
    L -- "Publicar en Chat" --> D
    D -- Envía Evento (RabbitMQ/Kafka) --> E
    D -- Envía Evento --> G

```
``` mermaid
sequenceDiagram
    Usuario ->> Servicio de Chat: Enviar mensaje
    Servicio de Chat ->> Bus de Eventos: Publicar: MensajeEnviado
    Bus de Eventos ->> Servicio de Notificaciones: Enviar
    Bus de Eventos ->> Servicio de Búsqueda: Enviar
    Servicio de Notificaciones ->> Usuario: Notificación Push

```

```mermaid
graph TD
    %% Inicio del proceso
    A[Inicio: Usuario sube archivo LaTeX] --> B{API Gateway enruta a Servicio de Calendario};

    %% Flujo principal del servicio de calendario
    B --> C[Servicio de Calendario recibe archivo];
    C --> D[Leer el archivo de texto];
    D --> E{Buscar el patrón de fecha `\evento{...}{...}`};

    %% Ramificaciones del proceso
    E -- No se encuentra el patrón --> F[Generar un error];
    F --> G[Notificar al usuario sobre error en el formato];
    E -- Patrón encontrado --> H[Extraer evento y fecha];
    H --> I{Validar el formato de la fecha};

    %% Flujo de validación
    I -- Fecha inválida --> J[Generar un error];
    J --> G;
    I -- Fecha válida --> K[Guardar evento y fecha en la Base de Datos de Calendario];

    %% Flujo de publicación y notificación
    K --> L[Programar notificaciones para el evento];
    L --> M[Enviar evento al Servicio de Notificaciones];
    
    K --> N[Publicar en el chat];
    N --> O[Enviar evento al Servicio de Chat para publicación];

    %% Final del proceso
    O --> P[Fin];
    M --> P;
    G --> P;
```
