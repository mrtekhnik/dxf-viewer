#!/usr/bin/env python3
"""Сборка просмотрщика DXF/PDF из исходников в src/.

    python src/build.py

Склеивает head.part + help.part + core.part + geom.part + main.part, подставляет pdf.js и пишет:
    src/dist/dxf-viewer.html      — один файл, pdf.js внутри, работает офлайн без установки
    src/dist/pwa/                 — приложение для GitHub Pages (index.html, sw.js, manifest, иконки, lib/)
    src/dist/dxf-viewer.src.html  — склеенный исходник без pdf.js (для проверки)

Логика сборки та же, что в build_original.py (сборка во временной папке сессии); изменены только пути
(теперь относительно src/), добавлена склейка трёх частей (раньше — отдельная команда cat)
и явная кодировка UTF-8 с переводами строк \\n (чтобы на Windows результат был побайтно тем же).
"""
import hashlib, shutil, os, json, re, sys, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.join(HERE, 'vendor', 'pdfjs-3.11.174') + os.sep
DIST = os.path.join(HERE, 'dist')
OUT = os.path.join(DIST, 'pwa') + os.sep
os.makedirs(OUT + 'lib', exist_ok=True)

def rd(p): return open(p, encoding='utf-8', newline='').read()
def wr(p, t): open(p, 'w', encoding='utf-8', newline='').write(t)

# 0) склейка трёх частей
s = ''.join(rd(os.path.join(HERE, p)) for p in ('head.part', 'help.part', 'core.part', 'geom.part', 'xform.part', 'main.part'))
# версия: одна на всё — в шапке (head.part, «+PDF · vX.Y.Z»), APP_VERSION на странице и VERSION в sw.js.
# Дата выпуска — в versions.json (ставится при первой сборке этой версии и больше не меняется).
APP_VERSION = re.search(r'\+PDF · v([0-9][0-9.]*)<', s).group(1)
VJ = os.path.join(HERE, 'versions.json')
vers = json.load(open(VJ, encoding='utf-8')) if os.path.exists(VJ) else {}
kiev = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=2)))
APP_DATE = (vers.get(APP_VERSION) or {}).get('date') or kiev.strftime('%d.%m.%Y')
s = s.replace('@@APPVER@@', APP_VERSION).replace('@@APPDATE@@', APP_DATE)
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
# страж версии: та же версия, но другое содержимое — значит, забыли увеличить версию (телефон не узнает об обновлении)
rec = vers.get(APP_VERSION)
if '--release' in sys.argv:
    if rec and rec.get('hash') != h:
        sys.exit('ОШИБКА: версия %s уже выпускалась с другим содержимым — увеличьте версию в head.part' % APP_VERSION)
    vers[APP_VERSION] = {'date': APP_DATE, 'hash': h}
    open(VJ, 'w', encoding='utf-8', newline='').write(json.dumps(vers, ensure_ascii=False, indent=1))
elif rec and rec.get('hash') != h:
    print('ВНИМАНИЕ: содержимое изменилось, а версия %s та же — перед публикацией увеличьте версию' % APP_VERSION)
sw = '''/* Офлайн-кэш «Просмотр DXF и PDF».
   ВАЖНО: VERSION = APP_VERSION на странице (берутся из шапки при сборке, меняются вместе). По изменению VERSION
   телефон и компьютер узнают о новой версии: она скачивается целиком и ЖДЁТ, пока пользователь нажмёт «Обновить».
   Удаляются только свои старые кэши (dxfv-*): на домене mrtekhnik.github.io живут и другие приложения.
   Библиотека PDF (lib/) — в отдельном кэше, не сбрасывается при обновлении приложения. */
const VERSION='%s';
const CORE=['./','index.html','manifest.webmanifest','icon.svg','icon-192.png','icon-512.png'];
const LIBS=['lib/pdf.min.js','lib/pdf.worker.min.js'];
const C_APP='dxfv-app-'+VERSION, C_LIB='dxfv-lib-3.11.174';
const OFFLINE_PAGE='<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Просмотр DXF и PDF</title>'
 +'<body style="margin:0;font-family:sans-serif;background:#1b1d21;color:#e9eef5;display:flex;align-items:center;justify-content:center;height:100vh;text-align:center">'
 +'<div style="padding:24px"><h2>Нет сети</h2><p>Сохранённая копия приложения не найдена.<br>Подключитесь к интернету и нажмите «Повторить».</p>'
 +'<button onclick="location.reload()" style="font-size:18px;padding:12px 24px;border:0;border-radius:10px;background:#3b82f6;color:#fff">Повторить</button></div>';
self.addEventListener('install',e=>{   // без skipWaiting: новая версия ждёт кнопку «Обновить»
  e.waitUntil((async()=>{
    const a=await caches.open(C_APP);await a.addAll(CORE.map(u=>new Request(u,{cache:'reload'})));
    const l=await caches.open(C_LIB);for(const u of LIBS)if(!(await l.match(u))){try{await l.add(new Request(u,{cache:'reload'}));}catch(_){}}
  })());
});
self.addEventListener('message',e=>{if(e.data==='SKIP_WAITING'||e.data==='skip')self.skipWaiting();});
self.addEventListener('activate',e=>{e.waitUntil((async()=>{
  for(const k of await caches.keys())if(k.startsWith('dxfv-')&&k!==C_APP&&k!==C_LIB)await caches.delete(k);   // только свои старые кэши
  await self.clients.claim();
})());});
self.addEventListener('fetch',e=>{   // сначала свой кэш (страница — index.html из кэша этой версии), иначе сеть
  const r=e.request;if(r.method!=='GET')return;
  const u=new URL(r.url);if(u.origin!==location.origin)return;
  const isLib=u.pathname.includes('/lib/'),nav=r.mode==='navigate';
  e.respondWith((async()=>{
    try{
      const c=await caches.open(isLib?C_LIB:C_APP);
      let hit=await c.match(nav?'./index.html':r,{ignoreSearch:true});
      if(!hit&&!isLib)hit=await caches.match(nav?new URL('./index.html',self.registration.scope).href:r,{ignoreSearch:true});   // запас: копия прошлой версии
      if(hit)return hit;
      const n=await fetch(r);if(isLib&&n.ok)c.put(r,n.clone());return n;
    }catch(_){
      if(!nav)return new Response('',{status:503});
      return new Response(OFFLINE_PAGE,{status:503,headers:{'Content-Type':'text/html; charset=utf-8'}});
    }
  })());
});
''' % APP_VERSION
wr(OUT + 'sw.js', sw)
print('one-file', len(one.encode()) // 1024, 'KB | index.html', len(idx.encode()) // 1024, 'KB | версия', APP_VERSION, 'от', APP_DATE, '| hash', h)
