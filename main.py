import os
import asyncio
from starlette.applications import Starlette
from starlette.responses import JSONResponse, HTMLResponse
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
import yt_dlp

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Don Pedro Music</title>
    <link rel="manifest" href="/manifest.json">
    <meta name="theme-color" content="#1db954">
    <style>
        body { background: #121212; color: #ffffff; font-family: Arial, sans-serif; padding: 15px; max-width: 600px; margin: 0 auto; padding-bottom: 80px; }
        .tab-container { display: flex; gap: 8px; margin-bottom: 20px; border-bottom: 2px solid #333; padding-bottom: 10px; }
        .tab-btn { flex: 1; padding: 10px 5px; background: #222; color: #aaa; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; text-align: center; font-size: 13px; }
        .tab-btn.active { background: #1db954; color: #fff; }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        input[type="text"] { width: 100%; padding: 14px; background: #222; color: #fff; border: 1px solid #444; border-radius: 8px; font-size: 16px; outline: none; box-sizing: border-box; margin-bottom: 10px; }
        button.main-btn { width: 100%; padding: 14px; background: #1db954; color: #fff; border: none; border-radius: 8px; font-weight: bold; font-size: 16px; cursor: pointer; }
        .card { background: #1e1e1e; padding: 12px; margin-bottom: 12px; border-radius: 8px; border: 1px solid #333; display: flex; gap: 10px; align-items: center; }
        .card img { width: 75px; height: 55px; object-fit: cover; border-radius: 6px; background: #222; }
        .card-info { flex: 1; overflow: hidden; }
        .card-info h4 { margin: 0 0 4px 0; font-size: 13px; color: #fff; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .card-info p { margin: 0 0 6px 0; font-size: 11px; color: #aaa; }
        .download-btn { background: #282828; color: #1db954; border: 1px solid #1db954; padding: 6px 12px; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 11px; }
        #status { text-align: center; color: #ffeb3b; font-weight: bold; margin-bottom: 15px; font-size: 14px; }
        #loading { text-align: center; color: #1db954; display: none; margin: 20px; font-weight: bold; }
        audio { width: 100%; margin-top: 10px; border-radius: 6px; }
        .ad-box { background: #181818; border: 1px solid #333; padding: 10px; text-align: center; margin: 15px 0; border-radius: 8px; }
    </style>
</head>
<body>
    <h2 style="color: #1db954; text-align: center; margin-bottom: 2px;">🎵 Don Pedro Music 🎵</h2>
    <p style="text-align: center; color: #888; font-size: 12px; margin-top: 0; margin-bottom: 15px;">Plataforma Oficial de Monetización</p>

    <!-- 1. ESTRUCTURA DE TRES PESTAÑAS -->
    <div class="tab-container">
        <button class="tab-btn active" onclick="switchTab(1)">🔍 Buscador</button>
        <button class="tab-btn" onclick="switchTab(2)">🎧 Reproductor</button>
        <button class="tab-btn" onclick="switchTab(3)">📥 Descargas</button>
    </div>

    <div id="status"></div>

    <!-- PESTAÑA 1: BUSCADOR -->
    <div id="tab1" class="tab-content active">
        <div>
            <input type="text" id="query" placeholder="Escribe artista o canción..." onkeydown="if(event.key === 'Enter') buscarClient()">
            <button class="main-btn" onclick="buscarClient()">Buscar Rolas</button>
        </div>

        <div class="ad-box">
            <script async src="https://pl31305642.profitableratecpmnetwork.com/31213080/invoke.js"></script>
            <div id="container-5fb16da782b926221a41d2e6f11d9f41"></div>
        </div>

        <div id="loading">⚡ Buscando canciones...</div>
        <div id="results" style="margin-top: 15px;"></div>
    </div>

    <!-- PESTAÑA 2: REPRODUCTOR -->
    <div id="tab2" class="tab-content">
        <h3 style="color: #1db954; font-size: 15px; margin-bottom: 10px;">🎧 Colección & Reproductor:</h3>
        <div id="downloaded-list">
            <p style="color: #777; font-size: 13px; text-align: center;">Cargando lista...</p>
        </div>

        <div class="ad-box">
            <script async src="https://pl31305642.profitableratecpmnetwork.com/31213080/invoke.js"></script>
        </div>
    </div>

    <!-- PESTAÑA 3: CENTRO DE DESCARGAS -->
    <div id="tab3" class="tab-content">
        <h3 style="color: #1db954; font-size: 15px; margin-bottom: 10px;">📥 Archivos listos para guardar:</h3>
        <div id="files-direct-list">
            <p style="color: #777; font-size: 13px; text-align: center;">No hay archivos descargados todavía.</p>
        </div>
    </div>

    <!-- 2. ANUNCIO POPUNDER (EJECUCIÓN GLOBAL AUTOMÁTICA) -->
    <script src="https://pl31305642.profitableratecpmnetwork.com/f2/0e/67/f20e6758589f93239924993b647b2b21.js"></script>

    <!-- 3. ANUNCIO SOCIAL BAR (FLOTANTE QUE SIGUE AL USUARIO) -->
    <script data-cfasync="false" src="https://bellnewyork.org/14/e24c54a7abfb06cd69608a2609703f4b"></script>

    <script>
        function switchTab(n) {
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            document.querySelectorAll('.tab-btn')[n-1].classList.add('active');
            document.getElementById('tab' + n).classList.add('active');
            if(n === 2 || n === 3) cargarBiblioteca();
        }

        function triggerPopunder() {
            try {
                let ev = new MouseEvent('click', {view: window, bubbles: true, cancelable: true});
                document.body.dispatchEvent(ev);
            } catch(e) {}
        }

        async function buscarClient() {
            triggerPopunder();
            const q = document.getElementById('query').value;
            if (!q) return;
            document.getElementById('loading').style.display = 'block';
            document.getElementById('results').innerHTML = '';
            document.getElementById('status').innerText = '';

            try {
                let response = await fetch(`/api/buscar?q=` + encodeURIComponent(q));
                let data = await response.json();
                document.getElementById('loading').style.display = 'none';

                if (data && data.length > 0) {
                    let html = '';
                    data.forEach(item => {
                        let videoId = item.id;
                        let titulo = item.title.replace(/'/g, "").replace(/"/g, "");
                        let canal = item.uploader || "YouTube";
                        let miniatura = item.thumbnail || `https://i.ytimg.com/vi/${videoId}/hqdefault.jpg`;

                        html += `
                            <div class="card">
                                <img src="${miniatura}">
                                <div class="card-info">
                                    <h4>${titulo}</h4>
                                    <p>${canal}</p>
                                    <button class="download-btn" onclick="descargar('${videoId}', '${titulo}', this)">📥 Descargar MP3</button>
                                </div>
                            </div>
                        `;
                    });
                    document.getElementById('results').innerHTML = html;
                } else {
                    document.getElementById('status').innerText = 'No se encontraron rolas.';
                }
            } catch (e) {
                document.getElementById('loading').style.display = 'none';
                document.getElementById('status').innerText = 'Error al conectar con el servidor.';
            }
        }

        async function descargar(id, titulo, btn) {
            triggerPopunder();
            btn.innerText = "⏳ Bajando...";
            btn.disabled = true;
            document.getElementById('status').innerText = `⏳ Procesando MP3...`;

            try {
                let res = await fetch('/descargar_mp3/' + id);
                let data = await res.json();
                if (data.status === "success") {
                    btn.innerText = "✅ ¡Listo!";
                    document.getElementById('status').innerText = "¡Descarga completada!";
                    setTimeout(() => switchTab(2), 1200);
                } else {
                    btn.innerText = "📥 Descargar MP3";
                    btn.disabled = false;
                    document.getElementById('status').innerText = data.error || "Error al descargar.";
                }
            } catch (e) {
                btn.innerText = "📥 Descargar MP3";
                btn.disabled = false;
                document.getElementById('status').innerText = 'Error de conexión.';
            }
        }

        async function cargarBiblioteca() {
            try {
                let res = await fetch('/api/archivos');
                let files = await res.json();
                let listDiv2 = document.getElementById('downloaded-list');
                let listDiv3 = document.getElementById('files-direct-list');
                
                if(files && files.length > 0) {
                    let html2 = '';
                    let html3 = '';
                    files.forEach(f => {
                        html2 += `
                            <div class="card" style="flex-direction: column; align-items: stretch;">
                                <h4 style="margin: 0 0 6px 0; color: #1db954; font-size: 13px;">🎵 ${f}</h4>
                                <audio controls onplay="triggerPopunder()" src="/archivo/${f}"></audio>
                            </div>
                        `;
                        html3 += `
                            <div class="card" style="justify-content: space-between;">
                                <span style="font-size: 13px; color: #fff; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 70%;">🎵 ${f}</span>
                                <a href="/archivo/${f}" download style="background: #1db954; color: #fff; padding: 6px 12px; border-radius: 6px; text-decoration: none; font-size: 12px; font-weight: bold;">💾 Guardar</a>
                            </div>
                        `;
                    });
                    listDiv2.innerHTML = html2;
                    listDiv3.innerHTML = html3;
                } else {
                    let emptyMsg = '<p style="color: #777; font-size: 13px; text-align: center;">No hay rolas descargadas todavía.</p>';
                    listDiv2.innerHTML = emptyMsg;
                    listDiv3.innerHTML = emptyMsg;
                }
            } catch(e) {}
        }
    </script>
</body>
</html>
"""

async def home(request):
    return HTMLResponse(HTML_TEMPLATE)

async def manifest(request):
    return JSONResponse({
        "name": "Don Pedro Music",
        "short_name": "DonPedro",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#121212",
        "theme_color": "#1db954"
    })

async def api_buscar(request):
    query = request.query_params.get('q', '')
    if not query:
        return JSONResponse([])

    ydl_opts = {
        'extract_flat': True,
        'quiet': True,
        'extractor_args': {'youtube': {'player_client': ['android']}},
    }
    if os.path.exists("cookies.txt"):
        ydl_opts['cookiefile'] = "cookies.txt"

    loop = asyncio.get_event_loop()
    def _buscar():
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch10:{query}", download=False)
            return info.get('entries', [])

    try:
        entries = await loop.run_in_executor(None, _buscar)
        resultados = []
        for entry in entries:
            if entry:
                resultados.append({
                    "id": entry.get('id'),
                    "title": entry.get('title'),
                    "uploader": entry.get('uploader'),
                    "thumbnail": entry.get('thumbnail')
                })
        return JSONResponse(resultados)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

async def descargar_audio(request):
    video_id = request.path_params['video_id']
    url = f"https://www.youtube.com/watch?v={video_id}"

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(DOWNLOAD_DIR, '%(id)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'extractor_args': {'youtube': {'player_client': ['android']}},
    }
    if os.path.exists("cookies.txt"):
        ydl_opts['cookiefile'] = "cookies.txt"

    loop = asyncio.get_event_loop()
    def _descargar():
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(url, download=True)
            return os.path.join(DOWNLOAD_DIR, f"{video_id}.mp3")

    try:
        mp3_file = await loop.run_in_executor(None, _descargar)
        if os.path.exists(mp3_file):
            return JSONResponse({
                "status": "success",
                "download_url": f"/archivo/{video_id}.mp3"
            })
        else:
            return JSONResponse({"error": "No se generó el MP3"}, status_code=500)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

async def api_archivos(request):
    try:
        archivos = [f for f in os.listdir(DOWNLOAD_DIR) if f.endswith('.mp3')]
        return JSONResponse(archivos)
    except Exception as e:
        return JSONResponse([], status_code=500)

routes = [
    Route("/", home),
    Route("/manifest.json", manifest),
    Route("/api/buscar", api_buscar),
    Route("/api/archivos", api_archivos),
    Route("/descargar_mp3/{video_id}", descargar_audio),
    Mount("/archivo", StaticFiles(directory=DOWNLOAD_DIR), name="archivo"),
]

app = Starlette(routes=routes)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
