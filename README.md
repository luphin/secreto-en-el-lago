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
