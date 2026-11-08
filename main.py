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
    <title>Don Pedro Music - Definitiva</title>
    <link rel="manifest" href="/manifest.json">
    <meta name="theme-color" content="#1db954">
</head>
<body style="background: #121212; color: #ffffff; font-family: Arial; padding: 15px; max-width: 600px; margin: 0 auto;">
    <h2 style="color: #1db954; text-align: center; margin-bottom: 5px;">🎵 Don Pedro Music 🎵</h2>
    <p style="text-align: center; color: #888; font-size: 12px; margin-top: 0;">Modo Venganza - Cero Bloqueos</p>

    <!-- ANUNCIO SUPERIOR -->
    <div style="background: #1e1e1e; border: 1px dashed #444; padding: 10px; text-align: center; margin-bottom: 15px; border-radius: 8px; color: #666;">
        [ Espacio para tu Anuncio / Banner Superior ]
    </div>

    <!-- BUSCADOR DIRECTO DESDE EL CLIENTE -->
    <div style="display: flex; gap: 10px; margin-bottom: 15px;">
        <input type="text" id="query" placeholder="Busca artista, cumbia o corrido..." onkeydown="if(event.key === 'Enter') buscarClient()" style="flex: 1; padding: 14px; background: #222; color: #fff; border: 1px solid #444; border-radius: 8px; font-size: 16px; outline: none;">
        <button onclick="buscarClient()" style="padding: 14px 20px; background: #1db954; color: #fff; border: none; border-radius: 8px; font-weight: bold; font-size: 16px; cursor: pointer;">Buscar</button>
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
    <div id="loading" style="text-align: center; color: #1db954; display: none; margin: 20px; font-weight: bold;">⚡ Buscando canciones...</div>
    <div id="results"></div>

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

        async function buscarClient() {
            const q = document.getElementById('query').value;
            if (!q) return;
            document.getElementById('loading').style.display = 'block';
            document.getElementById('results').innerHTML = '';
            document.getElementById('status').innerText = '';

            try {
                // Consultamos una API pública de Invidious directamente desde el navegador del usuario para evitar bloqueo de IP de Render
                let response = await fetch(`https://vid.priv.au/api/v1/search?q=${encodeURIComponent(q)}&type=video`);
                let data = await response.json();
                document.getElementById('loading').style.display = 'none';

                if (data && data.length > 0) {
                    let html = '';
                    data.slice(0, 15).forEach(item => {
                        let videoId = item.videoId;
                        let titulo = item.title.replace(/'/g, "").replace(/"/g, "");
                        let canal = item.author;
                        let miniatura = `https://i.ytimg.com/vi/${videoId}/hqdefault.jpg`;
                        let streamUrl = `https://www.youtube.com/watch?v=${videoId}`;

                        html += `
                            <div style="background: #1e1e1e; padding: 10px; margin-bottom: 12px; border-radius: 8px; border: 1px solid #333; display: flex; gap: 10px; align-items: center;">
                                <img src="${miniatura}" style="width: 75px; height: 55px; object-fit: cover; border-radius: 6px; background: #222;">
                                <div style="flex: 1; overflow: hidden;">
                                    <h4 style="margin: 0 0 4px 0; font-size: 13px; color: #fff; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${titulo}</h4>
                                    <p style="margin: 0 0 6px 0; font-size: 11px; color: #aaa;">${canal}</p>
                                    <div style="display: flex; align-items: center; gap: 8px;">
                                        <a href="https://www.youtube.com/watch?v=${videoId}" target="_blank" style="background: #333; color: #1db954; padding: 6px 10px; border-radius: 6px; text-decoration: none; font-size: 11px; font-weight: bold;">▶️ Ver</a>
                                        <button onclick="descargar('${videoId}', '${titulo}', this)" style="background: #282828; color: #1db954; border: 1px solid #1db954; padding: 6px 10px; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 11px;">📥 SD</button>
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
                document.getElementById('status').innerText = 'Error al buscar en los servidores públicos.';
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
                    document.getElementById('status').innerText = "¡Descarga lista al centavazo!";
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

async def descargar_audio(request):
    video_id = request.path_params['video_id']
    url = f"https://www.youtube.com/watch?v={video_id}"

    # El servidor solo procesa la descarga individual cuando tú le pides el MP3, usando cliente android optimizado
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
