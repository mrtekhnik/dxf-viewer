import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1400,'height':850})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.set_input_files('#inFiles',['cmp2/Заказ А/DXF/АБВГ.200001.003-Ст3-3-k1.dxf']); await pg.wait_for_timeout(1500)
    await pg.keyboard.press('d'); await pg.select_option('#measMode','gap'); await pg.wait_for_timeout(100)
    bb=await pg.locator('#stage canvas').first.bounding_box()
    sc=lambda x,y: pg.evaluate(f"(()=>{{const p=panes[0],o=p.doc.origin;return m2s(p,{x}-o[0],{y}-o[1])}})()")
    async def click(x,y):
      q=await sc(x,y); await pg.mouse.move(bb['x']+q[0],bb['y']+q[1]); await pg.wait_for_timeout(60); await pg.mouse.click(bb['x']+q[0],bb['y']+q[1]); await pg.wait_for_timeout(400)
    await click(60,60); await click(140,60)          # два отверстия: 80
    await click(50,70); await click(100,110)         # отверстие и линия: ~40.99
    await click(250,50); await click(300,40)         # отверстие и правая кромка: 300-250-10=40
    print('gaps', await pg.evaluate("panes[0].ms.items.map(i=>i.d.toFixed(3))"))
    await pg.screenshot(path='t59a.png')
    # лупа по левой кнопке
    await pg.keyboard.press('d'); await pg.click('#vLoupe'); await pg.mouse.move(bb['x']+200,bb['y']+60)
    print('armed, visible', await pg.is_visible('#loupe'))
    await pg.mouse.down(); await pg.wait_for_timeout(200); print('down visible', await pg.is_visible('#loupe'), 'clip', await pg.evaluate("$('loupe').style.clipPath"))
    await pg.screenshot(path='t59b.png'); await pg.mouse.up(); await pg.wait_for_timeout(100); print('up visible', await pg.is_visible('#loupe'))
    print('errors',errs); await b.close()
asyncio.run(main())
