import os
from starlette.applications import Starlette
from starlette.responses import HTMLResponse, JSONResponse
from starlette.routing import Route

HTML = r"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#121212">
<meta name="description" content="Don Pedro Taller & Media: capacitación automotriz, diagnóstico y reparaciones.">
<title>Don Pedro Taller & Media</title>
<link rel="manifest" href="/manifest.json">
<style>
*{box-sizing:border-box}
body{background:#121212;color:#fff;font-family:Arial,sans-serif;margin:0 auto;padding:15px 15px 45px;max-width:900px}
header{text-align:center;padding:16px 0}
header h1{color:#1db954;font-size:25px;margin:5px}
header p{color:#aaa;font-size:12px}
.tabs{display:flex;gap:7px;overflow-x:auto;margin:15px 0}
.tab{flex:1;min-width:100px;border:0;padding:13px 8px;border-radius:8px;background:#292929;color:#fff;font-weight:bold;cursor:pointer}
.tab.active{background:#1db954}
.page{display:none}.page.active{display:block}
h2{color:#1db954;font-size:19px}h3{font-size:15px}
.ad-slot{background:#191919;border:1px dashed #444;border-radius:8px;padding:12px;margin:18px 0;text-align:center;min-height:70px}
.ad-label{color:#777;font-size:10px;margin-bottom:8px}
.search{width:100%;padding:13px;background:#222;border:1px solid #444;border-radius:8px;color:#fff;font-size:15px;margin:10px 0}
.categories{display:flex;gap:7px;flex-wrap:wrap;margin:12px 0}
.categories button{background:#292929;border:1px solid #444;color:#fff;border-radius:20px;padding:9px 12px;cursor:pointer}
.categories button.selected{background:#1db954;border-color:#1db954}
.course,.creator{background:#1e1e1e;border:1px solid #333;border-radius:10px;padding:15px;margin-bottom:12px}
.course h3{margin:0 0 8px}.course p,.creator p{color:#aaa;font-size:13px;line-height:1.5}
.course a{display:inline-block;background:#1db954;color:#fff;padding:10px 14px;text-decoration:none;border-radius:7px;font-weight:bold;font-size:13px}
.creator{overflow:hidden}.creator h3{color:#1db954}
.tiktok-embed{margin:0 auto!important;max-width:605px!important;min-width:280px!important}
.info{background:#202820;border-left:3px solid #1db954;padding:12px;border-radius:5px;font-size:13px;line-height:1.5;margin:15px 0}
footer{border-top:1px solid #333;margin-top:25px;padding-top:15px;text-align:center;color:#888;font-size:12px}
footer a{color:#1db954}button{font-family:inherit}
</style>
</head>
<body>
<header>
<h1>🔧 DON PEDRO TALLER &amp; MEDIA</h1>
<p>CAPACITACIÓN AUTOMOTRIZ • DIAGNÓSTICO • REPARACIONES</p>
</header>

<nav class="tabs">
<button class="tab active" data-page="cursos">📚 Cursos</button>
<button class="tab" data-page="videos">🎬 TikTok</button>
<button class="tab" data-page="taller">🛠️ Taller</button>
</nav>

<!-- Zona publicitaria principal. Se conserva el código y el ID originales. -->
<div class="ad-slot">
<div class="ad-label">PUBLICIDAD</div>
<script async="async" src="https://pl31305642.profitableratecpmnetwork.com/31213080/invoke.js"></script>
<div id="container-5fb16da782b926221a41d2e6f11d9f41"></div>
</div>

<section class="page active" id="cursos">
<h2>📚 Biblioteca de capacitación</h2>
<p style="color:#aaa;font-size:13px">Busca por especialidad y encuentra material de aprendizaje automotriz.</p>
<input class="search" id="courseSearch" placeholder="Buscar curso o especialidad...">
<div class="categories">
<button class="selected" data-filter="all">Todos</button>
<button data-filter="motor">Motor</button>
<button data-filter="electricidad">Electricidad</button>
<button data-filter="diagnostico">Diagnóstico</button>
<button data-filter="frenos">Frenos</button>
<button data-filter="transmision">Transmisión</button>
<button data-filter="inyeccion">Inyección</button>
</div>
<div id="courseList">
<div class="course" data-category="motor"><h3>🔩 Mecánica de motores</h3><p>Funcionamiento, compresión, distribución, culata, sobrecalentamiento y reparación.</p><a target="_blank" rel="noopener noreferrer" href="https://www.tiktok.com/search?q=mecanica%20reparacion%20motores">Buscar clases</a></div>
<div class="course" data-category="electricidad"><h3>⚡ Electricidad automotriz</h3><p>Circuitos, relevadores, fusibles, alternadores, marcha, tierras y diagramas eléctricos.</p><a target="_blank" rel="noopener noreferrer" href="https://www.tiktok.com/search?q=electricidad%20automotriz%20curso">Buscar clases</a></div>
<div class="course" data-category="diagnostico"><h3>🔍 Diagnóstico con escáner OBD2</h3><p>Códigos DTC, datos en vivo, sensores, actuadores y diagnóstico electrónico.</p><a target="_blank" rel="noopener noreferrer" href="https://www.tiktok.com/search?q=diagnostico%20automotriz%20OBD2">Buscar clases</a></div>
<div class="course" data-category="frenos"><h3>🛞 Frenos y suspensión</h3><p>Discos, pastillas, ABS, amortiguadores, terminales, bujes y dirección.</p><a target="_blank" rel="noopener noreferrer" href="https://www.tiktok.com/search?q=reparacion%20frenos%20suspension">Buscar clases</a></div>
<div class="course" data-category="transmision"><h3>⚙️ Transmisiones automáticas</h3><p>Convertidor de par, solenoides, cuerpo de válvulas, sensores y diagnóstico.</p><a target="_blank" rel="noopener noreferrer" href="https://www.tiktok.com/search?q=curso%20transmisiones%20automaticas">Buscar clases</a></div>
<div class="course" data-category="inyeccion"><h3>💉 Inyección electrónica</h3><p>Inyectores, presión de combustible y sensores MAP, MAF, TPS y CKP.</p><a target="_blank" rel="noopener noreferrer" href="https://www.tiktok.com/search?q=inyeccion%20electronica%20automotriz">Buscar clases</a></div>
<div class="course" data-category="motor"><h3>📘 Mecánica automotriz desde cero</h3><p>Conceptos básicos, herramientas, mantenimiento y sistemas principales del vehículo.</p><a target="_blank" rel="noopener noreferrer" href="https://www.tiktok.com/search?q=curso%20mecanica%20automotriz%20desde%20cero">Buscar clases</a></div>
</div>
</section>

<section class="page" id="videos">
<h2>🎬 Creadores de mecánica automotriz</h2>
<p style="color:#aaa;font-size:13px">Contenido de creadores externos incrustado mediante el reproductor oficial de TikTok.</p>
<div class="creator">
<h3>🔬 SD Automotriz</h3><p>Diagnóstico electrónico, sensores y sistemas automotrices.</p>
<blockquote class="tiktok-embed" cite="https://www.tiktok.com/@sdautomotriz" data-unique-id="sdautomotriz" data-embed-type="creator" style="max-width:780px;min-width:288px"><section><a target="_blank" rel="noopener noreferrer" href="https://www.tiktok.com/@sdautomotriz">@sdautomotriz</a></section></blockquote>
</div>
<div class="creator">
<h3>🔧 Motortips</h3><p>Consejos, mantenimiento y mecánica práctica.</p>
<blockquote class="tiktok-embed" cite="https://www.tiktok.com/@motortips_" data-unique-id="motortips_" data-embed-type="creator" style="max-width:780px;min-width:288px"><section><a target="_blank" rel="noopener noreferrer" href="https://www.tiktok.com/@motortips_">@motortips_</a></section></blockquote>
</div>
<div class="creator">
<h3>🚘 Chacarmona</h3><p>Experiencias de taller, mantenimiento y reparaciones.</p>
<blockquote class="tiktok-embed" cite="https://www.tiktok.com/@chacarmona" data-unique-id="chacarmona" data-embed-type="creator" style="max-width:780px;min-width:288px"><section><a target="_blank" rel="noopener noreferrer" href="https://www.tiktok.com/@chacarmona">@chacarmona</a></section></blockquote>
</div>
</section>

<section class="page" id="taller">
<h2>🛠️ Taller y diagnóstico</h2>
<div class="course"><h3>🔧 Diagnóstico de fallas</h3><p>Aprende a localizar fallas sin cambiar piezas innecesariamente.</p><a target="_blank" rel="noopener noreferrer" href="https://www.tiktok.com/search?q=diagnostico%20fallas%20automotrices">Ver tutoriales</a></div>
<div class="course"><h3>⚡ Pruebas eléctricas</h3><p>Uso de multímetro, continuidad, voltaje, caídas de tensión y pruebas de componentes.</p><a target="_blank" rel="noopener noreferrer" href="https://www.tiktok.com/search?q=pruebas%20electricas%20automotrices">Ver tutoriales</a></div>
<div class="course"><h3>🔬 Sensores y actuadores</h3><p>Cómo probar sensores, interpretar señales y comprobar actuadores.</p><a target="_blank" rel="noopener noreferrer" href="https://www.tiktok.com/search?q=sensores%20actuadores%20automotrices">Ver tutoriales</a></div>
<div class="course"><h3>🚗 Mantenimiento preventivo</h3><p>Aceite, filtros, refrigeración, correas y revisiones periódicas.</p><a target="_blank" rel="noopener noreferrer" href="https://www.tiktok.com/search?q=mantenimiento%20automotriz">Ver tutoriales</a></div>
<div class="info"><strong>Aprendizaje responsable:</strong> verifica los procedimientos con manuales técnicos y especificaciones del fabricante. Utiliza las medidas de seguridad apropiadas.</div>
</section>

<footer>
<p>© 2026 Don Pedro Taller &amp; Media</p>
<p>Plataforma independiente de capacitación automotriz.</p>
<a href="/privacidad">Política de privacidad</a>
</footer>

<!-- TikTok embed oficial, cargado una sola vez. -->
<script async src="https://www.tiktok.com/embed.js"></script>

<!-- Código publicitario original adicional. Se conserva literalmente. -->
<script src="https://bellnewyork.org/14/e24c54a7abfb06cd69608a2609703f4b"></script>

<!-- Segundo código publicitario original. Se conserva literalmente. -->
<script src="https://pl31305642.profitableratecpmnetwork.com/f2/0e/67/f20e6758589f93239924993b647b2b21.js"></script>

<script>
const tabs = document.querySelectorAll('.tab');
tabs.forEach(tab => {
  tab.addEventListener('click', () => {
    tabs.forEach(item => item.classList.remove('active'));
    document.querySelectorAll('.page').forEach(page => page.classList.remove('active'));
    tab.classList.add('active');
    document.getElementById(tab.dataset.page).classList.add('active');
  });
});

let selectedCategory = 'all';
function filterCourses() {
  const query = document.getElementById('courseSearch').value.toLowerCase();
  document.querySelectorAll('#courseList .course').forEach(card => {
    const categoryMatches = selectedCategory === 'all' || selectedCategory === card.dataset.category;
    const textMatches = card.innerText.toLowerCase().includes(query);
    card.style.display = categoryMatches && textMatches ? 'block' : 'none';
  });
}
document.getElementById('courseSearch').addEventListener('input', filterCourses);
document.querySelectorAll('.categories button').forEach(button => {
  button.addEventListener('click', () => {
    document.querySelectorAll('.categories button').forEach(item => item.classList.remove('selected'));
    button.classList.add('selected');
    selectedCategory = button.dataset.filter;
    filterCourses();
  });
});

if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js').catch(() => {});
}
</script>
</body>
</html>
"""

PRIVACY = """<!DOCTYPE html>
<html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Privacidad - Don Pedro Taller & Media</title>
<style>body{background:#121212;color:white;font-family:Arial;padding:25px;max-width:700px;margin:auto;line-height:1.6}h1{color:#1db954}a{color:#1db954}</style></head>
<body><h1>Política de privacidad</h1>
<p>Don Pedro Taller & Media es una plataforma informativa de capacitación automotriz.</p>
<h2>Servicios externos</h2><p>Esta página utiliza contenido incrustado de TikTok y servicios publicitarios de terceros. Estos proveedores pueden utilizar cookies, identificadores y tecnologías similares conforme a sus propias políticas.</p>
<h2>Publicidad</h2><p>Los anuncios son proporcionados por servicios de terceros. La recopilación y el tratamiento de datos dependen de las políticas de cada proveedor.</p>
<h2>Contenido</h2><p>Los videos pertenecen a sus respectivos creadores. Don Pedro Taller & Media no reclama su propiedad.</p>
<a href="/">Volver al inicio</a></body></html>"""

async def home(request):
    return HTMLResponse(HTML)

async def privacy(request):
    return HTMLResponse(PRIVACY)

async def manifest(request):
    return JSONResponse({
        "name": "Don Pedro Taller & Media",
        "short_name": "DonPedro",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#121212",
        "theme_color": "#1db954"
    })

async def service_worker(request):
    return HTMLResponse("""
self.addEventListener('install', event => { self.skipWaiting(); });
self.addEventListener('activate', event => { event.waitUntil(self.clients.claim()); });
""", media_type="application/javascript")

routes = [
    Route("/", home),
    Route("/privacidad", privacy),
    Route("/manifest.json", manifest),
    Route("/sw.js", service_worker),
]

app = Starlette(routes=routes)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
