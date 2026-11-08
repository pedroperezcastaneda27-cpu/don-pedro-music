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
    <title>Don Pedro Music - Reproductor y Descargador</title>
    <link rel="manifest" href="/manifest.json">
    <meta name="theme-color" content="#1db954">
</head>
<body style="background: #121212; color: #ffffff; font-family: Arial; padding: 15px; max-width: 600px; margin: 0 auto;">
    <h2 style="color: #1db954; text-align: center; margin-bottom: 5px;">🎵 Don Pedro Music 🎵</h2>
    <p style="text-align: center; color: #888; font-size: 12px; margin-top: 0;">Reproductor, Bajos Pesados y Descargas</p>

    <!-- ANUNCIO SUPERIOR -->
    <div style="background: #1e1e1e; border: 1px dashed #444; padding: 10px; text-align: center; margin-bottom: 15px; border-radius: 8px; color: #666;">
        [ Espacio para tu Anuncio / Banner Superior ]
    </div>

    <!-- BOTÓN DE INSTALACIÓN PWA -->
    <div id="install-container" style="text-align: center; margin-bottom: 15px; display: none;">
        <button id="btn-install" style="background: #1db954; color: #fff; border: none; padding: 10px 18px; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 14px;">📱 Instalar App en el Cel</button>
    </div>

    <!-- PANEL DE CONTROL Y BUSCADOR -->
    <div style="display: flex; gap: 10px; margin-bottom: 15px;">
        <input type="text" id="query" placeholder="Busca artista, cumbia o corrido..." onkeydown="if(event.key === 'Enter') buscar()" style="flex: 1; padding: 14px; background: #222; color: #fff; border: 1px solid #444; border-radius: 8px; font-size: 16px; outline: none;">
        <button onclick="buscar()" style="padding: 14px 20px; background: #1db954; color: #fff; border: none; border-radius: 8px; font-weight: bold; font-size: 16px; cursor: pointer;">Buscar</button>
    </div>

    <!-- ECUALIZADOR / BOTONES DE BAJOS PESADOS -->
    <div style="background: #1a1a1a; padding: 12px; border-radius: 8px; border: 1px solid #333; margin-bottom: 15px; text-align: center;">
        <p style="margin: 0 0 8px 0; font-size: 13px; color: #ffeb3b; font-weight: bold;">🎛️ Ecualizador de Bajos (Modo Taller)</p>
        <div style="display: flex; gap: 8px; justify-content: center; flex-wrap: wrap;">
            <button onclick="setBass(0)" style="background: #333; color: #fff; border: 1px solid #555; padding: 6px 12px; border-radius: 6px; cursor: pointer;">Normal</button>
            <button onclick="setBass(10)" style="background: #b22222; color: #fff; border: none; padding: 6px 12px; border-radius: 6px; cursor: pointer;">🔥 Mega Bajo</button>
            <button onclick="setBass(20)" style="background: #ff4500; color: #fff; border: none; padding: 6px 12px; border-radius: 6px; cursor: pointer;">⚡ Bajo a Tope</button>
        </div>
    </div>

    <div id="status" style="text-align: center; color: #ffeb3b; font-weight: bold; margin-bottom: 15px; font-size: 14px;"></div>
    <div id="loading" style="text-align: center; color: #1db954; display: none; margin: 20px; font-weight: bold;">⚡ Buscando repertorio con carátulas...</div>
    <div id="results"></div>

    <!-- ANUNCIO INFERIOR -->
    <div style="background: #1e1e1e; border: 1px dashed #444; padding: 10px; text-align: center; margin-top: 20px; border-radius: 8px; color: #666; font-size: 12px;">
        [ Espacio para tu Anuncio / Banner Inferior ]
    </div>

    <script>
        let audioCtx, sourceNode, bassFilter, currentAudioEl = null;

        let deferredPrompt;
        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            deferredPrompt = e;
            document.getElementById('install-container').style.display = 'block';
        });

        document.getElementById('btn-install').addEventListener('click', async () => {
            if (deferredPrompt) {
                deferredPrompt.prompt();
                let { outcome } = await deferredPrompt.userChoice;
                if (outcome === 'accepted') {
                    document.getElementById('install-container').style.display = 'none';
                }
                deferredPrompt = null;
            }
        });

        function initAudioContext(audioEl) {
            if (currentAudioEl === audioEl) return;
            currentAudioEl = audioEl;

            if (!audioCtx) {
                audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            }
            if (audioCtx.state === 'suspended') {
                audioCtx.resume();
            }

            try {
                if (sourceNode) sourceNode.disconnect();
                sourceNode = audioCtx.createMediaElementSource(audioEl);
                bassFilter = audioCtx.createBiquadFilter();
                bassFilter.type = "lowshelf";
                bassFilter.frequency.setValueAtTime(150, audioCtx.currentTime);
                bassFilter.gain.setValueAtTime(0, audioCtx.currentTime);

                sourceNode.connect(bassFilter);
                bassFilter.connect(audioCtx.destination);
            } catch (e) {
                console.log("Audio Context ya conectado");
            }
        }

        function setBass(gainValue) {
            if (bassFilter) {
                bassFilter.gain.setValueAtTime(gainValue, audioCtx.currentTime);
                document.getElementById('status').innerText = `🔊 Ecualizador aplicado: +${gainValue}dB de Bajo`;
            } else {
                document.getElementById('status').innerText = "⚠️ Dale play a alguna rola primero para activar el bajo.";
            }
        }

        async function buscar() {
            const q = document.getElementById('query').value;
            if (!q) return;
            document.getElementById('loading').style.display = 'block';
            document.getElementById('results').innerHTML = '';
            document.getElementById('status').innerText = '';

            try {
                let res = await fetch('/buscar?q=' + encodeURIComponent(q));
                let data = await res.json();
                document.getElementById('loading').style.display = 'none';

                if (data.resultados && data.resultados.length > 0) {
                    let html = '';
                    data.resultados.forEach(item => {
                        let tituloLimpio = item.titulo.replace(/'/g, "").replace(/"/g, "");
                        html += `
                            <div style="background: #1e1e1e; padding: 10px; margin-bottom: 12px; border-radius: 8px; border: 1px solid #333; display: flex; gap: 10px; align-items: center;">
                                <img src="${item.miniatura}" style="width: 75px; height: 55px; object-fit: cover; border-radius: 6px; background: #222;">
                                <div style="flex: 1; overflow: hidden;">
                                    <h4 style="margin: 0 0 4px 0; font-size: 13px; color: #fff; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${item.titulo}</h4>
                                    <p style="margin: 0 0 6px 0; font-size: 11px; color: #aaa;">${item.canal}</p>
                                    <div style="display: flex; align-items: center; gap: 8px;">
                                        <audio controls onplay="initAudioContext(this)" style="flex: 1; height: 32px;" src="${item.stream_url}"></audio>
                                        <button onclick="descargar('${item.id}', '${tituloLimpio}', this)" style="background: #282828; color: #1db954; border: 1px solid #1db954; padding: 6px 10px; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 11px;">📥 SD</button>
                                    </div>
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
                document.getElementById('status').innerText = 'Error al buscar.';
            }
        }

        async function descargar(id, titulo, btn) {
            btn.innerText = "⏳...";
            btn.disabled = true;
            document.getElementById('status').innerText = `⏳ Generando MP3 de "${titulo}"...`;

            try {
                let res = await fetch('/descargar_mp3/' + id);
                let data = await res.json();
                if (data.status === "success") {
                    btn.innerText = "✅ ¡Listo!";
                    btn.style.background = "#1db954";
                    btn.style.color = "#fff";
                    document.getElementById('status').innerText = "¡Descarga lista en tu dispositivo!";
                    window.location.href = data.download_url;
                } else {
                    btn.innerText = "📥 SD";
                    btn.disabled = false;
                    document.getElementById('status').innerText = data.error || "Error en la descarga.";
                }
            } catch (e) {
                btn.innerText = "📥 SD";
                btn.disabled = false;
                document.getElementById('status').innerText = 'Error de conexión.';
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
        "theme_color": "#1db954",
        "icons": [{
            "src": "https://img.icons8.com/color/512/youtube-music.png",
            "sizes": "512x512",
            "type": "image/png"
        }]
    })

async def buscar_canciones(request):
    q = request.query_params.get("q", "")
    if not q:
        return JSONResponse({"error": "Vacío"}, status_code=400)

    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'default_search': 'ytsearch30',
        'socket_timeout': 10,
        'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
        'match_filter': yt_dlp.utils.match_filter_func("duration < 720"),
    }

    loop = asyncio.get_event_loop()
    def _buscar():
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(f"ytsearch30:{q}", download=False)

    try:
        info = await loop.run_in_executor(None, _buscar)
        resultados = []
        titulos_vistos = set()

        for entry in info.get('entries', []):
            if entry and entry.get('url'):
                titulo_original = entry.get('title', '')
                titulo_normalizado = "".join(c.lower() for c in titulo_original if c.isalnum())

                if titulo_normalizado not in titulos_vistos:
                    titulos_vistos.add(titulo_normalizado)
                    video_id = entry.get('id')
                    thumbnail_url = entry.get('thumbnail') or f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"

                    resultados.append({
                        'id': video_id,
                        'titulo': titulo_original,
                        'canal': entry.get('uploader'),
                        'stream_url': entry.get('url'),
                        'miniatura': thumbnail_url
                    })

        return JSONResponse({"status": "ok", "resultados": resultados[:25]})
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
        'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
        'match_filter': yt_dlp.utils.match_filter_func("duration < 720"),
    }

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

routes = [
    Route("/", home),
    Route("/manifest.json", manifest),
    Route("/buscar", buscar_canciones),
    Route("/descargar_mp3/{video_id}", descargar_audio),
    Mount("/archivo", StaticFiles(directory=DOWNLOAD_DIR), name="archivo"),
]

app = Starlette(routes=routes)

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
