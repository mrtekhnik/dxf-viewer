# ⟳ Обновить / F5 / возврат в окно: новые, изменённые, удалённые файлы — без сброса открытого файла и сравнения
import asyncio,sys,subprocess
sys.path.insert(0,'/tmp/claude-0/t'); from cmpx import *
FS="""async([op,rel,b64])=>{const r=await navigator.storage.getDirectory();let d=await r.getDirectoryHandle('A');const parts=rel.split('/');
 for(const q of parts.slice(0,-1))d=await d.getDirectoryHandle(q);
 if(op==='del'){await d.removeEntry(parts.at(-1));return 1;}
 const h=await d.getFileHandle(parts.at(-1),{create:true});const w=await h.createWritable();await w.write(Uint8Array.from(atob(b64),c=>c.charCodeAt(0)));await w.close();return 1;}"""
async def main():
  srv=subprocess.Popen('cd /tmp/claude-0/srv && python3 -m http.server 8765',shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); await asyncio.sleep(1)
  errs=[]
  try:
    async with async_playwright() as p:
      b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1400,'height':800}); pg.on('pageerror',lambda e:errs.append(str(e)))
      await setup(pg,layout='list')
      files=collect('cmp3/A'); n0=await pg.evaluate('items.length'); paths=await pg.evaluate('items.map(x=>x.path)'); print('было',n0)
      vis=await pg.evaluate("!$('btnRefr').hidden"); 
      if not vis: errs.append('кнопки ⟳ нет')
      dxf=[f for f in files if f[0].endswith('.dxf')]
      # открыть файл в просмотре
      await pg.evaluate("showItem(view.findIndex(x=>x.path.endsWith(%r)));setFull(true);0"%dxf[0][0].split('/')[-1]); await pg.wait_for_timeout(1000)
      cur=await pg.evaluate('view[VW.idx].path')
      # ничего не изменилось
      await pg.evaluate('refreshFolder(false)'); await pg.wait_for_timeout(800)
      f0=await pg.evaluate("$('flash')?$('flash').textContent:''"); print('без изменений:',f0)
      # новый, изменённый (другой файл открытого не трогаем), удалённый
      newrel=dxf[0][0].rsplit('/',1)[0]+'/НОВЫЙ-St-2-K1.dxf' if '/' in dxf[0][0] else 'НОВЫЙ-St-2-K1.dxf'
      await pg.evaluate(FS,['put',newrel,dxf[1][1]])
      await pg.evaluate(FS,['put',dxf[1][0],dxf[2][1]])
      delrel=[f for f in files if f[0].endswith('.pdf')][0][0]
      await pg.evaluate(FS,['del',delrel,''])
      await pg.keyboard.press('F5'); await pg.wait_for_timeout(1500)
      r=await pg.evaluate("[items.length,items.some(x=>x.path.endsWith('НОВЫЙ-St-2-K1.dxf')),items.some(x=>x.path.endsWith(%r)),view[VW.idx]&&view[VW.idx].path,VW.full,OPENLOG.map(x=>x[1]).filter(x=>x.includes('обновлён')).join('|')]"%delrel.split('/')[-1]); print(r)
      if r[0]!=n0 or not r[1] or r[2]: errs.append('состав: '+str(r))
      if r[3]!=cur or not r[4]: errs.append('открытый файл сбился: '+str(r[3:5]))
      if 'новых 1, изменено 1, удалено 1' not in r[5]: errs.append('итог: '+r[5])
      # сравнение остаётся и учитывает новый файл
      await pg.evaluate('setFull(false);0'); await cmp(pg)
      await pg.evaluate(FS,['put','НОВЫЙ2-St-2-K1.dxf',dxf[1][1]])
      await pg.evaluate("REFR.t=0;window.dispatchEvent(new Event('focus'));0"); await pg.wait_for_timeout(3000)
      c=await pg.evaluate("[!!CMP,CMP&&CMP.path,items.some(x=>x.path.endsWith('НОВЫЙ2-St-2-K1.dxf')),CMP&&!!CMP.map.get(items.find(x=>x.path.endsWith('НОВЫЙ2-St-2-K1.dxf'))),document.querySelectorAll('#grid .cmprow').length]"); print('сравнение',c)
      if not (c[0] and c[2] and c[3]) or 'Архив' not in str(c[1]): errs.append('сравнение после обновления: '+str(c))
      # правая колонка: подписи (размер, дата)
      m=await pg.evaluate("[...document.querySelectorAll('#grid .cmprow')].slice(1,3).map(r=>r.lastChild.querySelector&&r.lastChild.querySelector('.meta')?r.lastChild.querySelector('.meta').textContent:'')"); print('справа',m)
      if not all(m): errs.append('справа нет подписей: '+str(m))
      h=await pg.evaluate("[document.querySelector('#grid .cmphead').textContent,[...document.querySelectorAll('#grid .cmpwhy')].map(x=>x.textContent)]"); print('шапка',h)
      if 'Архив 2024' not in h[0] or 'Текущий' not in h[0]: errs.append('пути не над колонками: '+h[0])
      if not any('здесь' in x and 'там' in x for x in h[1]): errs.append('нет пояснения отличия: '+str(h[1]))
      await b.close()
  finally: srv.terminate()
  print('errors',errs)
asyncio.run(main())
