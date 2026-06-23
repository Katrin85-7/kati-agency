@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo  Soul Method bot - Render (bez karty, $0)
echo  ========================================
echo.
echo  1. prepare-deploy.ps1  - PDF v pdfs/
echo  2. GitHub push         - tools/soul-workbook-bot
echo  3. render.com          - Blueprint iz render.yaml
echo  4. uptimerobot.com     - ping /health kazhdye 5 min
echo.
echo  Polnaya instrukciya: DEPLOY-RENDER.md
echo.

powershell -ExecutionPolicy Bypass -File "%~dp0prepare-deploy.ps1"

echo.
echo  Otkryvayu render.com i uptimerobot.com...
start https://render.com
timeout /t 2 >nul
start https://uptimerobot.com
start "" "%~dp0DEPLOY-RENDER.md"

pause
