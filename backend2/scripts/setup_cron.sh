#!/bin/bash

# Script para configurar el cron job (Linux/Mac)

echo "Configurando cron job para trabajos batch..."

# Obtener la ruta absoluta del script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BATCH_SCRIPT="$SCRIPT_DIR/run_batch_jobs.sh"

# Hacer ejecutable el script
chmod +x "$BATCH_SCRIPT"

# Agregar al crontab (ejecutar diariamente a las 2 AM)
(crontab -l 2>/dev/null; echo "0 2 * * * $BATCH_SCRIPT >> /var/log/bec_batch.log 2>&1") | crontab -

echo "✓ Cron job configurado exitosamente"
echo "  Se ejecutará diariamente a las 2:00 AM"
echo "  Logs en: /var/log/bec_batch.log"

