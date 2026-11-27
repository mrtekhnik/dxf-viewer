# сравнение закрыли ✕: сравнение заканчивается полностью (нет полосы и красного в одиночном файле); «Сравнить с…» — прошлая пара первой (↺)
import asyncio,sys,subprocess
sys.path.insert(0,'/tmp/claude-0/t'); from cmpx import *
async def main():
  srv=subprocess.Popen('cd /tmp/claude-0/srv && python3 -m http.server 8765',shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); await asyncio.sleep(1)
  errs=[]
  try:
    async with async_playwright() as p:
      b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1400,'height':800}); pg.on('pageerror',lambda e:errs.append(str(e)))
      await setup(pg,'cmp4/A','cmp4/B')
      await pg.evaluate("(()=>{const a=items.find(x=>x.name.includes('00.02')),b=items.find(x=>x.name.includes('00.04-St'));showItem(view.indexOf(a));setFull(true);cmpOpen(a,b,true);})()"); await pg.wait_for_timeout(2500)
      await pg.click('#vClose'); await pg.wait_for_timeout(500)
      await pg.locator('.tile').filter(has_text='00.02').first.dblclick(); await pg.wait_for_timeout(1500)
      r=await pg.evaluate("[!!OV,VW.set.length,$('ovBar').hidden,!!panes[0].ov]"); print('снова открыли',r)
      if r!=[False,1,True,False]: errs.append('остатки сравнения: '+str(r))
      await pg.keyboard.press('v'); await pg.wait_for_timeout(1500)
      f=await pg.evaluate("$('pickList').firstChild&&$('pickList').firstChild.textContent"); print('первый в списке',f)
      if not f or '↺' not in f or '00.04-St' not in f: errs.append('прошлая пара не первая: '+str(f))
      await b.close()
  finally: srv.terminate()
  print('errors',errs)
asyncio.run(main())
