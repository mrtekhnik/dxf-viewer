import asyncio, base64, os, sys, subprocess
from playwright.async_api import async_playwright
def collect(root):
  out=[]
  for d,_,fs in os.walk(root):
    for f in fs: p=os.path.join(d,f); out.append([os.path.relpath(p,root),base64.b64encode(open(p,'rb').read()).decode()])
  return out
JS_PUT="""async([nm,files])=>{const r=await navigator.storage.getDirectory();try{await r.removeEntry(nm,{recursive:true})}catch(e){}
 const root=await r.getDirectoryHandle(nm,{create:true});
 for(const [rel,b64] of files){const parts=rel.split('/');let d=root;for(const q of parts.slice(0,-1))d=await d.getDirectoryHandle(q,{create:true});
  const h=await d.getFileHandle(parts.at(-1),{create:true});const w=await h.createWritable();await w.write(Uint8Array.from(atob(b64),c=>c.charCodeAt(0)));await w.close();}
 return true;}"""
async def setup(pg,A='cmp3/A',B='cmp3/B',layout='grid'):
  await pg.add_init_script("localStorage.setItem('dxfv.set',JSON.stringify({click:'1',layout:'%s'}))"%layout)
  await pg.goto('http://localhost:8765/dxf-viewer/'); await pg.wait_for_timeout(800)
  await pg.evaluate(JS_PUT,['A',collect(A)]); await pg.evaluate(JS_PUT,['B',collect(B)])
  await pg.evaluate("(async()=>{const r=await navigator.storage.getDirectory();window.__A=await r.getDirectoryHandle('A');window.__B=await r.getDirectoryHandle('B');await openDirHandle(window.__A);})()")
  await pg.wait_for_timeout(1500)
async def cmp(pg):
  # OPFS-дескрипторы из IndexedDB в headless Chrome роняют браузер — путь подставляем (в жизни папки из окна выбора)
  await pg.evaluate("window.knownPath=async h=>h===window.__B?'Сервер / Архив 2024 / Заказ 1187 / B':'Сервер / Заказы / Текущий / A';window.curDirHandle=async()=>window.__A;window.rememberRoot=async()=>null;")
  await pg.evaluate("cmpFromHandle(window.__B)"); await pg.wait_for_timeout(2500)
