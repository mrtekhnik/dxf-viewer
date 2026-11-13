import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); ctx=await b.new_context(viewport={'width':1400,'height':850},accept_downloads=True); pg=await ctx.new_page()
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.set_input_files('#inFiles',['blk/rot_sheet.pdf','blk/normal_sheet.pdf','cmp2/Заказ А/DXF/АБВГ.200001.003-Ст3-3-k1.dxf']); await pg.wait_for_timeout(1500)
    await pg.locator('.tile', has_text='rot_sheet').dblclick(); await pg.wait_for_timeout(2500)
    print('rot: suggest', await pg.evaluate('panes[0].sugRot'), 'btn visible', await pg.is_visible('#vPdfRot'), 'title', await pg.get_attribute('#vPdfRot','title'))
    await pg.screenshot(path='t56a.png')
    await pg.click('#vPdfRot'); await pg.wait_for_timeout(2000); print('after: prot', await pg.evaluate('panes[0].prot'), 'pw,ph', await pg.evaluate('[Math.round(panes[0].pw),Math.round(panes[0].ph)]'), 'btn', await pg.is_visible('#vPdfRot'))
    await pg.screenshot(path='t56b.png')
    await pg.keyboard.press('ArrowRight'); await pg.wait_for_timeout(1800); print('normal: suggest', await pg.evaluate('panes[0].sugRot'), 'btn', await pg.is_visible('#vPdfRot'))
    await pg.keyboard.press('Shift+F'); await pg.wait_for_timeout(800); print('fitW s*pw/W', await pg.evaluate('(panes[0].s*panes[0].pw/panes[0].W).toFixed(3)'))
    # лупа
    bb=await pg.locator('#stage canvas').first.bounding_box(); await pg.mouse.move(bb['x']+300,bb['y']+200)
    await pg.keyboard.down('z'); await pg.mouse.move(bb['x']+320,bb['y']+210); await pg.wait_for_timeout(600); print('loupe visible', await pg.is_visible('#loupe'))
    await pg.screenshot(path='t56c.png'); await pg.keyboard.up('z'); await pg.wait_for_timeout(100); print('loupe after up', await pg.is_visible('#loupe'))
    await pg.keyboard.press('ArrowRight'); await pg.wait_for_timeout(1200)
    await pg.click('#vLoupe'); await pg.mouse.move(bb['x']+400,bb['y']+300); await pg.mouse.down(); await pg.wait_for_timeout(200); print('boost', await pg.evaluate('LOUPE.boost')); await pg.screenshot(path='t56d.png'); await pg.mouse.up(); await pg.click('#vLoupe')
    # PNG
    await pg.click('#vPng'); await pg.wait_for_timeout(200)
    async with pg.expect_download() as dl: await pg.click('#pngGo')
    d=await dl.value; print('png', d.suggested_filename); await d.save_as('t56.png')
    print('errors',errs); await b.close()
asyncio.run(main())
