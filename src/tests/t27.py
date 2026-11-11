import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1400,'height':850})
    await pg.add_init_script("try{const s=JSON.parse(localStorage.getItem('dxfv.set')||'{}');if(s.click===undefined){s.click='1';localStorage.setItem('dxfv.set',JSON.stringify(s))}}catch(e){}")
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.set_input_files('#inFolder','kit/Заказ'); await pg.wait_for_timeout(1200)
    await pg.locator('.tile', has_text='Корпус').click(); await pg.wait_for_timeout(1200)
    chk="(()=>{const p=panes[0];const f=fitView(p.doc,p.xf,p.W,p.H,0.02);return [p.W|0,p.H|0,(p.s/f.s).toFixed(3)]})()"
    print('single:', await pg.evaluate(chk))
    await pg.keyboard.press('r'); await pg.wait_for_timeout(1800); print('side:', await pg.evaluate(chk))
    await pg.set_viewport_size({'width':1000,'height':700}); await pg.wait_for_timeout(800); print('resized:', await pg.evaluate(chk))
    await pg.keyboard.press('r'); await pg.wait_for_timeout(1200); print('back single:', await pg.evaluate(chk))
    # zoom in then side: relative zoom kept
    box=await pg.locator('#stage canvas').first.bounding_box(); await pg.mouse.move(box['x']+200,box['y']+200); await pg.mouse.wheel(0,-500); await pg.wait_for_timeout(200)
    z0=await pg.evaluate(chk); await pg.set_viewport_size({'width':1300,'height':800}); await pg.wait_for_timeout(800); print('zoomed', z0, '-> after resize', await pg.evaluate(chk))
    print('errors', errs); await b.close()
asyncio.run(main())
