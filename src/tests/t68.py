# sw.js: при активации новой версии удаляются только свои старые кэши (dxfv-*), чужие кэши домена остаются
import asyncio, subprocess, shutil, os
from playwright.async_api import async_playwright
SRC='/home/claude/pwa'; TMP='/tmp/claude-0/srv_sw'
async def main():
  shutil.rmtree(TMP,ignore_errors=True); os.makedirs(TMP); shutil.copytree(SRC,TMP+'/dxf-viewer')
  srv=subprocess.Popen(['python3','-m','http.server','8766'],cwd=TMP,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); await asyncio.sleep(1)
  errs=[]
  try:
    async with async_playwright() as p:
      b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); ctx=await b.new_context(); pg=await ctx.new_page()
      await pg.goto('http://localhost:8766/dxf-viewer/'); 
      await pg.evaluate("navigator.serviceWorker.ready"); await pg.wait_for_timeout(1500)
      k1=await pg.evaluate("caches.keys()")
      # чужие кэши и свой старый
      await pg.evaluate("""(async()=>{for(const n of ['razmery-1.0','shablony-2','apps-3','dxfv-app-old0000'])(await caches.open(n)).put('/x-'+n,new Response('x'));})()""")
      # новая версия sw
      sw=open(TMP+'/dxf-viewer/sw.js',encoding='utf-8').read(); import re
      sw=re.sub(r"const VER='([^']+)'",lambda m:"const VER='"+m.group(1)+"x'",sw,count=1); open(TMP+'/dxf-viewer/sw.js','w',encoding='utf-8').write(sw)
      await pg.evaluate("""(async()=>{const r=await navigator.serviceWorker.getRegistration();await r.update();
        const w=r.installing||r.waiting;if(w){await new Promise(ok=>{const f=()=>{if(w.state==='installed'){w.postMessage('skip');}if(w.state==='activated')ok();};w.addEventListener('statechange',f);f();});}})()""")
      await pg.wait_for_timeout(1500)
      k2=await pg.evaluate("caches.keys()"); act=await pg.evaluate("navigator.serviceWorker.controller&&navigator.serviceWorker.controller.scriptURL")
      print('before',sorted(k1)); print('after ',sorted(k2))
      for n in ['razmery-1.0','shablony-2','apps-3']:
        if n not in k2: errs.append('чужой кэш удалён: '+n)
        elif not await pg.evaluate(f"(async()=>!!(await (await caches.open('{n}')).match('/x-{n}')))()"): errs.append('чужой кэш пуст: '+n)
      if 'dxfv-app-old0000' in k2: errs.append('свой старый кэш не удалён')
      new=[k for k in k2 if k.startswith('dxfv-app-')]
      if len(new)!=1 or not new[0].endswith('x'): errs.append('нет нового кэша приложения: '+str(new))
      if 'dxfv-lib-3.11.174' not in k2: errs.append('нет кэша библиотеки')
      await b.close()
  finally: srv.terminate()
  print('errors',errs)
asyncio.run(main())
