# Email config

## Acceder a inbox de Ethereal

- Ir a : https://ethereal.email/
- Iniciar sesión con credenciales
- Ver emails enviados en "Messages"

## Para verificar emails en tu app:

- Los emails de verificación llegarán a Ethereal
- Copia el token del email y úsalo en tu API

## Probar flujo

1. Registrar usuario
2. Revisar Ethereal - se visualizará email de verificación
3. Copiar el token de email
4. Usar el token en `POST  /api/v1/auth/verify-email`

**Ejemplo:**
```bash
# 1. Registrar usuario
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "rut": "12345678-9",
    "names": "Usuario",
    "last_names": "Prueba", 
    "email": "usuario_prueba@test.cl",
    "phone": "+56912345678",
    "address": "Test 123",
    "password": "secret123"
  }'

# 2. Revisar Ethereal.email, copiar token
# 3. Verificar email
curl -X POST "http://localhost:8000/api/v1/auth/verify-email?token=TOKEN_COPIADO_DEL_EMAIL"
```

>[!Note]  **Testing en consola**
> También se puede probar con `python scripts/test_ethereal.py` en la consola de Docker

---

## Ventajas de Ethereal Email vs Simulación

| Característica | Ethereal Email | Simulación |
|----------------|----------------|------------|
| Emails reales | Sí | No |
| Testing de templates HTML | Sí | Sí |
| Prueba de links y URLs | Sí | No |
| Flujo completo de verificación | Sí | Parcial |
| Prueba de formatos de email | Sí | No |
| Depuración de problemas SMTP | Sí | No |
| Configuración requerida | Credenciales SMTP | Ninguna |
| Velocidad de desarrollo | Rápida | Muy rápida |
| Dependencia externa | Sí (servicio Ethereal) | No |
| Verificación de entregabilidad | Sí | No |
| Testing de spam filters | Sí | No |
| Prueba en diferentes clientes | Sí | No |
| Consistencia con producción | Alta | Baja |
| Costo | Gratuito | Gratuito |
| Complejidad de setup | Media | Baja |
| Mantenimiento | Requiere credenciales | Sin mantenimiento |
| Escalabilidad | Limitada (testing) | Ilimitada |
| Logs detallados | En plataforma Ethereal | En consola/archivo |
| Recuperación de emails | Sí (inbox web) | No |
| Testing de attachments | Sí | No |
| Prueba de encoding | Sí | Parcial |

### Casos de uso recomendados

**Usar Ethereal Email cuando:**
- Necesitas probar el flujo completo de verificación de email
- Quieres ver cómo se renderizan los templates HTML en clientes reales
- Estás debuggeando problemas de entrega de emails
- Necesitas probar links y URLs en los emails
- Quieres una experiencia cercana a producción

**Usar Simulación cuando:**
- Estás en desarrollo temprano
- Quieres máxima velocidad de iteración
- No tienes acceso a credenciales SMTP
- Estás haciendo testing unitario
- Prefieres no depender de servicios externos
- Necesitas logs simples y rápidos


