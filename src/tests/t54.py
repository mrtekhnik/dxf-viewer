import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1300,'height':800})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.set_input_files('#inFiles',['blk/angle.dxf']); await pg.wait_for_timeout(1500)
    await pg.keyboard.press('d'); await pg.select_option('#measMode','ang'); await pg.wait_for_timeout(100)
    bb=await pg.locator('#stage canvas').first.bounding_box()
    sc=lambda x,y: pg.evaluate(f"(()=>{{const p=panes[0],o=p.doc.origin;return m2s(p,{x}-o[0],{y}-o[1])}})()")
    async def click(x,y):
      q=await sc(x,y); await pg.mouse.move(bb['x']+q[0],bb['y']+q[1]); await pg.wait_for_timeout(60); await pg.mouse.click(bb['x']+q[0],bb['y']+q[1]); await pg.wait_for_timeout(400)
    await click(200,30); await click(130,80)        # вертикальная кромка и скос
    await click(100,0); await click(130,80)          # низ и скос
    print('angles', await pg.evaluate("panes[0].ms.items.map(i=>i.A&&i.A.deg.toFixed(2))"))
    await pg.select_option('#measMode','dim'); await click(0,0); await click(0,100); await click(-6,50)
    await pg.screenshot(path='t54.png')
    await pg.keyboard.press('Escape'); await pg.wait_for_timeout(200); print('esc1: meas',await pg.evaluate('MEAS.on'),'full',await pg.evaluate('VW.full'))
    await pg.keyboard.press('Escape'); await pg.wait_for_timeout(200); print('esc2: full',await pg.evaluate('VW.full'))
    print('errors',errs); await b.close()
asyncio.run(main())
