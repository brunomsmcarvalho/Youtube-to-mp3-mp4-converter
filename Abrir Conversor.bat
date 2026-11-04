@echo off
chcp 65001 >nul
title Conversor YouTube
cd /d "%~dp0"

rem --- ffmpeg ---
where ffmpeg >nul 2>&1
if errorlevel 1 (
  echo O ffmpeg nao esta instalado. A instalar com o winget...
  winget install --id Gyan.FFmpeg -e --accept-source-agreements --accept-package-agreements
  echo.
  echo Instalacao concluida. Fecha esta janela e abre o Conversor outra vez.
  pause
  exit /b
)

rem --- Python ---
set "PY="
where py >nul 2>&1 && set "PY=py -3"
if not defined PY (
  where python >nul 2>&1 && python -c "import sys" >nul 2>&1 && set "PY=python"
)
if not defined PY (
  echo O Python nao esta instalado. A instalar com o winget...
  winget install --id Python.Python.3.13 -e --accept-source-agreements --accept-package-agreements
  echo.
  echo Instalacao concluida. Fecha esta janela e abre o Conversor outra vez.
  pause
  exit /b
)

rem --- Ambiente (so na primeira vez) ---
if not exist ".venv\Scripts\python.exe" (
  echo A preparar o ambiente, so na primeira vez...
  %PY% -m venv .venv || (echo Nao foi possivel criar o ambiente Python. & pause & exit /b 1)
  ".venv\Scripts\python.exe" -m pip install -q -r requirements.txt
)

rem Mantem o yt-dlp atualizado (o YouTube muda com frequencia)
".venv\Scripts\python.exe" -m pip install -q --upgrade yt-dlp >nul 2>&1

".venv\Scripts\python.exe" app.py
pause
