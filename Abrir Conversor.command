#!/bin/zsh
# Abre o Conversor. Na primeira vez prepara o ambiente Python automaticamente.
cd "$(dirname "$0")"

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "É preciso o ffmpeg. Instala com:  brew install ffmpeg"
  read -k1 "?Carrega numa tecla para sair..."
  exit 1
fi

if [ ! -x .venv/bin/python ]; then
  echo "A preparar o ambiente (só na primeira vez)..."
  python3 -m venv .venv || { echo "Não foi possível criar o ambiente Python."; exit 1; }
  .venv/bin/pip install -q -r requirements.txt
fi

# Mantém o yt-dlp atualizado (o YouTube muda com frequência)
.venv/bin/pip install -q --upgrade yt-dlp >/dev/null 2>&1

.venv/bin/python app.py
