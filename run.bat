@echo off
:: 1. Start the three terminals with unique titles
start "ML-Services" /d "%~dp0" cmd /k "venv\Scripts\activate && cd ml-service && python main.py"
start "FrontEnd" cmd /k "cd web-frontend && npm run dev"
start "Backend" cmd /k "cd backend-gateway && npm start"


echo Terminals launched. 
echo Press any key in THIS window to close all of them and exit.
pause

:: 2. Kill the terminals by their specific titles
taskkill /fi "WINDOWTITLE eq ML-Services*" /f
taskkill /fi "WINDOWTITLE eq FrontEnd*" /f
taskkill /fi "WINDOWTITLE eq Backend*" /f

exit