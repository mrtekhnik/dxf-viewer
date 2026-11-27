# этап 3: измерения в сравнении DXF; пары PDF из папок А и Б — рядом, листание парами одного вида, листы вместе при 🔒
import asyncio,sys,subprocess
sys.path.insert(0,'/tmp/claude-0/t'); from cmpx import *
async def main():
  srv=subprocess.Popen('cd /tmp/claude-0/srv && python3 -m http.server 8765',shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); await asyncio.sleep(1)
  errs=[]
  try:
    async with async_playwright() as p:
      b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1400,'height':800}); pg.on('pageerror',lambda e:errs.append(str(e)))
      await setup(pg,'cmp4/A','cmp4/B',layout='list'); await cmp(pg)
      m=await pg.evaluate("view.map(x=>[x.name,CMP.map.get(x)&&CMP.map.get(x).b&&CMP.map.get(x).b.name])"); print(m)
      if not any('Рама.pdf' in a and b and 'Рама нова' in b for a,b in m): errs.append('пара PDF по номеру не нашлась')
      # --- пары PDF ---
      await pg.evaluate("$('typeSel').value='pdf';$('typeSel').dispatchEvent(new Event('change'));0"); await pg.wait_for_timeout(300)
      await pg.evaluate("cmpOpenFor(view.find(x=>x.name.includes('Рама')));0"); await pg.wait_for_timeout(2500)
      r=await pg.evaluate("[VW.set.map(x=>x.name),panes.slice(0,2).map(p=>p.isPdf&&p.doc&&p.doc.pages)]"); print('пара',r)
      if len(r[0])!=2 or r[1]!=[3,3]: errs.append('пара PDF не открылась: '+str(r))
      await pg.evaluate("SET.sync=true;VW.active=0;0"); await pg.keyboard.press('PageDown'); await pg.wait_for_timeout(1500)
      pgs=await pg.evaluate("panes.slice(0,2).map(p=>p.pageNo)"); print('листы',pgs)
      if pgs!=[2,2]: errs.append('листы не вместе: '+str(pgs))
      await pg.evaluate("SET.sync=false;0"); await pg.keyboard.press('PageDown'); await pg.wait_for_timeout(1500)
      pgs2=await pg.evaluate("panes.slice(0,2).map(p=>p.pageNo)"); print('без 🔒',pgs2)
      if pgs2!=[3,2]: errs.append('без 🔒 листается и второе: '+str(pgs2))
      await pg.evaluate("$('typeSel').value='';$('typeSel').dispatchEvent(new Event('change'));0"); await pg.wait_for_timeout(300)
      await pg.evaluate("cmpOpenFor(view.find(x=>x.name.includes('Рама')));0"); await pg.wait_for_timeout(1500)
      seen=[]
      for i in range(3):
        await pg.keyboard.press('ArrowRight'); await pg.wait_for_timeout(1200); seen.append(await pg.evaluate("VW.set.map(x=>x.type).join('+')"))
      print('листание',seen)
      if any(s!='pdf+pdf' for s in seen): errs.append('листание вышло на DXF: '+str(seen))
      # --- измерения в сравнении DXF ---
      await pg.evaluate("cmpOpenFor(view.find(x=>x.name.includes('00.02-St')));0"); await pg.wait_for_timeout(3500)
      st=await pg.evaluate("[!!OV&&!!OV.res,$('vMeas').hidden]"); print('сравнение DXF',st)
      if not st[0] or st[1]: errs.append('нет кнопки размеров в сравнении: '+str(st))
      await pg.keyboard.press('d'); await pg.wait_for_timeout(300)
      # две точки привязки: концы самой длинной линии левой детали
      for side in [0,1]:
        res=await pg.evaluate("""(side=>{const p=panes[side],M=measEntP(p);const L=M.E.filter(e=>e.t==='L').sort((a,b)=>Math.hypot(b.x2-b.x1,b.y2-b.y1)-Math.hypot(a.x2-a.x1,a.y2-a.y1))[0];
          return [M.E.length,L?Math.hypot(L.x2-L.x1,L.y2-L.y1):0,L?m2s(p,L.x1,L.y1):null,L?m2s(p,L.x2,L.y2):null,p.cv.getBoundingClientRect().left,p.cv.getBoundingClientRect().top]})(%d)"""%side)
        n,ln,a,bb,ox,oy=res
        if not n: errs.append(f'окно {side}: нет привязок'); continue
        for q in [a,bb]:
          await pg.mouse.move(ox+q[0],oy+q[1]); await pg.wait_for_timeout(60); await pg.mouse.click(ox+q[0],oy+q[1]); await pg.wait_for_timeout(150)
        await pg.mouse.click(ox+(a[0]+bb[0])/2+30,oy+(a[1]+bb[1])/2+30); await pg.wait_for_timeout(300)
        it=await pg.evaluate("(side=>{const M=panes[side].ms;const it=M&&M.items[M.items.length-1];return it?[it.t,Math.hypot(it.b[0]-it.a[0],it.b[1]-it.a[1])]:null})(%d)"%side)
        print('окно',side,'линия',round(ln,3),'размер',it)
        if not it or abs(it[1]-ln)>0.01: errs.append(f'окно {side}: размер {it}, ждали {ln}')
      await b.close()
  finally: srv.terminate()
  print('errors',errs)
asyncio.run(main())
