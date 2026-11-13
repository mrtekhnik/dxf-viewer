import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1400,'height':850})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.set_input_files('#inFolder','kit/Заказ'); await pg.wait_for_timeout(1500)
    await pg.locator('.tile', has_text='002-08пс').dblclick(); await pg.wait_for_timeout(1500)
    await pg.click('#vLoupe'); bb=await pg.locator('#stage canvas').first.bounding_box(); await pg.mouse.move(bb['x']+500,bb['y']+300); await pg.wait_for_timeout(300)
    print('loupe', await pg.is_visible('#loupe'), await pg.evaluate("$('loupe').style.width"), 'pane title', await pg.evaluate("panes[0].el.title"))
    await pg.keyboard.press('Escape'); await pg.wait_for_timeout(200); print('esc1 loupe', await pg.is_visible('#loupe'), 'full', await pg.evaluate('VW.full'))
    await pg.click('#vLoupe'); await pg.mouse.move(bb['x']+520,bb['y']+300); await pg.wait_for_timeout(200)
    await pg.click('#vClose') if await pg.is_visible('#vClose') else await pg.evaluate('setFull(false)')
    await pg.wait_for_timeout(300); print('after close loupe', await pg.is_visible('#loupe'), 'on', await pg.evaluate('LOUPE.on'))
    print('errors',errs); await b.close()
asyncio.run(main())
