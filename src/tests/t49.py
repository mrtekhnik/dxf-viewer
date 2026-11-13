import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1400,'height':850})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.set_input_files('#inFiles',['cmp2/Заказ А/DXF/АБВГ.200001.003-Ст3-3-k1.dxf']); await pg.wait_for_timeout(1500)
    await pg.wait_for_timeout(500)
    await pg.keyboard.press('d'); await pg.wait_for_timeout(200); print('meas on', await pg.evaluate('MEAS.on'))
    cv=pg.locator('#stage canvas').first; bb=await cv.bounding_box()
    # координаты экрана для точек детали: центр отверстия (50,60), угол (0,0), линия (60..200,110)
    sc=lambda x,y: pg.evaluate(f"(()=>{{const p=panes[0],o=p.doc.origin,q=m2s(p,{x}-o[0],{y}-o[1]);return q}})()")
    a=await sc(0,0); b2=await sc(300,150); c=await sc(57.07,67.07); l=await sc(100,110)
    await pg.mouse.move(bb['x']+a[0]+3,bb['y']+a[1]-2); await pg.wait_for_timeout(100); print('hover', await pg.evaluate("panes[0].ms.hover.snap"))
    await pg.mouse.click(bb['x']+a[0]+3,bb['y']+a[1]-2); await pg.mouse.click(bb['x']+b2[0]-2,bb['y']+b2[1]+3); await pg.wait_for_timeout(200)
    print('ms', await pg.evaluate('JSON.stringify(panes[0].ms.items)+JSON.stringify(panes[0].ms.pts)'))
    print('dist:', await pg.evaluate("measText(panes[0].ms.items[0])"))
    await pg.mouse.click(bb['x']+c[0]+1,bb['y']+c[1]); await pg.wait_for_timeout(100); print('circle:', await pg.evaluate("measText(panes[0].ms.items[1])"))
    await pg.mouse.click(bb['x']+l[0],bb['y']+l[1]+1); await pg.wait_for_timeout(100); print('line:', await pg.evaluate("panes[0].ms.items[2]&&measText(panes[0].ms.items[2])"))
    await pg.screenshot(path='t49.png')
    await pg.keyboard.press('Escape'); print('after esc items', await pg.evaluate("panes[0].ms.items.length"), 'on', await pg.evaluate('MEAS.on'))
    await pg.keyboard.press('Escape'); print('after esc2 on', await pg.evaluate('MEAS.on'), 'full', await pg.evaluate('VW.full'))
    print('errors',errs); await b.close()
asyncio.run(main())
