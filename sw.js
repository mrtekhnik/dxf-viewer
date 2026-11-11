/* Офлайн-кэш «Просмотр DXF». Версия меняется автоматически при каждом изменении index.html. */
const VER='f82794455c';
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
