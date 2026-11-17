# Обновление по стандарту: новая версия ждёт «Обновить», после нажатия — загружается; офлайн работает;
# страница — из своего кэша (не из сети); чужой кэш (razmery-1.0) на месте; свои старые кэши удалены
import asyncio, subprocess, shutil, os, re
from playwright.async_api import async_playwright
SRC='/home/claude/pwa'; TMP='/tmp/claude-0/srv_upd'; PORT='8767'
def bump(v):
  d=TMP+'/dxf-viewer'
  sw=open(d+'/sw.js',encoding='utf-8').read(); sw=re.sub(r"const VERSION='[^']+'","const VERSION='%s'"%v,sw,count=1); open(d+'/sw.js','w',encoding='utf-8').write(sw)
  ix=open(d+'/index.html',encoding='utf-8').read(); ix=re.sub(r"const APP_VERSION='[^']+'","const APP_VERSION='%s'"%v,ix,count=1); open(d+'/index.html','w',encoding='utf-8').write(ix)
async def main():
  shutil.rmtree(TMP,ignore_errors=True); os.makedirs(TMP); shutil.copytree(SRC,TMP+'/dxf-viewer')
  srv=subprocess.Popen(['python3','-m','http.server',PORT],cwd=TMP,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); await asyncio.sleep(1)
  errs=[]
  try:
    async with async_playwright() as p:
      b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); ctx=await b.new_context(); pg=await ctx.new_page(); pg.on('pageerror',lambda e:errs.append(str(e)))
      url='http://localhost:%s/dxf-viewer/'%PORT
      await pg.goto(url); await pg.evaluate("navigator.serviceWorker.ready"); await pg.wait_for_timeout(1200)
      v0=await pg.evaluate('APP_VERSION'); print('v0',v0,'ctrl',await pg.evaluate('!!navigator.serviceWorker.controller'))
      await pg.reload(); await pg.wait_for_timeout(800); print('controlled after reload',await pg.evaluate('!!navigator.serviceWorker.controller'))
      await pg.evaluate("""(async()=>{for(const n of ['razmery-1.0','apps-3','dxfv-app-0.0.1'])(await caches.open(n)).put('/x-'+n,new Response('x'));})()""")
      # выпуск новой версии на «сервере»
      bump('9.9.9')
      await pg.evaluate("swReg.update()"); await pg.wait_for_timeout(2500)
      print('update bar',await pg.is_visible('#updBar'),'page still',await pg.evaluate('APP_VERSION'))
      if not await pg.is_visible('#updBar'): errs.append('нет панели «Обновить»')
      # страница берётся из кэша: перезагрузка без нажатия — всё ещё старая версия
      await pg.reload(); await pg.wait_for_timeout(1500); vv=await pg.evaluate('APP_VERSION'); print('reload w/o button ->',vv,'bar',await pg.is_visible('#updBar'))
      if vv!=v0: errs.append('новая версия поставилась сама: '+vv)
      if not await pg.is_visible('#updBar'): errs.append('после перезапуска нет панели «Обновить» (reg.waiting)')
      async with pg.expect_navigation(): await pg.click('#updBtn')
      await pg.wait_for_timeout(1500); v1=await pg.evaluate('APP_VERSION'); print('after Обновить ->',v1,await pg.inner_text('#verSet'))
      if v1!='9.9.9': errs.append('после «Обновить» версия '+v1)
      keys=sorted(await pg.evaluate('caches.keys()')); print('caches',keys)
      for n in ['razmery-1.0','apps-3']:
        if n not in keys: errs.append('чужой кэш удалён: '+n)
      if 'dxfv-app-0.0.1' in keys or 'dxfv-app-'+v0 in keys: errs.append('свои старые кэши не удалены')
      if 'dxfv-app-9.9.9' not in keys or 'dxfv-lib-3.11.174' not in keys: errs.append('нет своих кэшей')
      # «Проверить обновления»: новой нет
      await pg.evaluate("checkUpdate()"); await pg.wait_for_timeout(2200); st=await pg.inner_text('#status'); print('check:',st)
      if 'последняя версия' not in st: errs.append('проверка обновлений: '+st)
      # офлайн
      srv.terminate(); await ctx.set_offline(True); await pg.reload(); await pg.wait_for_timeout(1500)
      vo=await pg.evaluate('APP_VERSION')
      await pg.set_input_files('#inFiles',['blk/many.pdf','xf2/A/DXF/АЮИА.100-01.01-St-3-K1.dxf']); await pg.wait_for_timeout(2500)
      pdfjs=await pg.evaluate("items.every(i=>i.state===2&&!i.err)&&items.length===2"); print('offline ->',vo,'PDF и DXF открыты',pdfjs, await pg.evaluate("items.map(i=>[i.name,i.state,i.err])"))
      if vo!='9.9.9' or not pdfjs: errs.append('офлайн не работает')
      await b.close()
  finally: srv.terminate()
  print('errors',errs)
asyncio.run(main())
