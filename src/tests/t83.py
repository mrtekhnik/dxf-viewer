# сравнение с подпапкой открытой папки: подпапка предлагается, её файлы сами с собой не сравниваются; «Сравнить с…» не предлагает тот же файл
import asyncio,sys,subprocess
sys.path.insert(0,'/tmp/claude-0/t'); from cmpx import *
async def main():
  srv=subprocess.Popen('cd /tmp/claude-0/srv && python3 -m http.server 8765',shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); await asyncio.sleep(1)
  errs=[]
  try:
    async with async_playwright() as p:
      b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1400,'height':800}); pg.on('pageerror',lambda e:errs.append(str(e)))
      await setup(pg,'sub/A','cmp4/B')
      await pg.evaluate("window.knownPath=async h=>'Сервер / '+h.name;window.curDirHandle=async()=>window.__A;window.rememberRoot=async()=>null;0")
      await pg.evaluate("(async()=>{window.__S=await window.__A.getDirectoryHandle('Старое');await cmpFromHandle(window.__S);})()"); await pg.wait_for_timeout(3000)
      m=await pg.evaluate("[!!CMP,[...CMP.map].map(([a,c])=>[a.path,c.st,c.b&&c.b.path])]"); print(m)
      if not m[0]: errs.append('сравнение с подпапкой не открылось')
      else:
        paths=[x[0] for x in m[1]]
        if any('Старое' in x for x in paths): errs.append('файлы подпапки сравниваются сами с собой: '+str(paths))
        pr=[x for x in m[1] if x[0]=='A/АЮИА.320-02.03.00.00.02-St-16-K1.dxf']
        if not pr or pr[0][1] not in ('same','diff','geo','name') or 'Старое' not in str(pr[0][2]): errs.append('пара с подпапкой: '+str(pr))
      # «Сравнить с…» для файла из подпапки — без него самого
      c=await pg.evaluate("pickCands(items.find(x=>x.path.includes('Старое'))).map(x=>x.path+(x.cmpB?' (там)':''))"); print('кандидаты',c)
      if any('Старое' in x for x in c): errs.append('предлагает тот же файл: '+str(c))
      await b.close()
  finally: srv.terminate()
  print('errors',errs)
asyncio.run(main())
