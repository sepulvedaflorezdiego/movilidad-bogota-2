from google.colab import files

codigo_html = r"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Movilidad Bogotá D.C. - Datos oficiales TransMilenio / SITP</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css" />
<style>
:root{--primary:#0056b3;--primary-dark:#003d80;--tm-red:#dc2626;--sitp-blue:#0284c7;--feed-green:#16a34a;--walk-gray:#334155;--accent:#25d366;--bg:#f8fafc;--text:#1e293b;--text-muted:#64748b}
*{box-sizing:border-box;font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif}
body{margin:0;padding:15px;background:var(--bg);color:var(--text)}
.dashboard{max-width:900px;margin:0 auto;display:flex;flex-direction:column;gap:15px}
.header-card{background:linear-gradient(135deg,#0056b3 0%,#002d5e 100%);color:#fff;padding:20px 24px;border-radius:16px;box-shadow:0 10px 25px -5px rgba(0,86,179,.3);display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px}
.header-title h2{margin:0;font-size:22px;font-weight:700;display:flex;align-items:center;gap:10px}
.header-title p{margin:4px 0 0;opacity:.85;font-size:13px}
.live-clock{background:rgba(255,255,255,.15);backdrop-filter:blur(8px);padding:8px 16px;border-radius:12px;border:1px solid rgba(255,255,255,.2);text-align:right}
.clock-time{font-size:18px;font-weight:800}.clock-date{font-size:11px;opacity:.9;text-transform:capitalize}
.card{background:#fff;border-radius:16px;padding:20px;box-shadow:0 4px 20px -2px rgba(0,0,0,.05)}
.inputs-grid{display:grid;grid-template-columns:1fr 1fr auto;gap:12px}
.input-group{display:flex;flex-direction:column;gap:6px}
.input-group label{font-size:12px;font-weight:700;color:var(--text-muted);text-transform:uppercase;letter-spacing:.5px}
.input-wrapper{position:relative}
.input-wrapper i{position:absolute;left:14px;top:50%;transform:translateY(-50%);color:var(--primary);z-index:2}
input,select{width:100%;padding:12px 14px 12px 40px;border:1.5px solid #e2e8f0;border-radius:10px;font-size:14px;outline:none;background:#fff}
input:focus,select:focus{border-color:var(--primary);box-shadow:0 0 0 3px rgba(0,86,179,.15)}
button.btn-search{padding:0 24px;height:45px;align-self:flex-end;background:var(--primary);color:#fff;border:none;border-radius:10px;cursor:pointer;font-weight:700;font-size:14px;display:flex;align-items:center;gap:8px}
button.btn-search:hover{background:var(--primary-dark)}
.bus-selector-box{background:#eff6ff;border:1.5px solid #bfdbfe;border-radius:12px;padding:14px 16px;display:flex;flex-direction:column;gap:8px}
.bus-selector-box label{font-size:13px;font-weight:800;color:#1e40af;display:flex;align-items:center;gap:8px}
#mapContainer{height:440px;width:100%;border-radius:14px;overflow:hidden;border:1px solid #e2e8f0;z-index:0}
.address-badge-card{display:grid;grid-template-columns:1fr 1fr;gap:12px;background:#f1f5f9;padding:12px 16px;border-radius:12px;border:1px solid #e2e8f0;margin-bottom:12px}
.address-item{font-size:12px}.address-item b{display:flex;align-items:center;gap:6px;color:var(--primary-dark);margin-bottom:3px;font-size:11px;text-transform:uppercase}
.alert-banner{display:none;background:#fffbeb;border-left:4px solid #f59e0b;color:#b45309;padding:14px 18px;border-radius:10px;font-size:13px;line-height:1.5}
.alert-banner.active{display:flex;gap:12px;align-items:flex-start}.alert-banner i{font-size:18px;margin-top:2px}
.timeline-title{font-weight:700;margin:15px 0 14px;display:flex;align-items:center;gap:8px;font-size:15px;color:var(--primary-dark)}
.step-card{display:flex;gap:14px;padding:16px;background:#fff;border:1px solid #e2e8f0;border-radius:14px;margin-bottom:12px;align-items:flex-start;box-shadow:0 2px 8px rgba(0,0,0,.03)}
.step-icon-box{width:46px;height:46px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:20px;color:#fff;flex-shrink:0}
.icon-walk{background:var(--walk-gray)}.icon-tm{background:var(--tm-red)}.icon-sitp{background:var(--sitp-blue)}.icon-feed{background:var(--feed-green)}
.step-content{flex:1;font-size:13px;line-height:1.5}
.step-title-line{font-weight:700;display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:6px;font-size:14px}
.badge-bus{display:inline-flex;align-items:center;gap:5px;padding:4px 10px;border-radius:8px;font-size:12px;font-weight:800;color:#fff}
.badge-tm{background:var(--tm-red)}.badge-sitp{background:var(--sitp-blue)}.badge-feed{background:var(--feed-green)}
.step-details{color:#475569}
.pill{display:inline-block;background:#f1f5f9;border-radius:6px;padding:2px 8px;margin:4px 6px 0 0;font-size:12px;font-weight:600;color:#334155}
.metrics-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;margin-bottom:12px}
.metric-card{background:#f1f5f9;padding:14px 16px;border-radius:12px;display:flex;align-items:center;gap:14px}
.metric-icon{width:42px;height:42px;border-radius:10px;background:#fff;color:var(--primary);display:flex;align-items:center;justify-content:center;font-size:18px;box-shadow:0 2px 6px rgba(0,0,0,.06)}
.metric-info label{font-size:11px;color:var(--text-muted);font-weight:600;text-transform:uppercase;display:block}
.metric-info span{font-size:15px;font-weight:800}
.share-box{margin-top:15px;padding:16px;background:#f0fdf4;border:1px solid #bbf7d0;border-radius:12px;display:flex;flex-direction:column;gap:10px}
.share-input-wrapper{display:flex;gap:8px}.share-input-wrapper input{padding-left:12px;font-size:13px}
button.btn-share{background:var(--accent);color:#fff;border:none;padding:0 18px;border-radius:8px;font-weight:700;cursor:pointer;display:flex;align-items:center;gap:6px;white-space:nowrap}
.note{font-size:12px;color:#475569;line-height:1.5}
@media(max-width:768px){.inputs-grid,.address-badge-card{grid-template-columns:1fr}button.btn-search{width:100%;justify-content:center}.header-card{flex-direction:column;align-items:flex-start}.live-clock{width:100%;text-align:left}}
</style>
</head>
<body>
<div class="dashboard">
  <div class="header-card">
    <div class="header-title">
      <h2><i class="fa-solid fa-map-location-dot"></i> Rutas oficiales TransMilenio y SITP - Bogotá D.C.</h2>
      <p>Datos abiertos de TRANSMILENIO S.A.: trazados de rutas, estaciones y horarios</p>
    </div>
    <div class="live-clock"><div class="clock-time" id="clockTime">--:--:--</div><div class="clock-date" id="clockDate">Cargando fecha...</div></div>
  </div>

  <div class="card">
    <div class="inputs-grid">
      <div class="input-group"><label>Punto A (Origen)</label>
        <div class="input-wrapper"><i class="fa-solid fa-location-dot"></i>
        <input type="text" id="origen" placeholder="Ej: Portal Norte" value="Portal Norte" autocomplete="off"></div></div>
      <div class="input-group"><label>Punto B (Destino)</label>
        <div class="input-wrapper"><i class="fa-solid fa-flag-checkered"></i>
        <input type="text" id="destino" placeholder="Ej: Centro Comercial Santafé" value="Centro Comercial Santafé" autocomplete="off"></div></div>
      <button class="btn-search" id="btnBuscar" onclick="consultar()"><i class="fa-solid fa-route"></i> Buscar rutas</button>
    </div>
  </div>

  <div id="busSelectorCard" class="card" style="display:none">
    <div class="bus-selector-box">
      <label for="selectBus"><i class="fa-solid fa-bus-simple"></i> Rutas oficiales que sirven tu trayecto (cambia el mapa y el paso a paso):</label>
      <div class="input-wrapper"><i class="fa-solid fa-list-check"></i>
      <select id="selectBus" onchange="render(+this.value)"></select></div>
    </div>
  </div>

  <div class="card" style="padding:10px"><div id="mapContainer"></div></div>

  <div id="alertBanner" class="alert-banner"><i class="fa-solid fa-triangle-exclamation"></i><div id="alertText"></div></div>

  <div id="resultsCard" class="card" style="display:none">
    <div class="address-badge-card">
      <div class="address-item"><b><i class="fa-solid fa-circle-dot" style="color:#0056b3"></i> Origen confirmado:</b><span id="txtDirOrigen">--</span></div>
      <div class="address-item"><b><i class="fa-solid fa-location-pin" style="color:#dc2626"></i> Destino confirmado:</b><span id="txtDirDestino">--</span></div>
    </div>
    <div class="metrics-grid" id="metrics"></div>
    <div class="timeline-title"><i class="fa-solid fa-route"></i> Paso a paso detallado:</div>
    <div id="timelineSteps"></div>
    <div class="share-box">
      <span style="font-size:13px;font-weight:700;color:#166534"><i class="fa-solid fa-share-nodes"></i> Enlace interactivo sincronizado con esta búsqueda:</span>
      <div class="share-input-wrapper">
        <input type="text" id="pageUrlInput" readonly onclick="this.select()">
        <button class="btn-share" onclick="copiarPagina()"><i class="fa-solid fa-copy"></i> Copiar enlace</button>
      </div>
      <span style="font-size:13px;font-weight:700;color:#166534"><i class="fa-solid fa-map-location-dot"></i> Comparar / abrir este trayecto en la app de Google Maps:</span>
      <div class="share-input-wrapper">
        <input type="text" id="shareUrlInput" readonly onclick="this.select()">
        <button class="btn-share" onclick="abrirLink()"><i class="fa-solid fa-arrow-up-right-from-square"></i> Abrir / Copiar</button>
      </div>
      <span class="note">Fuente: datos abiertos de TRANSMILENIO S.A. (rutas troncales, rutas zonales SITP y estaciones). Las distancias a pie son aproximadas (línea recta × 1,3) y los tiempos en bus son estimados por velocidad media, no en tiempo real. Confirma desvíos y novedades en <a href="https://www.transmilenio.gov.co/buscador_de_rutas" target="_blank" rel="noopener">el buscador oficial</a> o en la TransMi App.</span>
    </div>
  </div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
<script>
const $ = id => document.getElementById(id);
const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const TM = 'https://gis.transmilenio.gov.co/arcgis/rest/services/';
const LAYER = {
  troncal: TM + 'Troncal/consulta_rutas_troncales/MapServer/0',
  est: TM + 'Troncal/consulta_estaciones_troncales/MapServer/0',
  zonal: TM + 'Zonal/consulta_rutas_zonales/MapServer/0'
};
const F_TRONCAL = 'objectid,nombre_ruta_troncal,origen_ruta_troncal,destino_ruta_troncal,desc_tipo_ruta_troncal,desc_tipo_bus_ruta_troncal,horario_lunes_viernes,horario_sabado,horario_domingo_festivo,estado_ruta_troncal';
const F_ZONAL = 'objectid,codigo_definitivo_ruta_zonal,route_name_ruta_zonal,denominacion_ruta_zonal,origen_ruta_zonal,destino_ruta_zonal,operador_ruta_zonal,tipo_operacion';
const F_EST = 'nombre_estacion,ubicacion_estacion,troncal_estacion';
let map, layerGroup, options = [], A = null, B = null;

function actualizarReloj() {
  const a = new Date();
  $('clockTime').textContent = a.toLocaleTimeString('es-CO', {timeZone:'America/Bogota', hour:'2-digit', minute:'2-digit', second:'2-digit', hour12:true});
  $('clockDate').textContent = a.toLocaleDateString('es-CO', {timeZone:'America/Bogota', weekday:'long', year:'numeric', month:'long', day:'numeric'});
}
setInterval(actualizarReloj, 1000); actualizarReloj();

function aviso(html) { $('alertText').innerHTML = html; $('alertBanner').classList.add('active'); }

/* ---------- Acceso a los servicios oficiales (ArcGIS REST) ---------- */
function jsonp(url) {
  return new Promise((res, rej) => {
    const cb = 'cb' + Math.random().toString(36).slice(2), s = document.createElement('script');
    const t = setTimeout(() => { rej(new Error('timeout')); s.remove(); }, 25000);
    window[cb] = d => { clearTimeout(t); delete window[cb]; s.remove(); res(d); };
    s.onerror = () => { clearTimeout(t); s.remove(); rej(new Error('jsonp')); };
    s.src = url + '&callback=' + cb; document.head.appendChild(s);
  });
}
async function arc(layer, p) {
  const q = new URLSearchParams(Object.assign({f:'json', where:'1=1', inSR:4326, outSR:4326}, p));
  const url = layer + '/query?' + q;
  let d;
  try { d = await (await fetch(url)).json(); } catch (e) { d = await jsonp(url); }
  if (d.error) throw new Error((d.error.message || 'Error del servicio') + (d.error.details && d.error.details.length ? ' (' + d.error.details.join('; ') + ')' : ''));
  return d;
}
async function near(layer, pt, dist, fields, geom = true, extra = {}) {
  const dLat = dist / 110540, dLng = dist / (111320 * Math.cos(pt.lat * Math.PI / 180));
  const env = [pt.lng - dLng, pt.lat - dLat, pt.lng + dLng, pt.lat + dLat].join(',');
  const base = {geometry: env, geometryType:'esriGeometryEnvelope', spatialRel:'esriSpatialRelIntersects', outFields: fields, returnGeometry: geom};
  const lite = Object.assign({}, extra); delete lite.maxAllowableOffset; delete lite.resultRecordCount;
  const intentos = [Object.assign({}, base, extra), Object.assign({}, base, lite),
    Object.assign({}, base, lite, {geometry: pt.lng + ',' + pt.lat, geometryType:'esriGeometryPoint', distance: dist, units:'esriSRUnit_Meter'})];
  let err;
  for (const p of intentos) { try { return await arc(layer, p); } catch (e) { err = e; } }
  throw new Error(layer.split('/services/')[1] + ' → ' + err.message);
}

/* ---------- Geocodificación: estaciones oficiales primero, luego OpenStreetMap ---------- */
async function geocodificar(texto) {
  const stop = ['de','del','la','el','los','las','bogota','bogotá','estacion','estación'];
  const words = texto.toUpperCase().replace(/[%'"]/g, '').split(/\s+/).filter(w => w.length > 1 && !stop.includes(w.toLowerCase()));
  if (words.length && words.length <= 3) {
    try {
      const w = words.map(x => "UPPER(nombre_estacion) LIKE '%" + x.normalize('NFD').replace(/[\u0300-\u036f]/g, '') + "%'").join(' AND ');
      const d = await arc(LAYER.est, {where: w, outFields: F_EST, returnGeometry: true, resultRecordCount: 1});
      if (d.features && d.features.length) {
        const f = d.features[0];
        return {lat: f.geometry.y, lng: f.geometry.x, name: 'Estación ' + f.attributes.nombre_estacion + ' (' + (f.attributes.ubicacion_estacion || 'TransMilenio') + ')'};
      }
    } catch (e) {}
  }
  const u = 'https://nominatim.openstreetmap.org/search?format=jsonv2&limit=1&countrycodes=co&viewbox=-74.25,4.84,-73.99,4.45&bounded=1&accept-language=es&q=' +
    encodeURIComponent(/bogot/i.test(texto) ? texto : texto + ', Bogotá');
  const r = await (await fetch(u)).json();
  if (!r.length) throw new Error('No encontré "' + esc(texto) + '" en Bogotá. Prueba con una dirección más específica (ej: "Calle 100 con Carrera 15") o el nombre de una estación.');
  return {lat: +r[0].lat, lng: +r[0].lon, name: r[0].display_name};
}

/* ---------- Geometría ---------- */
const rad = Math.PI / 180;
function hav(a, b) {
  const dl = (b.lat - a.lat) * rad, dn = (b.lng - a.lng) * rad;
  const x = Math.sin(dl / 2) ** 2 + Math.cos(a.lat * rad) * Math.cos(b.lat * rad) * Math.sin(dn / 2) ** 2;
  return 2 * 6371000 * Math.asin(Math.sqrt(x));
}
function snap(path, p) {
  let best = {d:1e12, pos:0, i:0, pt:path[0]}, cum = 0;
  const k = Math.cos(p.lat * rad);
  for (let i = 0; i < path.length - 1; i++) {
    const a = path[i], b = path[i + 1];
    const ax = (a[0] - p.lng) * k * 111320, ay = (a[1] - p.lat) * 110540, bx = (b[0] - p.lng) * k * 111320, by = (b[1] - p.lat) * 110540;
    const dx = bx - ax, dy = by - ay, L2 = dx * dx + dy * dy, len = Math.sqrt(L2);
    const t = L2 ? Math.max(0, Math.min(1, -(ax * dx + ay * dy) / L2)) : 0;
    const d = Math.hypot(ax + t * dx, ay + t * dy);
    if (d < best.d) best = {d, pos: cum + t * len, i, pt: [a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])]};
    cum += len;
  }
  return best;
}
const cleanPaths = g => (g && g.paths || []).map(p => p.map(c => [c[0], c[1]])).filter(p => p.length > 1);
const walkMin = m => Math.max(1, Math.round(m * 1.3 / 80));
const walkM = m => Math.round(m * 1.3 / 10) * 10;
const fmtDist = m => m >= 1000 ? (m / 1000).toFixed(1).replace('.', ',') + ' km' : Math.round(m) + ' m';

/* ---------- Búsqueda de rutas directas ---------- */
async function consultar() {
  const o = $('origen').value.trim(), d = $('destino').value.trim();
  if (!o || !d) { alert('Ingresa origen y destino.'); return; }
  $('alertBanner').classList.remove('active');
  const qs = new URLSearchParams({origen: o, destino: d});
  $('pageUrlInput').value = location.href.split('?')[0].split('#')[0] + '?' + qs;
  try { history.replaceState(null, '', '?' + qs); } catch (e) {}
  $('btnBuscar').disabled = true; $('btnBuscar').innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Buscando...';
  try {
    [A, B] = await Promise.all([geocodificar(o), geocodificar(d)]);
    $('txtDirOrigen').textContent = A.name; $('txtDirDestino').textContent = B.name;
    const fallos = [];
    const safe = p => p.catch(e => { if (!fallos.includes(e.message)) fallos.push(e.message); return {features: [], objectIds: []}; });
    const [tA, eA, eB, zA, zB] = await Promise.all([
      safe(near(LAYER.troncal, A, 1300, F_TRONCAL, true, {maxAllowableOffset: 0.00002})),
      safe(near(LAYER.est, A, 1300, F_EST)),
      safe(near(LAYER.est, B, 1300, F_EST)),
      safe(near(LAYER.zonal, A, 450, F_ZONAL, true, {maxAllowableOffset: 0.00003, resultRecordCount: 1500})),
      safe(near(LAYER.zonal, B, 450, 'objectid', false, {returnIdsOnly: true}))
    ]);
    if (fallos.length >= 3) throw new Error(fallos.join(' | '));
    const est = r => (r.features || []).map(f => ({name: f.attributes.nombre_estacion, addr: f.attributes.ubicacion_estacion, troncal: f.attributes.troncal_estacion, lat: f.geometry.y, lng: f.geometry.x}));
    const stA = est(eA), stB = est(eB);
    options = [];

    (tA.features || []).forEach(f => {
      const at = f.attributes;
      if (/inactiv|suspend|cancel/i.test(at.estado_ruta_troncal || '')) return;
      let mejor = null;
      cleanPaths(f.geometry).forEach(path => {
        const bs = stA.map(s => ({s, sn: snap(path, s), dA: hav(A, s)})).filter(x => x.sn.d <= 90).sort((a, b) => a.dA - b.dA)[0];
        const as = stB.map(s => ({s, sn: snap(path, s), dB: hav(B, s)})).filter(x => x.sn.d <= 90).sort((a, b) => a.dB - b.dB)[0];
        if (!bs || !as) return;
        const ride = Math.abs(as.sn.pos - bs.sn.pos), cand = {path, bs, as, ride, score: bs.dA + as.dB + ride / 3};
        if (!mejor || cand.score < mejor.score) mejor = cand;
      });
      if (!mejor || mejor.ride < 150) return;
      const fwd = mejor.as.sn.pos > mejor.bs.sn.pos;
      options.push({kind:'tm', code: at.nombre_ruta_troncal, label:'TransMilenio troncal', tipo: at.desc_tipo_ruta_troncal, bus: at.desc_tipo_bus_ruta_troncal,
        origen: at.origen_ruta_troncal, destino: at.destino_ruta_troncal, horario: [at.horario_lunes_viernes, at.horario_sabado, at.horario_domingo_festivo],
        estado: at.estado_ruta_troncal, hacia: fwd ? at.destino_ruta_troncal : at.origen_ruta_troncal, reverso: false,
        board: mejor.bs.s, alight: mejor.as.s, bPt: [mejor.bs.s.lng, mejor.bs.s.lat], aPt: [mejor.as.s.lng, mejor.as.s.lat],
        w1: mejor.bs.dA, w2: mejor.as.dB, ride: mejor.ride, speed: 24, path: mejor.path, i1: mejor.bs.sn.i, i2: mejor.as.sn.i});
    });

    const idsB = new Set(zB.objectIds || []), vistos = {};
    (zA.features || []).filter(f => idsB.has(f.attributes.objectid)).forEach(f => {
      const at = f.attributes; let mejor = null;
      cleanPaths(f.geometry).forEach(path => {
        const sa = snap(path, A), sb = snap(path, B), cand = {path, sa, sb, score: sa.d + sb.d};
        if (!mejor || cand.score < mejor.score) mejor = cand;
      });
      if (!mejor || mejor.sa.d > 450 || mejor.sb.d > 450) return;
      const ride = Math.abs(mejor.sb.pos - mejor.sa.pos); if (ride < 150) return;
      const fwd = mejor.sb.pos > mejor.sa.pos, tipo = at.tipo_operacion || '';
      const kind = /aliment/i.test(tipo) ? 'feed' : 'sitp';
      const o = {kind, code: at.codigo_definitivo_ruta_zonal || at.route_name_ruta_zonal, label: /aliment/i.test(tipo) ? 'Alimentador TransMilenio' : (/complement/i.test(tipo) ? 'SITP complementario' : 'SITP zonal / urbano'),
        tipo, nombre: at.denominacion_ruta_zonal, origen: at.origen_ruta_zonal, destino: at.destino_ruta_zonal, operador: at.operador_ruta_zonal,
        hacia: at.destino_ruta_zonal, reverso: !fwd, board: null, alight: null, bPt: mejor.sa.pt, aPt: mejor.sb.pt,
        w1: mejor.sa.d, w2: mejor.sb.d, ride, speed: 14, path: mejor.path, i1: mejor.sa.i, i2: mejor.sb.i};
      const key = o.code + '|' + o.origen + '|' + o.destino;
      if (!vistos[key] || (vistos[key].w1 + vistos[key].w2) > (o.w1 + o.w2)) vistos[key] = o;
    });
    Object.values(vistos).forEach(o => options.push(o));

    options.forEach(o => { o.tw = walkMin(o.w1) + walkMin(o.w2); o.tb = Math.max(1, Math.round(o.ride / 1000 / o.speed * 60)); o.total = o.tw + o.tb + (o.reverso ? 15 : 0); });
    options.sort((a, b) => a.total - b.total);
    options = options.slice(0, 10);

    initMapa();
    if (!options.length) {
      $('busSelectorCard').style.display = 'none'; $('resultsCard').style.display = 'none';
      dibujarBase(); mostrarLinkGoogle();
      aviso('<b>No encontré rutas directas oficiales</b> entre estos dos puntos (sin transbordo, con paraderos a menos de ~450 m o estaciones a menos de ~1,3 km). El trayecto probablemente requiere transbordo: usa el enlace de Google Maps abajo o el buscador oficial.' + (fallos.length ? '<br><small>Consultas con error: ' + esc(fallos.join(' | ')) + '</small>' : ''));
      $('resultsCard').style.display = 'block'; $('metrics').innerHTML = ''; $('timelineSteps').innerHTML = '';
      return;
    }
    const sel = $('selectBus'); sel.innerHTML = '';
    options.forEach((o, i) => {
      const op = document.createElement('option'); op.value = i;
      op.textContent = 'Opción ' + (i + 1) + ': ' + o.code + ' (' + o.label + ') · ~' + o.total + ' min · caminata ' + fmtDist(walkM(o.w1 + o.w2)) + (o.reverso ? ' · sentido a verificar' : '');
      sel.appendChild(op);
    });
    $('busSelectorCard').style.display = 'block';
    render(0);
    if (fallos.length) { $('alertText').innerHTML += '<br><small>Algunas consultas oficiales fallaron, así que faltan datos: ' + esc(fallos.join(' | ')) + '</small>'; $('alertBanner').classList.add('active'); }
  } catch (e) {
    aviso('<b>No pude completar la búsqueda:</b> ' + e.message + ' Si el error menciona conexión, puede ser que el servidor de TransMilenio no esté disponible en este momento; intenta de nuevo en unos minutos.');
  } finally {
    $('btnBuscar').disabled = false; $('btnBuscar').innerHTML = '<i class="fa-solid fa-route"></i> Buscar rutas';
  }
}

/* ---------- Mapa ---------- */
function initMapa() {
  if (map) return;
  map = L.map('mapContainer').setView([4.65, -74.1], 12);
  L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {subdomains: 'abcd', maxZoom: 19, attribution: '© OpenStreetMap contributors © CARTO'}).addTo(map);
  layerGroup = L.layerGroup().addTo(map);
}
function dibujarBase() {
  layerGroup.clearLayers();
  L.marker([A.lat, A.lng]).addTo(layerGroup).bindPopup('<b>Origen</b><br>' + esc(A.name));
  L.marker([B.lat, B.lng]).addTo(layerGroup).bindPopup('<b>Destino</b><br>' + esc(B.name));
  map.fitBounds([[A.lat, A.lng], [B.lat, B.lng]], {padding: [40, 40]});
}
const COLOR = {tm:'#dc2626', sitp:'#0284c7', feed:'#16a34a'};

/* ---------- Resultado y paso a paso ---------- */
function render(i) {
  const o = options[i]; dibujarBase();
  const lo = Math.min(o.i1, o.i2), hi = Math.max(o.i1, o.i2);
  const tramo = [o.bPt, ...o.path.slice(lo + 1, hi + 1), o.aPt].map(c => [c[1], c[0]]);
  L.polyline(o.path.map(c => [c[1], c[0]]), {color: COLOR[o.kind], weight: 3, opacity: .25}).addTo(layerGroup);
  L.polyline(tramo, {color: COLOR[o.kind], weight: 6}).addTo(layerGroup).bindPopup(esc(o.code));
  L.polyline([[A.lat, A.lng], [o.bPt[1], o.bPt[0]]], {color:'#334155', dashArray:'6 8', weight: 3}).addTo(layerGroup);
  L.polyline([[o.aPt[1], o.aPt[0]], [B.lat, B.lng]], {color:'#334155', dashArray:'6 8', weight: 3}).addTo(layerGroup);
  map.fitBounds(L.latLngBounds(tramo.concat([[A.lat, A.lng], [B.lat, B.lng]])), {padding: [40, 40]});

  const m = (ic, lb, v) => `<div class="metric-card"><div class="metric-icon"><i class="fa-solid ${ic}"></i></div><div class="metric-info"><label>${lb}</label><span>${v}</span></div></div>`;
  const hora = +new Date().toLocaleString('en-US', {timeZone:'America/Bogota', hour:'numeric', hour12:false}) % 24;
  const pico = (hora >= 6 && hora <= 9) || (hora >= 17 && hora <= 20);
  $('metrics').innerHTML = m('fa-clock', 'Tiempo total (estimado)', '~' + o.total + ' min') + m('fa-person-walking', 'Caminata total (aprox.)', fmtDist(walkM(o.w1 + o.w2)) + ' · ~' + o.tw + ' min') +
    m('fa-bus', 'En bus (estimado)', '~' + o.tb + ' min') + m('fa-road', 'Recorrido en bus', fmtDist(o.ride)) + m('fa-shuffle', 'Transbordos', '0 (ruta directa)') +
    m('fa-traffic-light', 'Estado tráfico', pico ? 'Hora pico (estimado)' : 'Fluido (estimado)');
  if (pico) aviso('<b>Hora pico en Bogotá:</b> espera más demora y buses/estaciones llenos; los tiempos mostrados no incluyen tráfico real.');
  else if (!o.reverso) $('alertBanner').classList.remove('active');
  if (o.reverso) aviso('<b>Verifica el sentido:</b> en esta ruta el trazado oficial va en dirección contraria a tu viaje. Confirma en el paradero que el bus vaya hacia <b>' + esc(B.name.split(',')[0]) + '</b>, o prueba otra opción.');

  const abordar = o.board ? `la estación <b>${esc(o.board.name)}</b>${o.board.addr ? ' (' + esc(o.board.addr) + ')' : ''}` : 'el paradero SITP más cercano sobre el trazado de la ruta (punto del recorrido a ~' + fmtDist(o.w1) + ' en línea recta)';
  const bajar = o.alight ? `la estación <b>${esc(o.alight.name)}</b>${o.alight.addr ? ' (' + esc(o.alight.addr) + ')' : ''}` : 'el paradero SITP del trazado más cercano a tu destino';
  const h = o.horario ? `<span class="pill">L-V ${esc(o.horario[0] || '—')}</span><span class="pill">Sáb ${esc(o.horario[1] || '—')}</span><span class="pill">Dom/fest ${esc(o.horario[2] || '—')}</span>` : '';
  $('timelineSteps').innerHTML = `
  <div class="step-card"><div class="step-icon-box icon-walk"><i class="fa-solid fa-person-walking"></i></div><div class="step-content">
    <div class="step-title-line">Paso 1: Caminar ~${fmtDist(walkM(o.w1))} <span class="pill">~${walkMin(o.w1)} min</span></div>
    <div class="step-details">Desde <b>${esc(A.name.split(',')[0])}</b> hasta ${abordar}.</div></div></div>
  <div class="step-card"><div class="step-icon-box icon-${o.kind}"><i class="fa-solid fa-bus"></i></div><div class="step-content">
    <div class="step-title-line">Paso 2: Abordar <span class="badge-bus badge-${o.kind}"><i class="fa-solid fa-bus"></i> ${esc(o.code)}</span> <span class="pill">${esc(o.label)}</span></div>
    <div class="step-details">
      ${o.nombre ? esc(o.nombre) + '<br>' : ''}Servicio <b>${esc(o.origen)}</b> ⇄ <b>${esc(o.destino)}</b>${o.hacia ? ' · sentido hacia <b>' + esc(o.hacia) + '</b>' : ''}<br>
      <b>Subir en:</b> ${abordar}<br><b>Bajar en:</b> ${bajar}<br>
      <span class="pill">${fmtDist(o.ride)} en bus</span><span class="pill">~${o.tb} min (estimado)</span>
      ${o.tipo ? '<span class="pill">' + esc(o.tipo) + '</span>' : ''}${o.bus ? '<span class="pill">' + esc(o.bus) + '</span>' : ''}${o.operador ? '<span class="pill">' + esc(o.operador) + '</span>' : ''}${h}
    </div></div></div>
  <div class="step-card"><div class="step-icon-box icon-walk"><i class="fa-solid fa-flag-checkered"></i></div><div class="step-content">
    <div class="step-title-line">Paso 3: Caminar ~${fmtDist(walkM(o.w2))} hasta tu destino <span class="pill">~${walkMin(o.w2)} min</span></div>
    <div class="step-details">Desde ${bajar} hasta <b>${esc(B.name.split(',')[0])}</b>.</div></div></div>`;
  mostrarLinkGoogle(); $('resultsCard').style.display = 'block';
}
function mostrarLinkGoogle() {
  $('shareUrlInput').value = 'https://www.google.com/maps/dir/?api=1&origin=' + A.lat + ',' + A.lng + '&destination=' + B.lat + ',' + B.lng + '&travelmode=transit';
}
function abrirLink() {
  const url = $('shareUrlInput').value;
  navigator.clipboard.writeText(url).then(() => { alert('¡Enlace copiado! También se abrirá en una nueva pestaña.'); window.open(url, '_blank'); }).catch(() => window.open(url, '_blank'));
}
function copiarPagina() {
  const url = $('pageUrlInput').value;
  navigator.clipboard.writeText(url).then(() => alert('¡Enlace copiado!')).catch(() => $('pageUrlInput').select());
}
window.addEventListener('load', () => {
  const p = new URLSearchParams(location.search);
  if (p.get('origen')) $('origen').value = p.get('origen');
  if (p.get('destino')) $('destino').value = p.get('destino');
  ['origen', 'destino'].forEach(id => $(id).addEventListener('keydown', e => { if (e.key === 'Enter') consultar(); }));
  initMapa(); setTimeout(consultar, 300);
});
</script>
</body>
</html>"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(codigo_html)

files.download("index.html")
print("¡index.html con datos oficiales de TransMilenio generado y descargado correctamente!")
