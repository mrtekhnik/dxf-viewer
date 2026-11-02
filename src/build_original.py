import hashlib, shutil, os, json
SRC='/home/claude/dxf-viewer.src.html'; LIB='/tmp/claude-0/pj/package/build/'; OUT='/home/claude/pwa/'
s=open(SRC).read()
lic='/* pdf.js 3.11.174 (c) Mozilla Foundation, Apache License 2.0 */\n'
# 1) один файл (офлайн, без установки)
one=s.replace('<!--@@PWAHEAD@@-->','').replace('/*@@PDFJS@@*/',lic+open(LIB+'pdf.min.js').read(),1).replace('/*@@PDFWORKER@@*/',open(LIB+'pdf.worker.min.js').read(),1)
open('/home/claude/dxf-viewer.html','w').write(one)
# 2) PWA для GitHub Pages
head='''<link rel="manifest" href="manifest.webmanifest">
<meta name="theme-color" content="#24272c">
<link rel="icon" href="icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="icon-192.png">'''
idx=s.replace('<!--@@PWAHEAD@@-->',head).replace('/*@@PDFJS@@*/','').replace('/*@@PDFWORKER@@*/','')
open(OUT+'index.html','w').write(idx)
for f in ('pdf.min.js','pdf.worker.min.js'): shutil.copy(LIB+f, OUT+'lib/'+f)
man={"name":"Просмотр DXF и PDF","short_name":"DXF просмотр","start_url":"./","scope":"./","display":"standalone",
 "background_color":"#1b1d21","theme_color":"#24272c","lang":"ru",
 "icons":[{"src":"icon-192.png","sizes":"192x192","type":"image/png","purpose":"any maskable"},
          {"src":"icon-512.png","sizes":"512x512","type":"image/png","purpose":"any maskable"},
          {"src":"icon.svg","sizes":"any","type":"image/svg+xml"}],
 "file_handlers":[{"action":"./","accept":{"application/dxf":[".dxf"],"application/pdf":[".pdf"]}}],
 "launch_handler":{"client_mode":"focus-existing"}}
open(OUT+'manifest.webmanifest','w').write(json.dumps(man,ensure_ascii=False,indent=1))
h=hashlib.sha1(idx.encode()).hexdigest()[:10]
sw='''/* Офлайн-кэш «Просмотр DXF». Версия меняется автоматически при каждом изменении index.html. */
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
open(OUT+'sw.js','w').write(sw)
print('one-file',len(one.encode())//1024,'KB | index.html',len(idx.encode())//1024,'KB | sw',h)
