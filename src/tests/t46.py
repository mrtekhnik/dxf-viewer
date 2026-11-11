import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1400,'height':850})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.set_input_files('#inFolder','kit/Заказ'); await pg.wait_for_timeout(1500)
    t=pg.locator('.tile', has_text='002 Корпус')
    await t.click(); await pg.wait_for_timeout(400); print('1 click: full',await pg.evaluate('VW.full'),'cur',await pg.evaluate("[...document.querySelectorAll('.tile.cur')].map(t=>t._it.name)"))
    await t.dblclick(); await pg.wait_for_timeout(1200); print('dbl: full',await pg.evaluate('VW.full'),await pg.evaluate('VW.set.map(x=>x.name)'))
    await pg.keyboard.press('Escape'); await pg.wait_for_timeout(500)
    await pg.keyboard.press('Tab'); await pg.wait_for_timeout(1500); print('Tab: ',await pg.evaluate('VW.full'),await pg.evaluate('VW.set.map(x=>x.name)'))
    await pg.keyboard.press('Escape'); await pg.wait_for_timeout(500)
    await pg.click('#btnSideG'); await pg.wait_for_timeout(1500); print('Рядом:',await pg.evaluate('VW.set.map(x=>x.name)'))
    await pg.keyboard.press('Escape'); await pg.wait_for_timeout(500); await pg.evaluate('SET.side=false')
    await pg.keyboard.press('F1'); await pg.wait_for_timeout(400); print('help', await pg.is_visible('#helpPanel'), await pg.locator('#helpNav a').count())
    await pg.fill('#helpQ','мигание'); await pg.wait_for_timeout(300); print('found sections', await pg.locator('#helpBody section:not(.hid)').count(), await pg.locator('#helpBody mark').count())
    await pg.screenshot(path='t46.png')
    await pg.keyboard.press('Escape'); await pg.wait_for_timeout(200); print('help closed', not await pg.is_visible('#helpPanel'), 'full',await pg.evaluate('VW.full'))
    print('errors',errs); await b.close()
asyncio.run(main())
