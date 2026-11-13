import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1400,'height':850})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.set_input_files('#inFiles',['cmp2/Заказ А/DXF/АБВГ.200001.003-Ст3-3-k1.dxf']); await pg.wait_for_timeout(1500)
    await pg.keyboard.press('d'); await pg.wait_for_timeout(200)
    bb=await pg.locator('#stage canvas').first.bounding_box()
    sc=lambda x,y: pg.evaluate(f"(()=>{{const p=panes[0],o=p.doc.origin;return m2s(p,{x}-o[0],{y}-o[1])}})()")
    async def click(x,y,dx=0,dy=0):
      q=await sc(x,y); print('  click',x,y, await pg.evaluate(f'(()=>{{const p=panes[0];const h=measPick(p,{q[0]+dx},{q[1]+dy});return [h.snap?h.snap[2]:h.ent?h.ent.t:"-",p.ms?p.ms.pts.length:0]}})()')); await pg.mouse.move(bb['x']+q[0]+dx,bb['y']+q[1]+dy); await pg.wait_for_timeout(50); await pg.mouse.click(bb['x']+q[0]+dx,bb['y']+q[1]+dy); await pg.wait_for_timeout(80)
    # горизонтальный: от левого нижнего угла до центра правого отверстия, положить ниже детали
    await click(0,0); await click(250,60); await click(120,-6)
    # вертикальный: от низа до верха, положить правее
    await click(0,0); await click(0,150); await click(-8,75)
    # клик в пустоту — не ставится
    await click(150,30)
    print('items', await pg.evaluate("panes[0].ms.items.map(i=>i.t==='lin'?i.dir+' '+dimGeom(panes[0],i).val.toFixed(2):i.t)"), 'pts', await pg.evaluate('panes[0].ms.pts.length'))
    await pg.screenshot(path='t52a.png')
    print('esc skipped (now exits viewer)')
    await pg.keyboard.press('Backspace'); print('after bksp', await pg.evaluate('panes[0].ms.items.length'))
    await pg.select_option('#measPrec','2'); await pg.wait_for_timeout(100); await pg.screenshot(path='t52b.png')
    await pg.keyboard.press('d'); print('off', await pg.evaluate('MEAS.on'))
    print('errors',errs); await b.close()
asyncio.run(main())
