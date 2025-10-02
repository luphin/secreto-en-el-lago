#!/bin/bash

# Script para ejecutar trabajos batch diarios
# Programar con cron: 0 2 * * * /path/to/run_batch_jobs.sh

echo "$(date) - Iniciando trabajos batch..."

# Ejecutar dentro del contenedor Docker
docker exec bec_backend python -m app.services.batch_jobs

echo "$(date) - Trabajos batch completados"

