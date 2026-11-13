import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1400,'height':850})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.set_input_files('#inFiles',['cmp2/Заказ А/DXF/АБВГ.200001.003-Ст3-3-k1.dxf','cmp2/Заказ А/DXF/АБВГ.200001.002-Ст3-3-k1.dxf']); await pg.wait_for_timeout(1500)
    await pg.locator('.tile').first.dblclick(); await pg.wait_for_timeout(800)
    await pg.keyboard.press('d'); await pg.wait_for_timeout(200)
    bb=await pg.locator('#stage canvas').first.bounding_box()
    sc=lambda x,y: pg.evaluate(f"(()=>{{const p=panes[0],o=p.doc.origin;return m2s(p,{x}-o[0],{y}-o[1])}})()")
    async def click(x,y):
      q=await sc(x,y); await pg.mouse.move(bb['x']+q[0],bb['y']+q[1]); await pg.wait_for_timeout(60); await pg.mouse.click(bb['x']+q[0],bb['y']+q[1]); await pg.wait_for_timeout(400)
    await click(0,0); await click(250,60); await click(120,-6)
    await pg.select_option('#measMode','dist'); await click(50,60); await click(150,150)
    print('items', await pg.evaluate("panes[0].ms.items.map(i=>i.t)"))
    await pg.screenshot(path='t53a.png')
    # двойной клик — вписать, без новых точек
    await pg.evaluate("panes[0].zoomAt(400,400,3)"); q=await sc(150,75); await pg.mouse.dblclick(bb['x']+q[0],bb['y']+q[1]); await pg.wait_for_timeout(300)
    print('after dbl fitted', await pg.evaluate('panes[0].fitted'), 'pts', await pg.evaluate('panes[0].ms.pts.length'), 'items', await pg.evaluate('panes[0].ms.items.length'))
    await pg.keyboard.press('ArrowRight'); await pg.wait_for_timeout(800); print('other file items', await pg.evaluate('panes[0].ms?panes[0].ms.items.length:null'), await pg.evaluate('VW.set[0].name'))
    await pg.keyboard.press('ArrowLeft'); await pg.wait_for_timeout(800); print('back items', await pg.evaluate('msOf(panes[0]).items.length'))
    await pg.keyboard.press('Escape'); await pg.wait_for_timeout(300); print('esc -> full', await pg.evaluate('VW.full'))
    print('errors',errs); await b.close()
asyncio.run(main())
