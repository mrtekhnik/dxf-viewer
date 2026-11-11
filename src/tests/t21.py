import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1300,'height':800})
    await pg.add_init_script("try{const s=JSON.parse(localStorage.getItem('dxfv.set')||'{}');if(s.click===undefined){s.click='1';localStorage.setItem('dxfv.set',JSON.stringify(s))}}catch(e){}")
    await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.set_input_files('#inFolder','tree/Изделие 320'); await pg.wait_for_timeout(1500)
    t=pg.locator('.tile').nth(3); bb=await t.bounding_box(); await pg.mouse.move(bb['x']+50,bb['y']+50); await pg.wait_for_timeout(100)
    await pg.keyboard.press('ArrowRight'); await pg.keyboard.press('ArrowRight'); await pg.wait_for_timeout(150)
    bc=lambda i: pg.locator('.tile').nth(i).evaluate("e=>getComputedStyle(e).borderColor")
    print('hovered while kbd:', await bc(3), '| selected:', await bc(1))
    await pg.mouse.move(bb['x']+60,bb['y']+60); await pg.wait_for_timeout(100); print('hover after mouse move:', await bc(3))
    await b.close()
asyncio.run(main())
