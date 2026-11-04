# YouTube → MP3 / MP4 Converter

Uma aplicação local e simples para converter links do YouTube em **música (MP3)** ou **vídeo (MP4)** na melhor qualidade disponível. Corre no teu computador e abre no browser. Não tem anúncios nem sites de terceiros.

## Funcionalidades

- **Escolhes o formato:** 🎵 *Apenas a música* (MP3 320 kbps) ou 🎬 *Vídeo* (MP4 na melhor resolução).
- **Vários links de uma vez:** o botão **+** acrescenta mais campos.
- **Progresso em tempo real** de cada conversão.
- **Fila automática:** até 3 conversões em simultâneo, e as restantes esperam a vez.
- **Cancelar** uma conversão ou **Cancelar tudo**. O que já tinha sido descarregado é apagado.
- **Capa e título** incluídos nos ficheiros (metadados e miniatura).
- Guarda automaticamente em `Músicas/` ou `Vídeos/`, na pasta da aplicação.

## Requisitos

Funciona em **macOS** e **Windows 10/11**, e também em Linux pelo terminal.

- [Python 3.10+](https://www.python.org/downloads/)
- [ffmpeg](https://ffmpeg.org/)

No Windows, o lançador instala os dois automaticamente se faltarem. No macOS, o ffmpeg instala-se com `brew install ffmpeg`.

## Instalação e utilização

Primeiro, descarrega o repositório: botão verde **Code → Download ZIP** e extrai o ZIP. Também o podes clonar com `git clone`.

### 🪟 Windows

1. Dá duplo clique em **`Abrir Conversor.bat`**.
2. Se faltar o Python ou o ffmpeg, são instalados automaticamente com o `winget`. Quando a instalação terminar, **fecha a janela e abre o lançador outra vez**.
   - Se o Windows mostrar "O Windows protegeu o seu PC", clica em **Mais informações → Executar mesmo assim**.
3. Na primeira vez, o ambiente é preparado automaticamente. Depois, o browser abre em `http://127.0.0.1:5050`.

> Se o `winget` não estiver disponível, instala manualmente o [Python](https://www.python.org/downloads/) (marca **"Add python.exe to PATH"**) e o ffmpeg (`winget install Gyan.FFmpeg` ou [gyan.dev](https://www.gyan.dev/ffmpeg/builds/)).

### 🍎 macOS

1. Instala o ffmpeg: `brew install ffmpeg`.
2. Dá duplo clique em **`Abrir Conversor.command`**.
   - Na primeira vez, o ambiente Python é preparado automaticamente.
   - Se o macOS bloquear o ficheiro, clica com o botão direito → **Abrir**.
3. O browser abre em `http://127.0.0.1:5050`.

### 💻 Terminal (qualquer sistema)

```bash
git clone https://github.com/brunomsmcarvalho/Youtube-to-mp3-mp4-converter.git
cd Youtube-to-mp3-mp4-converter
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt      # Windows: .venv\Scripts\pip install -r requirements.txt
.venv/bin/python app.py                        # Windows: .venv\Scripts\python app.py
```

Para fechar a aplicação, fecha a janela do terminal ou carrega em `Ctrl + C`.

## Qualidade

| Modo | Resultado | Notas |
| --- | --- | --- |
| 🎵 Música | MP3 320 kbps | Usa a melhor faixa de áudio que o YouTube disponibiliza. O YouTube não tem áudio sem perdas, por isso o MP3 a 320 kbps (o máximo do formato) preserva tudo o que a fonte tem. |
| 🎬 Vídeo | MP4, melhor resolução | Junta vídeo e áudio sem recodificar. Na mesma resolução dá preferência a H.264, que é compatível com o QuickTime. Acima de 1080p o YouTube só oferece VP9 ou AV1, por isso pode ser preciso o [VLC](https://www.videolan.org/) ou o [IINA](https://iina.io/). |

## Problemas comuns

- **"É preciso o ffmpeg":** no macOS, instala com `brew install ffmpeg`. No Windows, usa `winget install Gyan.FFmpeg` e depois abre o lançador outra vez.
- **Windows: "python não é reconhecido" ou abre a Microsoft Store:** instala o Python a partir de [python.org](https://www.python.org/downloads/) e marca **"Add python.exe to PATH"**.
- **Erro de certificado SSL:** confirma que o pacote `certifi` está instalado (`.venv/bin/pip install certifi`).
- **Um vídeo deixou de converter:** atualiza o yt-dlp com `.venv/bin/pip install -U yt-dlp`. O lançador `.command` já o faz sempre que abre.

## Estrutura

```text
app.py                   # Servidor e interface web
requirements.txt         # Dependências Python
Abrir Conversor.command  # Lançador de duplo clique (macOS)
Abrir Conversor.bat      # Lançador de duplo clique (Windows)
```

## Aviso

Esta ferramenta é para uso pessoal. Descarrega apenas conteúdos que tens direito a guardar e respeita os direitos de autor e os [Termos de Serviço do YouTube](https://www.youtube.com/t/terms).

## Licença

[MIT](LICENSE)
