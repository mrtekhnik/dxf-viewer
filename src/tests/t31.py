import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1400,'height':850})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.set_input_files('#inFolder','kit/Заказ'); await pg.wait_for_timeout(1200)
    await pg.locator('.tile', has_text='Корпус').click(); await pg.wait_for_timeout(1500)
    st="(()=>{const p=panes[0];return {cont:p.cont,n:p.pg.length,page:p.pageNo,base:p.pg.map(e=>!!e.base),z:(p.s/p.fitS).toFixed(2),fitted:p.fitted,cap:$('vPgNum')?$('vPgNum').textContent:''}})()"
    print('open:', await pg.evaluate(st))
    box=await pg.locator('#stage canvas').first.bounding_box(); await pg.mouse.move(box['x']+500,box['y']+400)
    for i in range(8): await pg.mouse.wheel(0,400); await pg.wait_for_timeout(60)
    await pg.wait_for_timeout(900); print('scrolled:', await pg.evaluate(st))
    await pg.keyboard.press('PageUp'); await pg.wait_for_timeout(600); print('pgup:', await pg.evaluate(st))
    # zoom in/out with ctrl, then fit -> no stale hi drawn
    await pg.keyboard.down('Control'); await pg.mouse.wheel(0,-600); await pg.wait_for_timeout(100); await pg.mouse.wheel(0,300); await pg.keyboard.up('Control'); await pg.wait_for_timeout(1200)
    print('zoomed:', await pg.evaluate(st))
    await pg.keyboard.press('f'); await pg.wait_for_timeout(1200)
    print('fit:', await pg.evaluate(st), await pg.evaluate("(()=>{const p=panes[0],e=p.pg[0];return [e.baseSc.toFixed(3),(p.s*p.dpr).toFixed(3)]})()"))
    await pg.evaluate("$('vCont').click()"); await pg.wait_for_timeout(1500); print('single mode:', await pg.evaluate(st))
    await pg.keyboard.press('PageDown'); await pg.wait_for_timeout(1200); print('pgdn:', await pg.evaluate(st))
    await pg.screenshot(path='t31.png')
    print('errors', errs); await b.close()
asyncio.run(main())
