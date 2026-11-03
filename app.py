"""Conversor local de YouTube -> MP3 (Músicas) ou MP4 (Vídeos)."""
import shutil
import tempfile
import threading
import uuid
import webbrowser
from pathlib import Path

from flask import Flask, jsonify, request
import yt_dlp

BASE = Path(__file__).resolve().parent
PASTAS = {"musica": BASE / "Músicas", "video": BASE / "Vídeos"}
for p in PASTAS.values():
    p.mkdir(exist_ok=True)

app = Flask(__name__)
jobs: dict[str, dict] = {}
limite = threading.Semaphore(3)  # no máximo 3 conversões ao mesmo tempo; as outras esperam


def opcoes(tipo: str, job: dict, tmp: str) -> dict:
    def verificar():
        if job.get("cancelar"):
            raise yt_dlp.utils.DownloadCancelled("Cancelado")

    def hook(d):
        verificar()
        if d["status"] == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
            if total:
                job["progresso"] = round(d.get("downloaded_bytes", 0) * 100 / total)
            job["estado"] = "A descarregar…"
        elif d["status"] == "finished":
            job["estado"] = "A processar…"

    def pp_hook(d):
        verificar()
        if d["status"] == "finished" and d.get("postprocessor") == "MoveFiles":
            job["ficheiro"] = d["info_dict"].get("filepath")

    base = {
        "paths": {"home": str(PASTAS[tipo]), "temp": tmp},  # temporários isolados por conversão
        "outtmpl": "%(title)s.%(ext)s",
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "noprogress": True,
        "progress_hooks": [hook],
        "postprocessor_hooks": [pp_hook],
        "writethumbnail": True,
    }
    if tipo == "musica":
        # Melhor áudio disponível -> MP3 320 kbps (qualidade máxima do MP3)
        base.update({
            "format": "bestaudio/best",
            "postprocessors": [
                {"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "320"},
                {"key": "FFmpegMetadata", "add_metadata": True},
                {"key": "EmbedThumbnail"},
            ],
        })
    else:
        # Melhor resolução; entre iguais, prefere MP4/M4A para juntar sem recodificar
        base.update({
            "format": "bv*+ba/b",
            "format_sort": ["res", "fps", "vcodec:h264", "ext:mp4:m4a"],
            "merge_output_format": "mp4",
            "postprocessors": [
                {"key": "FFmpegMetadata", "add_metadata": True},
                {"key": "EmbedThumbnail"},
            ],
        })
    return base


def trabalhar(job_id: str, url: str, tipo: str):
    job = jobs[job_id]
    job["estado"] = "Em fila…"
    tmp = tempfile.mkdtemp(prefix="conversor-")
    try:
        with limite:
            if job.get("cancelar"):
                raise yt_dlp.utils.DownloadCancelled("Cancelado")
            with yt_dlp.YoutubeDL(opcoes(tipo, job, tmp)) as ydl:
                job["estado"] = "A iniciar…"
                info = ydl.extract_info(url, download=True)
        if job.get("cancelar"):  # cancelado mesmo no fim: apaga o ficheiro final
            raise yt_dlp.utils.DownloadCancelled("Cancelado")
        job.update(estado="Concluído ✔", progresso=100, titulo=info.get("title"), fim=True)
    except Exception as e:  # noqa: BLE001
        if job.get("cancelar"):
            apagar_final(job, tipo)
            job.update(estado="Cancelado — ficheiros apagados", fim=True, cancelado=True)
        else:
            msg = str(e).split("ERROR: ")[-1]
            job.update(estado=f"Erro: {msg}", fim=True, erro=True)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)  # apaga tudo o que foi descarregado para o temporário


def apagar_final(job: dict, tipo: str):
    """Apaga o ficheiro final se já tiver sido movido para Músicas/Vídeos."""
    f = job.get("ficheiro")
    if f:
        f = Path(f).resolve()
        if f.parent == PASTAS[tipo].resolve() and f.is_file():
            f.unlink()


@app.post("/converter")
def converter():
    dados = request.get_json(force=True)
    url = (dados.get("url") or "").strip()
    tipo = dados.get("tipo")
    if not url or tipo not in PASTAS:
        return jsonify(erro="Link ou tipo inválido"), 400
    job_id = uuid.uuid4().hex
    jobs[job_id] = {"estado": "A iniciar…", "progresso": 0, "fim": False, "tipo": tipo, "url": url}
    threading.Thread(target=trabalhar, args=(job_id, url, tipo), daemon=True).start()
    return jsonify(id=job_id)


@app.post("/cancelar/<job_id>")
def cancelar(job_id):
    job = jobs.get(job_id)
    if job and not job["fim"]:
        job["cancelar"] = True
        job["estado"] = "A cancelar…"
    return jsonify(ok=True)


@app.get("/estado/<job_id>")
def estado(job_id):
    return jsonify(jobs.get(job_id, {"estado": "Desconhecido", "fim": True, "erro": True}))


@app.get("/")
def index():
    return PAGINA


