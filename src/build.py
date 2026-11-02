#!/usr/bin/env python3
"""Сборка просмотрщика DXF/PDF из исходников в src/.

    python src/build.py

Склеивает head.part + core.part + main.part, подставляет pdf.js и пишет:
    src/dist/dxf-viewer.html      — один файл, pdf.js внутри, работает офлайн без установки
    src/dist/pwa/                 — приложение для GitHub Pages (index.html, sw.js, manifest, иконки, lib/)
    src/dist/dxf-viewer.src.html  — склеенный исходник без pdf.js (для проверки)

Логика сборки та же, что в build_original.py (сборка во временной папке сессии); изменены только пути
(теперь относительно src/), добавлена склейка трёх частей (раньше — отдельная команда cat)
и явная кодировка UTF-8 с переводами строк \\n (чтобы на Windows результат был побайтно тем же).
"""
import hashlib, shutil, os, json

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.join(HERE, 'vendor', 'pdfjs-3.11.174') + os.sep
DIST = os.path.join(HERE, 'dist')
OUT = os.path.join(DIST, 'pwa') + os.sep
os.makedirs(OUT + 'lib', exist_ok=True)

def rd(p): return open(p, encoding='utf-8', newline='').read()
def wr(p, t): open(p, 'w', encoding='utf-8', newline='').write(t)

# 0) склейка трёх частей
s = ''.join(rd(os.path.join(HERE, p)) for p in ('head.part', 'core.part', 'main.part'))
wr(os.path.join(DIST, 'dxf-viewer.src.html'), s)

lic = '/* pdf.js 3.11.174 (c) Mozilla Foundation, Apache License 2.0 */\n'
# 1) один файл (офлайн, без установки)
one = s.replace('<!--@@PWAHEAD@@-->', '').replace('/*@@PDFJS@@*/', lic + rd(LIB + 'pdf.min.js'), 1).replace('/*@@PDFWORKER@@*/', rd(LIB + 'pdf.worker.min.js'), 1)
wr(os.path.join(DIST, 'dxf-viewer.html'), one)
# 2) PWA для GitHub Pages
head = '''<link rel="manifest" href="manifest.webmanifest">
<meta name="theme-color" content="#24272c">
<link rel="icon" href="icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="icon-192.png">'''
idx = s.replace('<!--@@PWAHEAD@@-->', head).replace('/*@@PDFJS@@*/', '').replace('/*@@PDFWORKER@@*/', '')
wr(OUT + 'index.html', idx)
for f in ('pdf.min.js', 'pdf.worker.min.js'): shutil.copy(LIB + f, OUT + 'lib/' + f)
for f in ('icon.svg', 'icon-192.png', 'icon-512.png'): shutil.copy(os.path.join(HERE, 'assets', f), OUT + f)
man = {"name": "Просмотр DXF и PDF", "short_name": "DXF просмотр", "start_url": "./", "scope": "./", "display": "standalone",
 "background_color": "#1b1d21", "theme_color": "#24272c", "lang": "ru",
 "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any maskable"},
          {"src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"},
          {"src": "icon.svg", "sizes": "any", "type": "image/svg+xml"}],
 "file_handlers": [{"action": "./", "accept": {"application/dxf": [".dxf"], "application/pdf": [".pdf"]}}],
 "launch_handler": {"client_mode": "focus-existing"}}
wr(OUT + 'manifest.webmanifest', json.dumps(man, ensure_ascii=False, indent=1))
h = hashlib.sha1(idx.encode()).hexdigest()[:10]
sw = '''/* Офлайн-кэш «Просмотр DXF». Версия меняется автоматически при каждом изменении index.html. */
const VER='%s';
const CORE=['./','index.html','manifest.webmanifest','icon.svg','icon-192.png','icon-512.png'];
const LIBS=['lib/pdf.min.js','lib/pdf.worker.min.js'];
const C_APP='dxfv-app-'+VER, C_LIB='dxfv-lib-3.11.174';
self.addEventListener('install',e=>{e.waitUntil((async()=>{
  const a=await caches.open(C_APP);await a.addAll(CORE.map(u=>new Request(u,{cache:'reload'})));
  const l=await caches.open(C_LIB);for(const u of LIBS)if(!(await l.match(u)))await l.add(u);
})());});
self.addEventListener('activate',e=>{e.waitUntil((async()=>{
  for(const k of await caches.keys())if(k!==C_APP&&k!==C_LIB)await caches.delete(k);
  await self.clients.claim();
})());});
self.addEventListener('message',e=>{if(e.data==='skip')self.skipWaiting();});
self.addEventListener('fetch',e=>{
  const r=e.request;if(r.method!=='GET')return;
  const u=new URL(r.url);if(u.origin!==location.origin)return;
  if(u.pathname.includes('/lib/')){ // библиотека PDF: из кэша, не меняется
    e.respondWith(caches.match(r).then(c=>c||fetch(r).then(n=>{const cp=n.clone();caches.open(C_LIB).then(x=>x.put(r,cp));return n;})));return;}
  if(r.mode==='navigate'||u.pathname.endsWith('/')||u.pathname.endsWith('index.html')){ // страница: сначала сеть (свежая версия), без сети — кэш
    e.respondWith((async()=>{
      try{const ctl=new AbortController();const t=setTimeout(()=>ctl.abort(),4000);
        const n=await fetch(r,{cache:'no-cache',signal:ctl.signal});clearTimeout(t);
        if(n.ok){const cp=n.clone();caches.open(C_APP).then(x=>x.put('index.html',cp));}return n;}
      catch(err){return (await caches.match('index.html'))||(await caches.match('./'))||Response.error();}
    })());return;}
  e.respondWith(caches.match(r).then(c=>c||fetch(r)));
});
''' % h
wr(OUT + 'sw.js', sw)
print('one-file', len(one.encode()) // 1024, 'KB | index.html', len(idx.encode()) // 1024, 'KB | sw', h)
