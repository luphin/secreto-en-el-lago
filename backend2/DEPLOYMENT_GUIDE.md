# Guía de Despliegue - Sistema BEC

Esta guía describe cómo desplegar el Sistema de Préstamo BEC en producción.

## 📋 Tabla de Contenidos

1. [Requisitos Previos](#requisitos-previos)
2. [Configuración Inicial](#configuración-inicial)
3. [Despliegue con Docker](#despliegue-con-docker)
4. [Configuración de Servicios](#configuración-de-servicios)
5. [Monitoreo y Logs](#monitoreo-y-logs)
6. [Backups](#backups)
7. [Mantenimiento](#mantenimiento)

## 🔧 Requisitos Previos

### Hardware Recomendado
- **CPU**: 4 cores
- **RAM**: 8GB mínimo (16GB recomendado)
- **Disco**: 50GB SSD
- **Red**: 100Mbps

### Software
- Docker 20.10+
- Docker Compose 2.0+
- Linux (Ubuntu 20.04+ recomendado)

## 🚀 Configuración Inicial

### 1. Clonar el Repositorio

```bash
git clone <repository-url>
cd backend
```

### 2. Configurar Variables de Entorno

```bash
cp env.example .env
nano .env
```

**Variables críticas para producción:**

```env
# Cambiar OBLIGATORIAMENTE
SECRET_KEY=GENERAR_UNA_CLAVE_SEGURA_ALEATORIA_DE_64_CARACTERES

# MongoDB (si usas Atlas u otro servicio)
MONGODB_URL=mongodb+srv://usuario:password@cluster.mongodb.net/
MONGODB_DB_NAME=bec_biblioteca

# CORS (dominios permitidos)
ALLOWED_ORIGINS=["https://tudominio.com", "https://www.tudominio.com"]

# Email (SendGrid o Mailgun)
EMAIL_ENABLED=true
EMAIL_API_KEY=tu_api_key_aqui
EMAIL_FROM=noreply@tudominio.com

# MinIO/S3
STORAGE_ENDPOINT=https://tu-minio-endpoint.com
STORAGE_ACCESS_KEY=tu_access_key
STORAGE_SECRET_KEY=tu_secret_key

# Kafka (si usas servicio externo)
KAFKA_BOOTSTRAP_SERVERS=kafka.tudominio.com:9092
```

### 3. Generar Secret Key Segura

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(64))"
```

## 🐳 Despliegue con Docker

### Modo Producción

1. **Modificar docker-compose para producción**

Crear `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  backend:
    build: .
    container_name: bec_backend
    ports:
      - "8000:8000"
    env_file:
      - .env
    volumes:
      - ./app:/app/app
    depends_on:
      - mongodb
      - kafka
      - minio
    networks:
      - bec_network
    restart: always
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G

  notification_worker:
    build:
      context: .
      dockerfile: Dockerfile.consumer
    container_name: bec_notification_worker
    env_file:
      - .env
    depends_on:
      - kafka
    networks:
      - bec_network
    restart: always

  # ... resto de servicios
```

2. **Iniciar servicios**

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Con Nginx como Reverse Proxy

Instalar Nginx:

```bash
sudo apt install nginx
```

Configurar `/etc/nginx/sites-available/bec`:

```nginx
server {
    listen 80;
    server_name api.tudominio.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Habilitar sitio:

```bash
sudo ln -s /etc/nginx/sites-available/bec /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### SSL con Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d api.tudominio.com
```

## ⚙️ Configuración de Servicios

### MongoDB Atlas (Recomendado para Producción)

1. Crear cuenta en [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Crear cluster
3. Crear usuario de base de datos
4. Configurar IP whitelist
5. Obtener connection string
6. Actualizar `MONGODB_URL` en `.env`

### Kafka (Opcional - Servicio Externo)

Si prefieres usar Kafka como servicio (Confluent Cloud, AWS MSK):

1. Crear cluster
2. Crear tópicos: `email-notifications`, `overdue-checks`
3. Obtener credenciales
4. Actualizar configuración en `.env`

### MinIO (Almacenamiento)

**Opción 1: MinIO Local**

Ya está configurado en docker-compose.

**Opción 2: AWS S3**

```env
STORAGE_ENDPOINT=https://s3.amazonaws.com
STORAGE_ACCESS_KEY=tu_aws_access_key
STORAGE_SECRET_KEY=tu_aws_secret_key
STORAGE_BUCKET_NAME=bec-biometrics
```

## 📊 Monitoreo y Logs

### Configurar Grafana

1. Acceder a Grafana: `http://tu-servidor:3000`
2. Login: `admin` / `admin` (cambiar password)
3. Los dashboards ya están pre-configurados

### Ver Logs en Tiempo Real

```bash
# Logs del backend
docker logs -f bec_backend

# Logs del worker de notificaciones
docker logs -f bec_notification_worker

# Logs de todos los servicios
docker-compose logs -f
```

### Configurar Alertas

En Grafana, ir a:
1. **Alerting** → **Alert rules**
2. Crear alertas para:
   - Errores por minuto > 10
   - CPU usage > 80%
   - Memoria > 90%
   - MongoDB conexiones

## 🔄 Trabajos Batch (Cron)

### Configurar Cron para Trabajos Diarios

```bash
chmod +x scripts/setup_cron.sh
./scripts/setup_cron.sh
```

O manualmente:

```bash
crontab -e
```

Agregar:

```cron
# Verificar préstamos vencidos diariamente a las 2 AM
0 2 * * * docker exec bec_backend python -m app.services.batch_jobs >> /var/log/bec_batch.log 2>&1

# Backup de MongoDB diariamente a las 3 AM
0 3 * * * /path/to/backup_script.sh >> /var/log/bec_backup.log 2>&1
```

## 💾 Backups

### Script de Backup de MongoDB

Crear `scripts/backup_mongodb.sh`:

```bash
#!/bin/bash

BACKUP_DIR="/backups/mongodb"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup
docker exec bec_mongodb mongodump \
  --db bec_biblioteca \
  --out /tmp/backup_$DATE

# Copiar del contenedor
docker cp bec_mongodb:/tmp/backup_$DATE $BACKUP_DIR/

# Comprimir
cd $BACKUP_DIR
tar -czf backup_$DATE.tar.gz backup_$DATE
rm -rf backup_$DATE

# Eliminar backups antiguos (mantener últimos 7 días)
find $BACKUP_DIR -name "backup_*.tar.gz" -mtime +7 -delete

echo "Backup completado: $BACKUP_DIR/backup_$DATE.tar.gz"
```

### Restaurar Backup

```bash
# Descomprimir
tar -xzf backup_YYYYMMDD_HHMMSS.tar.gz

# Copiar al contenedor
docker cp backup_YYYYMMDD_HHMMSS bec_mongodb:/tmp/

# Restaurar
docker exec bec_mongodb mongorestore \
  --db bec_biblioteca \
  /tmp/backup_YYYYMMDD_HHMMSS/bec_biblioteca
```

## 🔧 Mantenimiento

### Actualizar el Sistema

```bash
# Detener servicios
docker-compose down

# Pull latest changes
git pull origin main

# Rebuild images
docker-compose build --no-cache

# Iniciar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f
```

### Limpiar Docker

```bash
# Eliminar contenedores no utilizados
docker system prune -a

# Eliminar volúmenes no utilizados
docker volume prune
```

### Reiniciar Servicios Individuales

```bash
docker-compose restart backend
docker-compose restart notification_worker
docker-compose restart mongodb
```

## 🔐 Seguridad

### Checklist de Seguridad

- [ ] `SECRET_KEY` cambiada a valor aleatorio
- [ ] MongoDB con autenticación habilitada
- [ ] CORS configurado solo para dominios permitidos
- [ ] SSL/TLS habilitado (HTTPS)
- [ ] Firewall configurado (solo puertos necesarios)
- [ ] Backups automatizados configurados
- [ ] Logs monitoreados
- [ ] Actualizaciones de seguridad aplicadas

### Firewall (UFW)

```bash
# Instalar UFW
sudo apt install ufw

# Permitir SSH
sudo ufw allow 22

# Permitir HTTP/HTTPS
sudo ufw allow 80
sudo ufw allow 443

# Habilitar
sudo ufw enable
```

## 📈 Escalabilidad

### Escalar Servicios

```bash
# Múltiples workers de notificaciones
docker-compose up -d --scale notification_worker=3

# Múltiples instancias del backend (con load balancer)
docker-compose up -d --scale backend=3
```

### Load Balancer con Nginx

```nginx
upstream backend {
    server localhost:8001;
    server localhost:8002;
    server localhost:8003;
}

server {
    listen 80;
    server_name api.tudominio.com;

    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🆘 Troubleshooting

### MongoDB no inicia

```bash
# Ver logs
docker logs bec_mongodb

# Verificar espacio en disco
df -h

# Reiniciar contenedor
docker restart bec_mongodb
```

### Kafka no conecta

```bash
# Verificar que Zookeeper esté corriendo
docker ps | grep zookeeper

# Ver logs de Kafka
docker logs bec_kafka

# Recrear contenedores
docker-compose restart zookeeper kafka
```

### Backend no responde

```bash
# Ver logs
docker logs bec_backend

# Verificar recursos
docker stats

# Reiniciar
docker restart bec_backend
```

## 📞 Soporte

Para problemas o consultas:

1. Revisar logs: `docker-compose logs`
2. Consultar documentación: [README.md](README.md)
3. Revisar issues en GitHub

---

**Última actualización**: Octubre 2025
**Versión del Sistema**: 1.0.0

