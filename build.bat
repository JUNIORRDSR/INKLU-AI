@echo off
echo Construyendo la aplicación React...

:: Navegar al directorio del frontend
cd c:\WorkSpace Vs Code\INKLU-AI\inklu-ai-flask\app_fronted

:: Ejecutar el comando de construcción de npm que genera los archivos estáticos
call npm run build

:: Mostrar mensaje de éxito
echo Construcción completada. La aplicación está lista para ser desplegada.

:: Volver al directorio principal del proyecto
cd c:\WorkSpace Vs Code\INKLU-AI\inklu-ai-flask