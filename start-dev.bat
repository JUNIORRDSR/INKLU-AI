@echo off
echo Iniciando servidores de desarrollo...

start cmd /k "cd c:\WorkSpace Vs Code\INKLU-AI\inklu-ai-flask && python run.py"
start cmd /k "cd c:\WorkSpace Vs Code\INKLU-AI\inklu-ai-flask\app_fronted && npm run dev"

echo Servidores iniciados:
echo - Backend Flask: http://localhost:5000
echo - Frontend React: http://localhost:5173