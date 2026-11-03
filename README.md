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

- macOS (testado com Apple Silicon). Também funciona em Linux e Windows se correres o `app.py` manualmente.
- [Python 3.10+](https://www.python.org/downloads/)
- [ffmpeg](https://ffmpeg.org/), que no macOS se instala com:

  ```bash
  brew install ffmpeg
  ```

## Instalação e utilização

### Opção 1: duplo clique (macOS)

1. Faz download ou clona este repositório.
2. Dá duplo clique em **`Abrir Conversor.command`**.
   - Na primeira vez, o ambiente Python é preparado automaticamente.
   - Se o macOS bloquear o ficheiro, clica com o botão direito → **Abrir**.
3. O browser abre em `http://127.0.0.1:5050`.

### Opção 2: terminal

```bash
git clone https://github.com/brunomsmcarvalho/Youtube-to-mp3-mp4-converter.git
cd Youtube-to-mp3-mp4-converter
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python app.py
```

Para fechar a aplicação, fecha a janela do Terminal ou carrega em `Ctrl + C`.

## Qualidade

| Modo | Resultado | Notas |
|---|---|---|
| 🎵 Música | MP3 320 kbps | Usa a melhor faixa de áudio que o YouTube disponibiliza. O YouTube não tem áudio sem perdas, por isso o MP3 a 320 kbps (o máximo do formato) preserva tudo o que a fonte tem. |
| 🎬 Vídeo | MP4, melhor resolução | Junta vídeo e áudio sem recodificar. Na mesma resolução dá preferência a H.264, que é compatível com o QuickTime. Acima de 1080p o YouTube só oferece VP9 ou AV1, por isso pode ser preciso o [VLC](https://www.videolan.org/) ou o [IINA](https://iina.io/). |

## Problemas comuns

- **"É preciso o ffmpeg":** instala com `brew install ffmpeg`.
- **Erro de certificado SSL:** confirma que o pacote `certifi` está instalado (`.venv/bin/pip install certifi`).
- **Um vídeo deixou de converter:** atualiza o yt-dlp com `.venv/bin/pip install -U yt-dlp`. O lançador `.command` já o faz sempre que abre.

## Estrutura

```
app.py                   # Servidor e interface web
requirements.txt         # Dependências Python
Abrir Conversor.command  # Lançador de duplo clique (macOS)
```

## Aviso

Esta ferramenta é para uso pessoal. Descarrega apenas conteúdos que tens direito a guardar e respeita os direitos de autor e os [Termos de Serviço do YouTube](https://www.youtube.com/t/terms).

## Licença

[MIT](LICENSE)
