# 📋 копировать путь (путь папки — один раз), ширина окна выбора, наложение (N) без ошибки
import asyncio,sys,subprocess
sys.path.insert(0,'/tmp/claude-0/t'); from cmpx import *
async def main():
  srv=subprocess.Popen('cd /tmp/claude-0/srv && python3 -m http.server 8765',shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); await asyncio.sleep(1)
  errs=[]
  try:
    async with async_playwright() as p:
      b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); ctx=await b.new_context(viewport={'width':1400,'height':800},permissions=['clipboard-read','clipboard-write']); pg=await ctx.new_page(); pg.on('pageerror',lambda e:errs.append(str(e)))
      await setup(pg,'cmp4/A','cmp4/B')
      await pg.evaluate("(()=>{const a=items.find(x=>x.name.includes('00.02'));showItem(view.indexOf(a));setFull(true);})()"); await pg.wait_for_timeout(1000)
      await pg.click('#vShare'); await pg.click('#shPath'); await pg.wait_for_timeout(200)
      if await pg.evaluate("$('shPathSet').hidden"): errs.append('не спросил путь папки')
      await pg.fill('#shPathIn','\\\\server\\Заказы\\Текущий\\A'); await pg.click('#shPathOk'); await pg.wait_for_timeout(300)
      c=await pg.evaluate("navigator.clipboard.readText()"); print('буфер',c)
      if c!='\\\\server\\Заказы\\Текущий\\A\\АЮИА.320-02.03.00.00.02-St-16-K1.dxf': errs.append('путь: '+c)
      await pg.keyboard.press('ArrowRight'); await pg.wait_for_timeout(800)
      await pg.click('#vShare'); await pg.click('#shPath'); await pg.wait_for_timeout(300)
      c2=await pg.evaluate("[navigator.clipboard.readText(),$('shPathSet').hidden]"); c2[0]=await pg.evaluate("navigator.clipboard.readText()"); print('второй',c2)
      if not c2[1] or not c2[0].startswith('\\\\server\\Заказы\\Текущий\\A\\') or c2[0]==c: errs.append('второй файл: '+str(c2))
      # ширина окна выбора
      for v,mn,mx in [('n',400,470),('m',600,650),('f',1300,1400)]:
        await pg.evaluate(f"SET.pickW='{v}';applyPickW();$('pickPanel').hidden=false;0"); w=await pg.evaluate("$('pickPanel').getBoundingClientRect().width")
        if not mn<=w<=mx: errs.append(f'ширина {v}: {w}')
      await pg.evaluate("$('pickPanel').hidden=true;0")
      # наложение (N) — без ошибки
      await pg.evaluate("(()=>{const a=items.find(x=>x.name.includes('00.02')),b=items.find(x=>x.name.includes('00.04-St'));cmpOpen(a,b,true);})()"); await pg.wait_for_timeout(2500)
      await pg.keyboard.press('n'); await pg.wait_for_timeout(2500)
      o=await pg.evaluate("[!!OV,OV&&OV.mode,VW.set.length,!!(panes[0].ov&&panes[0].ov.res)]"); print('наложение',o)
      if o!=[True,'over',1,True]: errs.append('наложение: '+str(o))
      await pg.keyboard.press('n'); await pg.wait_for_timeout(2500)
      o=await pg.evaluate("[!!OV,OV&&OV.mode,VW.set.length]"); print('две панели',o)
      if o!=[True,'two',2]: errs.append('две панели: '+str(o))
      await b.close()
  finally: srv.terminate()
  print('errors',errs)
asyncio.run(main())
