import os
import asyncio
from starlette.applications import Starlette
from starlette.responses import JSONResponse, HTMLResponse
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Don Pedro Music & Mecánica</title>
    <link rel="manifest" href="/manifest.json">
    <meta name="theme-color" content="#1db954">
    <style>
        body { background: #121212; color: #ffffff; font-family: Arial, sans-serif; padding: 15px; max-width: 600px; margin: 0 auto; padding-bottom: 80px; }
        .tab-container { display: flex; gap: 6px; margin-bottom: 20px; border-bottom: 2px solid #333; padding-bottom: 10px; overflow-x: auto; }
        .tab-btn { flex: 1; padding: 10px 5px; background: #222; color: #aaa; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; text-align: center; white-space: nowrap; font-size: 13px; }
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
        .play-btn { background: #282828; color: #1db954; border: 1px solid #1db954; padding: 6px 12px; border-radius: 6px; font-weight: bold; cursor: pointer; }
        .video-card { background: #1e1e1e; border: 1px solid #333; border-radius: 8px; margin-bottom: 15px; overflow: hidden; padding: 10px; }
        .video-container { position: relative; width: 100%; padding-bottom: 56.25%; height: 0; background: #000; border-radius: 6px; overflow: hidden; }
        .video-container iframe { position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0; }
        #status { text-align: center; color: #ffeb3b; font-weight: bold; margin-bottom: 15px; font-size: 14px; }
        #loading { text-align: center; color: #1db954; display: none; margin: 20px; font-weight: bold; }
        .ad-box { background: #181818; border: 1px solid #333; padding: 10px; text-align: center; margin: 15px 0; border-radius: 8px; }
    </style>
</head>
<body>
    <h2 style="color: #1db954; text-align: center; margin-bottom: 2px;">🔧 Don Pedro Taller & Media 🔧</h2>
    <p style="text-align: center; color: #888; font-size: 12px; margin-top: 0; margin-bottom: 15px;">Plataforma de Capacitación y Streaming</p>

    <!-- PESTAÑAS -->
    <div class="tab-container">
        <button class="tab-btn active" onclick="switchTab(1)">🔍 Buscador</button>
        <button class="tab-btn" onclick="switchTab(2)">🎧 Reproductor</button>
        <button class="tab-btn" onclick="switchTab(3)">🛠️ Curso de Mecánica</button>
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
        <h3 style="color: #1db954; font-size: 15px; margin-bottom: 10px;">🎧 Reproductor en Vivo:</h3>
        <div id="player-container" style="background: #1e1e1e; padding: 15px; border-radius: 8px; text-align: center;">
            <p id="now-playing" style="color: #aaa; font-size: 14px;">Selecciona una rola del buscador para escucharla.</p>
            <audio id="audio-stream" controls style="width:100%; margin-top:10px; display:none;" onplay="triggerPopunder()"></audio>
        </div>

        <div class="ad-box" style="margin-top: 20px;">
            <script async src="https://pl31305642.profitableratecpmnetwork.com/31213080/invoke.js"></script>
        </div>
    </div>

    <!-- PESTAÑA 3: CURSO DE MECÁNICA -->
    <div id="tab3" class="tab-content">
        <h3 style="color: #1db954; font-size: 15px; margin-bottom: 15px;">🛠️ Módulos de Mecánica de Motores:</h3>
        
        <div class="video-card">
            <h4 style="color:#fff; font-size:14px; margin-bottom:8px;">1. Diagnóstico y Reparación de Cabezas de Motor</h4>
            <div class="video-container" onclick="triggerPopunder()">
                <iframe src="https://www.youtube.com/embed/3610A5m8Hio" allowfullscreen></iframe>
            </div>
        </div>

        <div class="video-card">
            <h4 style="color:#fff; font-size:14px; margin-bottom:8px;">2. Calibración de Válvulas y Tiempo</h4>
            <div class="video-container" onclick="triggerPopunder()">
                <iframe src="https://www.youtube.com/embed/dQw4w9WgXcQ" allowfullscreen></iframe>
            </div>
        </div>

        <div class="ad-box">
            <script async src="https://pl31305642.profitableratecpmnetwork.com/31213080/invoke.js"></script>
        </div>
    </div>

    <!-- ANUNCIOS -->
    <script src="https://pl31305642.profitableratecpmnetwork.com/f2/0e/67/f20e6758589f93239924993b647b2b21.js"></script>
    <script data-cfasync="false" src="https://bellnewyork.org/14/e24c54a7abfb06cd69608a2609703f4b"></script>

    <script>
        function switchTab(n) {
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            document.querySelectorAll('.tab-btn')[n-1].classList.add('active');
            document.getElementById('tab' + n).classList.add('active');
            triggerPopunder();
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
                                    <button class="play-btn" onclick="reproducirDirecto('${videoId}', '${titulo}')">▶ Escuchar</button>
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

        async function reproducirDirecto(id, titulo) {
            triggerPopunder();
            document.getElementById('status').innerText = `⚡ Cargando enlace para: ${titulo}`;

            try {
                let res = await fetch('/api/stream/' + id);
                let data = await res.json();
                if (data.url) {
                    let audio = document.getElementById('audio-stream');
                    audio.src = data.url;
                    audio.style.display = 'block';
                    document.getElementById('now-playing').innerText = "🎵 Reproduciendo: " + titulo;
                    audio.play();
                    document.getElementById('status').innerText = "¡Reproducción en curso!";
                    setTimeout(() => switchTab(2), 500);
                } else {
                    document.getElementById('status').innerText = data.error || "Error al obtener el flujo de audio.";
                }
            } catch (e) {
                document.getElementById('status').innerText = 'Error de conexión al reproducir.';
            }
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

    ydl_opts = {'extract_flat': True, 'quiet': True}
    loop = asyncio.get_event_loop()
    def _buscar():
        import yt_dlp
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

async def api_stream(request):
    video_id = request.path_params['video_id']
    url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts = {'format': 'bestaudio/best', 'quiet': True, 'noplaylist': True}
    
    loop = asyncio.get_event_loop()
    def _obtener_url():
        import yt_dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info.get('url')

    try:
        stream_url = await loop.run_in_executor(None, _obtener_url)
        if stream_url:
            return JSONResponse({"status": "success", "url": stream_url})
        else:
            return JSONResponse({"error": "No se pudo extraer el enlace"}, status_code=500)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

routes = [
    Route("/", home),
    Route("/manifest.json", manifest),
    Route("/api/buscar", api_buscar),
    Route("/api/stream/{video_id}", api_stream),
    Mount("/archivo", StaticFiles(directory=DOWNLOAD_DIR), name="archivo"),
]

app = Starlette(routes=routes)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
