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
    <title>Don Pedro Music - Reproductor Directo</title>
    <link rel="manifest" href="/manifest.json">
    <meta name="theme-color" content="#1db954">
</head>
<body style="background: #121212; color: #ffffff; font-family: Arial; padding: 15px; max-width: 600px; margin: 0 auto;">
    <h2 style="color: #1db954; text-align: center; margin-bottom: 5px;">🎵 Don Pedro Music 🎵</h2>
    <p style="text-align: center; color: #888; font-size: 12px; margin-top: 0;">Modo Directo - Cero Bloqueos</p>

    <!-- ANUNCIO SUPERIOR -->
    <div style="background: #1e1e1e; border: 1px dashed #444; padding: 10px; text-align: center; margin-bottom: 15px; border-radius: 8px; color: #666;">
        [ Espacio para tu Anuncio / Banner Superior ]
    </div>

    <!-- PANEL DE DESCARGA POR ENLACE DIRECTO -->
    <div style="background: #1a1a1a; padding: 12px; border-radius: 8px; border: 1px solid #333; margin-bottom: 15px;">
        <p style="margin: 0 0 8px 0; font-size: 13px; color: #ffeb3b; font-weight: bold;">📥 Pega el Link de YouTube para Bajar MP3</p>
        <div style="display: flex; gap: 8px;">
            <input type="text" id="yt-link" placeholder="https://www.youtube.com/watch?v=..." style="flex: 1; padding: 10px; background: #222; color: #fff; border: 1px solid #444; border-radius: 6px; font-size: 14px; outline: none;">
            <button onclick="descargarPorLink()" style="padding: 10px 16px; background: #1db954; color: #fff; border: none; border-radius: 6px; font-weight: bold; cursor: pointer;">Descargar</button>
        </div>
    </div>

    <!-- ECUALIZADOR DE BAJOS -->
    <div style="background: #1a1a1a; padding: 12px; border-radius: 8px; border: 1px solid #333; margin-bottom: 15px; text-align: center;">
        <p style="margin: 0 0 8px 0; font-size: 13px; color: #ffeb3b; font-weight: bold;">🎛️ Ecualizador de Bajos (Modo Taller)</p>
        <div style="display: flex; gap: 8px; justify-content: center; flex-wrap: wrap;">
            <button onclick="setBass(0)" style="background: #333; color: #fff; border: 1px solid #555; padding: 6px 12px; border-radius: 6px; cursor: pointer;">Normal</button>
            <button onclick="setBass(10)" style="background: #b22222; color: #fff; border: none; padding: 6px 12px; border-radius: 6px; cursor: pointer;">🔥 Mega Bajo</button>
            <button onclick="setBass(20)" style="background: #ff4500; color: #fff; border: none; padding: 6px 12px; border-radius: 6px; cursor: pointer;">⚡ Bajo a Tope</button>
        </div>
    </div>

    <div id="status" style="text-align: center; color: #ffeb3b; font-weight: bold; margin-bottom: 15px; font-size: 14px;"></div>

    <!-- INCORPORACIÓN DE YOUTUBE PARA VER Y ESCUCHAR LIBREMENTE -->
    <div style="background: #1e1e1e; padding: 10px; border-radius: 8px; border: 1px solid #333; text-align: center;">
        <p style="margin: 0 0 8px 0; font-size: 13px; color: #1db954; font-weight: bold;">📺 Buscador y Reproductor Oficial</p>
        <iframe width="100%" height="315" src="https://www.youtube.com/embed?listType=search&list=Musica" title="YouTube reproductor" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="border-radius: 6px;"></iframe>
    </div>

    <!-- ANUNCIO INFERIOR -->
    <div style="background: #1e1e1e; border: 1px dashed #444; padding: 10px; text-align: center; margin-top: 20px; border-radius: 8px; color: #666; font-size: 12px;">
        [ Espacio para tu Anuncio / Banner Inferior ]
    </div>

    <script>
        let audioCtx, sourceNode, bassFilter, currentAudioEl = null;

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
                console.log("Audio Context conectado");
            }
        }

        function setBass(gainValue) {
            if (bassFilter) {
                bassFilter.gain.setValueAtTime(gainValue, audioCtx.currentTime);
                document.getElementById('status').innerText = `🔊 Ecualizador aplicado: +${gainValue}dB de Bajo`;
            } else {
                document.getElementById('status').innerText = "⚠️ Reproduce algún audio primero.";
            }
        }

        async function descargarPorLink() {
            let link = document.getElementById('yt-link').value;
            if (!link) return;
            let match = link.match(/(?:v=|\/)([0-9A-Za-z_-]{11})/);
            if (!match) {
                document.getElementById('status').innerText = "⚠️ Enlace de YouTube no válido.";
                return;
            }
            let videoId = match[1];
            document.getElementById('status').innerText = "⏳ Generando MP3 desde el enlace...";

            try {
                let res = await fetch('/descargar_mp3/' + videoId);
                let data = await res.json();
                if (data.status === "success") {
                    document.getElementById('status').innerText = "¡Descarga lista al centavazo!";
                    window.location.href = data.download_url;
                } else {
                    document.getElementById('status').innerText = data.error || "Error al descargar.";
                }
            } catch (e) {
                document.getElementById('status').innerText = "Error de conexión.";
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
    Route("/descargar_mp3/{video_id}", descargar_audio),
    Mount("/archivo", StaticFiles(directory=DOWNLOAD_DIR), name="archivo"),
]

app = Starlette(routes=routes)

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
