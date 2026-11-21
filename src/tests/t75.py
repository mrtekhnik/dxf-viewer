# зависший ответ диска: файл/список папки не отвечает — чтение не виснет, зависшее в списке непрочитанного; сравнение не ждёт пути
import asyncio,sys,subprocess
sys.path.insert(0,'/tmp/claude-0/t'); from cmpx import *
import glob
DXF=open(sorted(glob.glob('/home/claude/dxf-viewer/src/tests/dxf/*.dxf'))[0],encoding='latin1').read()
FAKE="""
window.fdir=(name,list,hang)=>{const d={kind:'directory',name,entries(){let i=0;return{next:()=>(hang!=null&&i>=hang)?new Promise(()=>{}):Promise.resolve(i<list.length?{done:false,value:list[i++]}:{done:true})};},
  queryPermission:async()=>'granted',isSameEntry:async x=>x===d,resolve:async()=>null};return [name,d];};
window.ffile=(name,txt,hang)=>[name,{kind:'file',name,getFile:()=>hang?new Promise(()=>{}):Promise.resolve(new File([txt],name))}];0
"""
async def main():
  srv=subprocess.Popen('cd /tmp/claude-0/srv && python3 -m http.server 8765',shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); await asyncio.sleep(1)
  errs=[]
  try:
    async with async_playwright() as p:
      b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1400,'height':700}); pg.on('pageerror',lambda e:errs.append(str(e)))
      await pg.add_init_script("localStorage.setItem('dxfv.set',JSON.stringify({}))")
      await pg.goto('http://localhost:8765/dxf-viewer/'); await pg.wait_for_timeout(800)
      await pg.evaluate(FAKE)
      await pg.evaluate("FST.to=1500;FST.slow=500;0")
      await pg.evaluate("""(d=>{const R=fdir('R',[ffile('a.dxf',d),ffile('b.dxf',d,true),fdir('S',[ffile('c.dxf',d)],1),fdir('H',[],0)])[1];window._p=openDirHandle(R).then(()=>window._done=1);})""",DXF)
      await pg.wait_for_timeout(1000); st=await pg.evaluate("$('status').textContent"); print('во время:',st)
      if 'жду ответ' not in st: errs.append('нет «жду ответ»: '+st)
      for i in range(20):
        await pg.wait_for_timeout(500)
        if await pg.evaluate("!!window._done"): break
      r=await pg.evaluate("[!!window._done,items.map(x=>x.path).sort(),OPENLOG.map(x=>x[1]).join('\\n'),$('noteT').textContent,[...$('noteL').children].map(x=>x.textContent)]"); print(r[0],r[1],r[3],r[4])
      if not r[0]: errs.append('чтение зависло')
      if r[1]!=['R/S/c.dxf','R/a.dxf']: errs.append('файлы: '+str(r[1]))
      if 'Не прочитано файлов: 1, папок: 2' not in r[3]: errs.append('итог: '+r[3])
      if not any('b.dxf' in x and 'нет ответа' in x for x in r[4]): errs.append('нет b.dxf в списке')
      if 'Долго нет ответа' not in r[2]: errs.append('журнал без «Долго нет ответа»')
      st=await pg.evaluate("$('status').textContent")
      if 'жду' in st: errs.append('строка состояния осталась: '+st)
      # сравнение: база «Недавних» не отвечает — сравнение всё равно открывается
      await pg.evaluate("$('noteBox').hidden=true;IDB.all=()=>new Promise(()=>{});0")
      await pg.evaluate("""(d=>{const R=fdir('R2',[ffile('a.dxf',d)])[1];window._c=0;cmpFromHandle(R).then(()=>window._c=1);})""",DXF)
      for i in range(12):
        await pg.wait_for_timeout(500)
        if await pg.evaluate("!!CMP"): break
      c=await pg.evaluate("[!!CMP,CMP&&CMP.name,OPENLOG.map(x=>x[1]).filter(x=>x.includes('R2')).join(' | ')]"); print(c)
      if not c[0]: errs.append('сравнение не открылось')
      for i in range(20):
        await pg.wait_for_timeout(500)
        if await pg.evaluate("!!window._c"): break
      if not await pg.evaluate("!!window._c"): errs.append('сравнение не закончилось (путь)')
      await b.close()
  finally: srv.terminate()
  print('errors',errs)
asyncio.run(main())
