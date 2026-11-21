# Сравнение папок и деталей: пути (1), две панели (2), выделенный файл сразу (3), пути у пары (4), списки в окнах + двойной клик (6)
import asyncio,sys,subprocess
sys.path.insert(0,'/tmp/claude-0/t'); from cmpx import *
async def main():
  srv=subprocess.Popen('cd /tmp/claude-0/srv && python3 -m http.server 8765',shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); await asyncio.sleep(1)
  errs=[]
  try:
    async with async_playwright() as p:
      b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1500,'height':900}); pg.on('pageerror',lambda e:errs.append(str(e)))
      await setup(pg,'xf2/A','xf2/B')
      # (3) выделенный файл, который там лежит под другим номером (…01.03 → …01.04)
      await pg.evaluate("SET.preview=true;applyFilter();showItem(view.findIndex(x=>x.name.includes('01.03')))"); await pg.wait_for_timeout(800)
      await cmp(pg); await pg.wait_for_timeout(2500)
      v=await pg.evaluate('VW.cmp&&[VW.cmp.a.name,VW.cmp.b.name]'); print('focus',v)
      if not v or '01.04' not in v[1]: errs.append('выделенный файл не открылся сразу: '+str(v))
      # (1) пути на строке сравнения
      t=await pg.evaluate("(document.querySelector('#cmpPaths')||document.querySelector('#grid .cmphead')).innerText"); print('paths',t.replace('\n',' | '))
      if 'Архив 2024' not in t or 'Текущий' not in t: errs.append('нет путей: '+t)
      # (2) две панели
      await pg.evaluate("SET.preview=false;VW.cmp=null;if(VW.full)setFull(false);applyFilter()"); await pg.wait_for_timeout(800)
      rows=await pg.evaluate("[...document.querySelectorAll('#grid .cmprow:not(.cmphead)')].map(r=>[...r.children].map(c=>c.classList.contains('tile')?c._it.name:c.textContent.trim()))")
      print('rows',rows)
      if len(rows)<4 or not any(r[1].startswith('≠') for r in rows) or not any(r[1].startswith('⇢') for r in rows): errs.append('две панели: '+str(rows))
      tot=await pg.inner_text('.cmptot'); print(tot)
      if 'здесь 4' not in tot: errs.append('итог: '+tot)
      # (4)(6) пара: пути, нет «папки» у имён, списки в окнах, двойной клик вписывает обе
      await pg.locator('#grid .cmprow .cmpmid.go').first.click(); await pg.wait_for_timeout(3000)
      na=await pg.inner_text('#ovNa'); nb=await pg.inner_text('#ovNb'); vn=await pg.inner_text('#vName'); print(na,'|',nb,'|',vn)
      if 'Архив 2024' not in nb or '«' in vn: errs.append('пути у пары: '+na+' / '+nb+' / '+vn)
      lists=await pg.evaluate("[...document.querySelectorAll('.ovdl:not([hidden])')].map(l=>l.innerText)"); print('lists',lists)
      if len(lists)!=2 or 'справа Ø24' not in lists[0] or 'слева Ø20' not in lists[1]: errs.append('списки в окнах: '+str(lists))
      c=pg.locator('#stage canvas'); bb0=await c.nth(0).bounding_box()
      await pg.mouse.move(bb0['x']+200,bb0['y']+300); await pg.mouse.wheel(0,-400); await pg.wait_for_timeout(300)
      await pg.mouse.dblclick(bb0['x']+300,bb0['y']+300); await pg.wait_for_timeout(500)
      st=await pg.evaluate("panes.slice(0,2).map(p=>[p.fitted,+p.s.toFixed(4)])"); print('dbl',st)
      if not (st[0][0] and st[1][0] and st[0][1]==st[1][1]): errs.append('двойной клик вписал не обе: '+str(st))
      await b.close()
  finally: srv.terminate()
  print('errors',errs)
asyncio.run(main())
