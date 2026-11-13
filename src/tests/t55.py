import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1300,'height':700})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.set_input_files('#inFiles',['blk/bigR.dxf']); await pg.wait_for_timeout(1500)
    await pg.keyboard.press('d'); await pg.wait_for_timeout(100)
    bb=await pg.locator('#stage canvas').first.bounding_box()
    sc=lambda x,y: pg.evaluate(f"(()=>{{const p=panes[0],o=p.doc.origin;return m2s(p,{x}-o[0],{y}-o[1])}})()")
    async def click(x,y,dx=0,dy=0):
      q=await sc(x,y); await pg.mouse.move(bb['x']+q[0]+dx,bb['y']+q[1]+dy); await pg.wait_for_timeout(60); await pg.mouse.click(bb['x']+q[0]+dx,bb['y']+q[1]+dy); await pg.wait_for_timeout(400)
    await click(250,84.95); await click(280,70)   # большая дуга R250 → надпись внутри детали рядом
    await click(65.66,25.66); await click(90,30)      # отверстие Ø16
    await click(380+10*0.707,20+10*0.707); await click(395,55)
    print('items', await pg.evaluate("panes[0].ms.items.map(i=>i.e?entText(i.e).main+' '+(i.o?'o':'-'):i.t+' '+JSON.stringify(i.a))"))
    await pg.screenshot(path='t55.png')
    print('errors',errs); await b.close()
asyncio.run(main())
