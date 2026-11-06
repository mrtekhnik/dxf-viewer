import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1400,'height':850})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e))); pg.on('console',lambda m: errs.append('console:'+m.text) if m.type=='error' else None)
    await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.set_input_files('#inFolder','cmp2/Заказ А'); await pg.wait_for_timeout(1500)
    await pg.set_input_files('#inCmp','cmp2/Заказ Б'); await pg.wait_for_timeout(3000)
    print('bar:', await pg.inner_text('#cmpInfo'))
    for t in await pg.locator('.tile').all(): print('  ', (await t.locator('.nm').inner_text()), '→', await t.locator('.cmpb').inner_text(), '|', await t.locator('.cmpb').get_attribute('title'))
    await pg.select_option('#cmpFilter','chg'); await pg.wait_for_timeout(200); print('filter chg:', await pg.locator('#grid .tile').count()); await pg.select_option('#cmpFilter','')
    await pg.locator('.tile', has_text='200001.003').locator('.cmpb').click(); await pg.wait_for_timeout(1200)
    print('vOv visible', await pg.is_visible('#vOv'))
    await pg.click('#vOv'); await pg.wait_for_timeout(2000)
    print('ov:', await pg.inner_text('#ovRes'), '|', await pg.inner_text('#ovNum'), '| panes', await pg.evaluate('VW.set.length'))
    await pg.screenshot(path='t40a.png')
    await pg.keyboard.press('.'); await pg.wait_for_timeout(300); print('next diff', await pg.inner_text('#ovNum'))
    await pg.screenshot(path='t40b.png')
    await pg.keyboard.press('ArrowRight'); await pg.wait_for_timeout(2000); print('→ next pair:', await pg.inner_text('#vName'), '|', await pg.inner_text('#ovRes'))
    # ручной сдвиг Shift+перетаскивание
    box=await pg.locator('#stage canvas').first.bounding_box()
    await pg.keyboard.down('Shift'); await pg.mouse.move(box['x']+600,box['y']+400); await pg.mouse.down(); await pg.mouse.move(box['x']+640,box['y']+420,steps=5); await pg.mouse.up(); await pg.keyboard.up('Shift')
    await pg.wait_for_timeout(1500); print('after manual move:', await pg.inner_text('#ovRes'))
    await pg.click('#ovAuto'); await pg.wait_for_timeout(1500); print('after auto:', await pg.inner_text('#ovRes'))
    await pg.keyboard.press('Escape'); await pg.wait_for_timeout(800); print('esc -> panes', await pg.evaluate('VW.set.length'), await pg.is_visible('#ovBar'))
    print('errors',errs); await b.close()
asyncio.run(main())
