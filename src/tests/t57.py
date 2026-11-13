import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); ctx=await b.new_context(viewport={'width':1400,'height':850},accept_downloads=True); pg=await ctx.new_page()
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.set_input_files('#inFolder','kit/Заказ'); await pg.wait_for_timeout(1500)
    await pg.locator('.tile', has_text='002 Корпус').dblclick(); await pg.wait_for_timeout(2500)
    print('normal pdf suggest', await pg.evaluate('panes[0].sugRot'), await pg.is_visible('#vPdfRot'))
    await pg.keyboard.press('Shift+F'); await pg.wait_for_timeout(800); print('fitW ratio', await pg.evaluate('(panes[0].s*(panes[0].curPage().w)/panes[0].W).toFixed(3)'))
    bb=await pg.locator('#stage canvas').first.bounding_box()
    await pg.mouse.move(bb['x']+700,bb['y']+300); await pg.keyboard.down('z'); await pg.mouse.move(bb['x']+710,bb['y']+305); await pg.wait_for_timeout(900); await pg.screenshot(path='t57a.png'); await pg.keyboard.up('z')
    await pg.keyboard.press('r'); await pg.wait_for_timeout(1500); print('side set', await pg.evaluate('VW.set.map(x=>x.name)'))
    await pg.click('#vPng'); await pg.locator('#pngOnlyDxf').check()
    async with pg.expect_download() as dl: await pg.click('#pngGo')
    d=await dl.value; print('png', d.suggested_filename); await d.save_as('t57.png')
    print('errors',errs); await b.close()
asyncio.run(main())
