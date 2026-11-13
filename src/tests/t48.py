import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1400,'height':800})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.set_input_files('#inFolder','kit/Заказ'); await pg.wait_for_timeout(1500)
    print('bar:', (await pg.inner_text('#mtBar')).replace('\n',' | '))
    await pg.locator('#mtBar .mt-c').nth(1).click(); await pg.wait_for_timeout(300); print('filtered:', await pg.evaluate('view.map(x=>x.name)'))
    await pg.locator('#mtBar .mt-c').nth(0).click(); await pg.locator('#mtBar input').check(); await pg.wait_for_timeout(300); print('sorted:', await pg.evaluate('view.map(x=>x.name)'))
    await pg.screenshot(path='t48.png',clip={'x':0,'y':0,'width':1400,'height':260})
    print('errors',errs); await b.close()
asyncio.run(main())
