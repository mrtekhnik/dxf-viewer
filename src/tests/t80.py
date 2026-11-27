# этап 1: кнопки мыши назад/вперёд, стрелки у краёв, Esc закрывает окна, имя корня, новое окно, без «сравнить с собой»
import asyncio,sys,subprocess
sys.path.insert(0,'/tmp/claude-0/t'); from cmpx import *
async def main():
  srv=subprocess.Popen('cd /tmp/claude-0/srv && python3 -m http.server 8765',shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); await asyncio.sleep(1)
  errs=[]
  try:
    async with async_playwright() as p:
      b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); ctx=await b.new_context(viewport={'width':1400,'height':800}); pg=await ctx.new_page(); pg.on('pageerror',lambda e:errs.append(str(e)))
      await setup(pg)
      st=await pg.evaluate("$('status').textContent"); print('строка:',st)
      if not st.startswith('Папка: A'): errs.append('нет имени корня: '+st)
      await pg.evaluate("showItem(0);setFull(true);0"); await pg.wait_for_timeout(800)
      i0=await pg.evaluate('VW.idx')
      bb=await pg.locator('#stageWrap').bounding_box()
      await pg.mouse.move(bb['x']+bb['width']/2,bb['y']+bb['height']/2)
      await pg.mouse.down(button='right'); await pg.mouse.up(button='right')
      await pg.evaluate("document.dispatchEvent(new MouseEvent('mouseup',{button:4,bubbles:true}));0"); await pg.wait_for_timeout(400)
      i1=await pg.evaluate('VW.idx')
      await pg.evaluate("document.dispatchEvent(new MouseEvent('mouseup',{button:3,bubbles:true}));0"); await pg.wait_for_timeout(400)
      i2=await pg.evaluate('VW.idx'); print('мышь',i0,i1,i2)
      if not (i1==i0+1 and i2==i0): errs.append(f'кнопки мыши: {i0} {i1} {i2}')
      await pg.mouse.move(bb['x']+bb['width']-20,bb['y']+bb['height']/2); await pg.wait_for_timeout(200)
      vis=await pg.evaluate("getComputedStyle($('edgeR')).display"); print('стрелка справа',vis)
      if vis!='block': errs.append('стрелка у края не появилась')
      await pg.click('#edgeR'); await pg.wait_for_timeout(400)
      if await pg.evaluate('VW.idx')!=i0+1: errs.append('стрелка не листает')
      await pg.mouse.move(bb['x']+bb['width']/2,bb['y']+bb['height']/2); await pg.wait_for_timeout(200)
      if await pg.evaluate("getComputedStyle($('edgeR')).display")!='none': errs.append('стрелка не прячется')
      await pg.evaluate("setFull(false);0"); await pg.wait_for_timeout(300)
      # Esc: меню 📂 и окно сравнения
      await pg.evaluate("$('openMenu').hidden=false;0"); await pg.keyboard.press('Escape')
      if not await pg.evaluate("$('openMenu').hidden"): errs.append('Esc не закрыл меню')
      await pg.evaluate("$('cmpPanel').hidden=false;0"); await pg.keyboard.press('Escape')
      if not await pg.evaluate("$('cmpPanel').hidden"): errs.append('Esc не закрыл окно сравнения')
      # в списке сравнения нет открытой папки
      await pg.evaluate("LS.set('cmpRecent',[{id:items[0].rid,name:'A',t:Date.now(),n:4}]);0")
      await pg.evaluate("IDB.get=async()=>null;IDB.all=async()=>[];0"); await pg.click('#btnCmp'); await pg.wait_for_timeout(1500)
      rows=await pg.evaluate("[...$('cmpRecent').children].map(x=>x.textContent)"); print('в списке сравнения',rows)
      if any(r.startswith('📁A') for r in rows): errs.append('предлагает сравнить с собой: '+str(rows))
      await pg.keyboard.press('Escape')
      # сравнение папок: Esc выходит
      await cmp(pg); await pg.evaluate("if(viewerShown()&&VW.full)setFull(false);0"); await pg.keyboard.press('Escape'); await pg.wait_for_timeout(300)
      c=await pg.evaluate('!!CMP'); print('после Esc',await pg.evaluate('[!!CMP,!!VW.cmp,VW.full,!!OV,viewerShown(),SEL.size,document.activeElement.tagName+"#"+document.activeElement.id]'))
      if c: 
        await pg.keyboard.press('Escape'); c=await pg.evaluate('!!CMP')
      if c: errs.append('Esc не выходит из сравнения')
      # новое окно
      u=await pg.evaluate("window.open=(u,t)=>{window._wo=u;return {};};$('btnNewWin').click();window._wo")
      c2=await b.new_context(); w=await c2.new_page(); await w.goto('http://localhost:8765'+u); await w.wait_for_timeout(1200)
      r=await w.evaluate("[location.search.startsWith('?new='),NEWWIN,items.length]"); print('новое окно',u,r)
      if not (r[0] and r[1] and r[2]==0): errs.append('новое окно: '+str(r))
      await b.close()
  finally: srv.terminate()
  print('errors',errs)
asyncio.run(main())