PAGINA = """<!doctype html>
<html lang="pt"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Conversor de Música</title>
<style>
:root{--bg:#0f1115;--card:#181b22;--txt:#e8eaf0;--mut:#8b90a0;--acc:#ff3b5c;--ok:#2ecc71;--line:#262a35}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--txt);font:16px/1.5 -apple-system,system-ui,sans-serif;
display:flex;justify-content:center;padding:48px 16px}
main{width:100%;max-width:620px}h1{font-size:26px;margin:0 0 4px}p.sub{color:var(--mut);margin:0 0 28px}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:22px}
#links{display:flex;flex-direction:column;gap:8px}
.linha{display:flex;gap:8px}
.linha input{flex:1;min-width:0;padding:14px;border-radius:10px;border:1px solid var(--line);background:#0b0d11;color:var(--txt);font-size:15px}
.linha button,.mais{width:48px;flex:none;border-radius:10px;border:1px solid var(--line);background:#0b0d11;color:var(--mut);font-size:22px;cursor:pointer}
.linha button:hover{color:var(--acc);border-color:var(--acc)}
.mais{margin-top:8px;height:44px;color:var(--txt)}.mais:hover{border-color:var(--acc);color:var(--acc)}
.q{margin:20px 0 10px;color:var(--mut);font-size:14px}
.ops{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.ops button{padding:18px 12px;border-radius:12px;border:1px solid var(--line);background:#0b0d11;color:var(--txt);
font-size:16px;cursor:pointer;text-align:left}
.ops button:hover{border-color:var(--acc)}.ops small{display:block;color:var(--mut);font-size:12px;margin-top:4px}
#lista{margin-top:12px;display:flex;flex-direction:column;gap:10px}
.job{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px}
.job .t{font-weight:600;word-break:break-word}.job .e{color:var(--mut);font-size:13px;margin:4px 0 8px}
.bar{height:6px;background:#0b0d11;border-radius:3px;overflow:hidden}.bar i{display:block;height:100%;background:var(--acc);width:0;transition:width .3s}
.job.ok .bar i{background:var(--ok)}.job.err .e{color:var(--acc)}
.job .top{display:flex;gap:10px;align-items:flex-start}.job .t{flex:1}
.cancel{flex:none;padding:6px 12px;border-radius:8px;border:1px solid var(--line);background:#0b0d11;color:var(--mut);font-size:13px;cursor:pointer}
.cancel:hover{color:var(--acc);border-color:var(--acc)}
.job.cx{opacity:.6}.job.cx .bar i{background:var(--mut)}
#tudo{display:none;margin:22px 0 0 auto}#tudo.on{display:block}
</style></head><body><main>
<h1>Conversor de Música</h1>
<p class="sub">Cola um link do YouTube (carrega em + para juntar mais) e escolhe o que queres guardar.</p>
<div class="card">
  <div id="links"></div>
  <button class="mais" onclick="novo().focus()" title="Adicionar outro link">+</button>
  <div class="q">Queres o vídeo ou apenas a música?</div>
  <div class="ops">
    <button onclick="ir('musica')">🎵 Apenas a música<small>MP3 320 kbps → pasta Músicas</small></button>
    <button onclick="ir('video')">🎬 Vídeo<small>MP4 melhor qualidade → pasta Vídeos</small></button>
  </div>
</div>
<button id="tudo" class="cancel" onclick="cancelarTudo()">Cancelar tudo</button>
<div id="lista"></div>
</main><script>
const caixa=document.getElementById('links'), ativos=new Map();
function atualizarTudo(){document.getElementById('tudo').classList.toggle('on',ativos.size>1)}
function cancelarTudo(){ativos.forEach(b=>{if(!b.disabled)b.click()})}
function novo(){
  const l=document.createElement('div'); l.className='linha';
  l.innerHTML='<input placeholder="https://www.youtube.com/watch?v=…"><button title="Remover">×</button>';
  l.querySelector('button').onclick=()=>{ if(caixa.children.length>1) l.remove(); else l.querySelector('input').value=''; };
  caixa.append(l); return l.querySelector('input');
}
novo().focus();
function ir(tipo){
  const campos=[...caixa.querySelectorAll('input')];
  const links=[...new Set(campos.flatMap(c=>c.value.split(/\\s+/)).filter(Boolean))];
  if(!links.length){campos[0].focus();return}
  caixa.innerHTML=''; novo().focus();
  links.forEach(url=>um(url,tipo));
}
async function um(url,tipo){
  const r=await fetch('/converter',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({url,tipo})});
  const d=await r.json(); if(d.erro){alert(d.erro);return}
  const div=document.createElement('div'); div.className='job';
  div.innerHTML=`<div class="top"><div class="t">${tipo==='musica'?'🎵':'🎬'} ${url.replace(/</g,'&lt;')}</div><button class="cancel">Cancelar</button></div><div class="e">A iniciar…</div><div class="bar"><i></i></div>`;
  const btn=div.querySelector('.cancel');
  btn.onclick=()=>{btn.disabled=true;btn.textContent='A cancelar…';fetch('/cancelar/'+d.id,{method:'POST'})};
  ativos.set(d.id,btn); atualizarTudo();
  document.getElementById('lista').prepend(div);
  const t=setInterval(async()=>{
    const s=await (await fetch('/estado/'+d.id)).json();
    div.querySelector('.e').textContent=s.estado;
    div.querySelector('i').style.width=(s.progresso||0)+'%';
    if(s.titulo) div.querySelector('.t').textContent=(tipo==='musica'?'🎵 ':'🎬 ')+s.titulo;
    if(s.fim){clearInterval(t);btn.remove();ativos.delete(d.id);atualizarTudo();
      div.classList.add(s.cancelado?'cx':s.erro?'err':'ok')}
  },700);
}
</script></body></html>"""


if __name__ == "__main__":
    threading.Timer(1.0, lambda: webbrowser.open("http://127.0.0.1:5050")).start()
    app.run(host="127.0.0.1", port=5050, debug=False)
