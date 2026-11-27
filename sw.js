/* Офлайн-кэш «Просмотр DXF и PDF».
   ВАЖНО: VERSION = APP_VERSION на странице (берутся из шапки при сборке, меняются вместе). По изменению VERSION
   телефон и компьютер узнают о новой версии: она скачивается целиком и ЖДЁТ, пока пользователь нажмёт «Обновить».
   Удаляются только свои старые кэши (dxfv-*): на домене mrtekhnik.github.io живут и другие приложения.
   Библиотека PDF (lib/) — в отдельном кэше, не сбрасывается при обновлении приложения. */
const VERSION='4.7.4';
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
