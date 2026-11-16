# Материал и толщина: режимы DXF / PDF / вместе (PDF — по своим развёрткам)
import asyncio,glob,os
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1500,'height':800}); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    await pg.goto('file:///home/claude/dxf-viewer.html')
    fs=sorted(f for f in glob.glob('tree/Изделие 320/**/*.*',recursive=True) if os.path.isfile(f))
    await pg.set_input_files('#inFiles',fs); await pg.wait_for_timeout(2500)
    chips=await pg.evaluate("[...document.querySelectorAll('#mtBar .mt-c')].map(c=>c.textContent)"); print('chips dxf',chips)
    await pg.locator('#mtBar .mt-c').nth(1).click(); await pg.wait_for_timeout(400)
    v=lambda: pg.evaluate("view.map(x=>x.type+':'+x.name)")
    d=await v(); print('dxf mode',d)
    if not d or any(not x.startswith('dxf') for x in d): errs.append('DXF: '+str(d))
    await pg.locator('#mtBar .mt-w button').nth(1).click(); await pg.wait_for_timeout(400); pp=await v(); print('pdf mode',pp)
    if not pp or any(not x.startswith('pdf') for x in pp): errs.append('PDF: '+str(pp))
    await pg.locator('#mtBar .mt-w button').nth(2).click(); await pg.wait_for_timeout(400); a=await v(); print('all mode',a)
    if sorted(a)!=sorted(d+pp): errs.append('вместе: '+str(a))
    await pg.evaluate("SET.sortMt=true;MTF='';applyFilter()"); await pg.wait_for_timeout(300); print('sorted all', await v())
    await pg.screenshot(path='t71.png',clip={'x':0,'y':0,'width':1500,'height':130})
    await pg.evaluate("SET.mtShow='dxf';SET.sortMt=false;saveSet()")
    print('errors',errs); await b.close()
asyncio.run(main())
