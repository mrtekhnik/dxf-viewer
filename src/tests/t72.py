# Ctrl+клик: выделенный файл + второй, одинаковые рамки; с PDF — «Открыть рядом», без сравнения
import asyncio,sys,subprocess
sys.path.insert(0,'/tmp/claude-0/t'); from cmpx import *
async def main():
  srv=subprocess.Popen('cd /tmp/claude-0/srv && python3 -m http.server 8765',shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); await asyncio.sleep(1)
  errs=[]
  try:
    async with async_playwright() as p:
      b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1400,'height':700}); pg.on('pageerror',lambda e:errs.append(str(e)))
      await pg.add_init_script("localStorage.setItem('dxfv.set',JSON.stringify({}))")
      await pg.goto('http://localhost:8765/dxf-viewer/'); await pg.wait_for_timeout(800)
      await pg.evaluate(JS_PUT,['A',collect('xf2/A')])
      await pg.evaluate("(async()=>{const r=await navigator.storage.getDirectory();await openDirHandle(await r.getDirectoryHandle('A'));})()"); await pg.wait_for_timeout(1500)
      T=pg.locator('#grid .tile'); names=await pg.evaluate("[...document.querySelectorAll('#grid .tile')].map(t=>t._it&&t._it.name)")
      st=lambda: pg.evaluate("[[...SEL].map(x=>x.name),$('selGo').textContent,document.body.classList.contains('selmode'),getComputedStyle($('grid').querySelector('.tile.cur')||document.body).boxShadow]")
      await T.nth(0).click(); await T.nth(1).click(modifiers=['Control']); await pg.wait_for_timeout(200); s1=await st(); print(s1)
      if s1[0]!=names[0:2] or 'Сравнить' not in s1[1]: errs.append('два DXF: '+str(s1))
      pdf=[i for i,n in enumerate(names) if n.endswith('.pdf')][0]
      await T.nth(pdf).click(modifiers=['Control']); await pg.wait_for_timeout(200); s2=await st(); print(s2)
      if 'Открыть рядом' not in s2[1]: errs.append('с PDF: '+str(s2))
      await pg.click('#selGo'); await pg.wait_for_timeout(1500); o=await pg.evaluate('[VW.set.length,!!VW.cmp,!!OV,document.body.classList.contains("selmode")]'); print(o)
      if o!=[2,False,False,False]: errs.append('открытие рядом: '+str(o))
      await b.close()
  finally: srv.terminate()
  print('errors',errs)
asyncio.run(main())
