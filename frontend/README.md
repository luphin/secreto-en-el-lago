# Frontend — Instrucciones para levantar desde 0

Este documento explica cómo compilar y ejecutar la parte `frontend` del proyecto (aplicación ASP.NET Core MVC) desde cero en un entorno Windows (PowerShell). También incluyo notas rápidas para Linux/macOS y Docker.

Requisitos previos
- .NET SDK 8.0 (o la versión indicada en el proyecto). Comprueba con:

```powershell
dotnet --version
```

- Node/npm no es necesario para esta aplicación (la UI usa Bootstrap y archivos estáticos ya incluidos). Si tu flujo usa herramientas de frontend externas, instálalas según se requiera.

Preparar el entorno
1. Clona el repositorio y sitúate en la carpeta `frontend`:

```powershell
cd C:\Users\Hoshi\Desktop\secreto-en-el-lago\frontend
```

2. (Opcional) Configura variables de entorno que la app pueda necesitar. Por ejemplo, si usas una API backend en otra máquina, exporta su URL en `ASPNETCORE_` o en el `appsettings.json` local.

Compilar y ejecutar (desarrollo)
1. Restaurar paquetes y compilar:

```powershell
dotnet restore
dotnet build -c Debug
```

2. Ejecutar la app (en consola). Por defecto escuchará en http://localhost:5000 y https://localhost:5001 (si tu `launchSettings.json` lo configura así):

```powershell
dotnet run 
```

3. Abrir el navegador en la URL indicada en la salida de `dotnet run` (usualmente `https://localhost:5001` o `http://localhost:5000`).

Notas sobre procesos bloqueados (Windows)
- Si recibes errores MSB3026/MSB3027 al compilar indicativos de que `frontend.exe` está en uso, detén el proceso que lo bloquea:

```powershell
Get-Process -Name frontend -ErrorAction SilentlyContinue | Stop-Process -Force
```

- Alternativamente usa el PID mostrado por `dotnet build` y ejecútalo con `Stop-Process -Id <PID> -Force`.

Ejecutar pruebas (si aplicara)
- Este proyecto no incluye tests en el subdirectorio `frontend` por defecto. Si añades tests, usa `dotnet test` en la raíz del proyecto de tests.

Publicar para producción
1. Genera un artefacto publicado:

```powershell
dotnet publish -c Release -o .\publish
```

2. Luego despliega el contenido de `publish` a tu servidor web / contenedor.

Ejecución en Docker (opcional)
- Si el repositorio incluye un Dockerfile para `frontend` (ver carpeta `frontend/Dockerfile`), puedes construir y ejecutar la imagen:

```powershell
docker build -t secreto-frontend:latest .
docker run --rm -p 5000:80 secreto-frontend:latest
```

Notas finales y troubleshooting
- Comprueba `appsettings.json` y `appsettings.Development.json` para configurar URLs de API u otros valores.
- Si la app no arranca o muestra errores 500, mira la salida de la consola para excepciones y revisa los logs.
- Si haces cambios en `wwwroot/css/site.css` y no los ves en el navegador, recuerda limpiar cache (Ctrl+F5) o eliminar los archivos temporales del navegador.

Contacto
- Si necesitas que automatice la configuración con un script PowerShell (crear variables, configurar `appsettings` locales, etc.), dime qué valores quieres y lo creo.
