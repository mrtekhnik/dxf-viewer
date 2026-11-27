# этап 2: толщины — раскрывающийся список с несколькими галочками, «Показывать» отдельно; путь в строке — по клику; листов PDF; панель в один ряд
import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1400,'height':800})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.set_input_files('#inFolder','kit/Заказ'); await pg.wait_for_timeout(3000)
    n0=await pg.evaluate('view.length')
    await pg.click('#mtBtn'); await pg.wait_for_timeout(200)
    opts=await pg.evaluate("[...document.querySelectorAll('#mtMenu .mt-o')].map(o=>o.textContent.trim())"); print('список',opts)
    if len(opts)<3: errs.append('мало толщин: '+str(opts))
    cbs=pg.locator('#mtMenu .mt-o:not(.mt-all) input')
    await cbs.nth(0).check(); await pg.wait_for_timeout(200)
    if not await pg.evaluate("!$('mtMenu').hidden"): errs.append('список закрылся после галочки')
    await pg.locator('#mtMenu .mt-o:not(.mt-all) input').nth(1).check(); await pg.wait_for_timeout(200)
    r=await pg.evaluate("[MTF.size,view.length,$('mtBtn').textContent,[...document.querySelectorAll('#mtBar .mt-l')].map(x=>x.textContent)]"); print('выбрано',r)
    if r[0]!=2 or not (0<r[1]<n0) or ',' not in r[2]: errs.append('две толщины: '+str(r))
    if 'Показывать:' not in r[3]: errs.append('нет подписи «Показывать»')
    await pg.keyboard.press('Escape'); 
    if not await pg.evaluate("$('mtMenu').hidden"): errs.append('Esc не закрыл список')
    await pg.click('#mtBtn'); await pg.locator('#mtMenu .mt-all input').check(); await pg.wait_for_timeout(200)
    if await pg.evaluate('[MTF.size,view.length]')!=[0,n0]: errs.append('«все» не сбросило')
    await pg.mouse.click(700,600)
    # путь по клику
    await pg.evaluate("setDir('Заказ/DXF');0"); await pg.wait_for_timeout(300)
    cr=await pg.evaluate("[...document.querySelectorAll('#status a.crumb')].map(a=>a.textContent+(a.classList.contains('here')?'*':''))"); print('путь',cr)
    if cr!=['Заказ','DXF*']: errs.append('путь: '+str(cr))
    await pg.locator('#status a.crumb').first.click(); await pg.wait_for_timeout(300)
    if await pg.evaluate('curDir')!='Заказ': errs.append('клик по пути не перешёл: '+str(await pg.evaluate('curDir')))
    for i in range(20):
      st=await pg.evaluate("$('status').textContent")
      if 'листов PDF: ' in st and 'не прочитано' not in st: break
      await pg.wait_for_timeout(300)
    print('строка',st)
    import re
    m=re.search(r'листов PDF: (\d+)',st)
    if not m or int(m.group(1))<3: errs.append('листов PDF: '+st)
    # панель в один ряд при всех кнопках
    for w in [1400,1280,1150,1000]:
      await pg.set_viewport_size({'width':w,'height':800}); await pg.evaluate("$('btnLog').hidden=false;$('btnCmp').hidden=false;$('btnTree').hidden=false;$('btnBrowse').hidden=false;0"); await pg.wait_for_timeout(300)
      r=await pg.evaluate("(()=>{const H=document.querySelector('header'),g=[...H.children].filter(x=>x.offsetParent!==null&&x.tagName!=='INPUT');return [H.className,g.every(x=>x.offsetTop<=g[0].offsetTop+8),H.offsetHeight]})()"); print(w,r)
      if not r[1] and w>=1150: errs.append(f'{w}: панель в два ряда {r}')
    print('errors',errs); await b.close()
asyncio.run(main())
