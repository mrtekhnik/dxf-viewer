# наложение, выбранное заранее: сравнение открывается сразу в наложении, мигание, следующая пара, повторное открытие
import asyncio,sys,subprocess
sys.path.insert(0,'/tmp/claude-0/t'); from cmpx import *
async def main():
  srv=subprocess.Popen('cd /tmp/claude-0/srv && python3 -m http.server 8765',shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); await asyncio.sleep(1)
  errs=[]
  try:
    async with async_playwright() as p:
      b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1400,'height':800}); pg.on('pageerror',lambda e:errs.append(str(e)))
      await setup(pg,'cmp4/A','cmp4/B'); await pg.evaluate("SET.cmpView='over';SET.blink=true;saveSet();0"); await cmp(pg)
      for nm in ['00.02','00.04-St','00.06']:
        await pg.evaluate(f"cmpOpenFor(view.find(x=>x.name.includes('{nm}')));0"); await pg.wait_for_timeout(2500)
        print(nm,await pg.evaluate("[!!OV,OV&&OV.mode,!!(OV&&OV.res),VW.set.length]"))
      await pg.keyboard.press(' '); await pg.wait_for_timeout(300); print('мигание',await pg.evaluate("OV&&OV.blink"))
      await pg.keyboard.press('ArrowRight'); await pg.wait_for_timeout(2500); print('след.',await pg.evaluate("[!!OV&&!!OV.res,OV&&OV.mode]"))
      await pg.click('#vClose'); await pg.wait_for_timeout(500); await pg.evaluate("cmpOpenFor(view.find(x=>x.name.includes('00.02')));0"); await pg.wait_for_timeout(2500)
      print('после закрытия снова',await pg.evaluate("[!!OV&&!!OV.res,OV&&OV.mode]"))
      await b.close()
  finally: srv.terminate()
  print('errors',errs)
asyncio.run(main())
