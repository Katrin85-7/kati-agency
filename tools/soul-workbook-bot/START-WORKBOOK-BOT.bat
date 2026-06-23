@echo off
chcp 65001 >nul
cd /d "%~dp0"

if not exist .env (
  echo.
  echo  Нет файла .env
  echo  1. copy .env.example .env
  echo  2. Вставь BOT_TOKEN от BotFather
  echo.
  pause
  exit /b 1
)

python -m pip install -r requirements.txt -q
python bot.py
pause
