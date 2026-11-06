import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1400,'height':850})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.set_input_files('#inFolder','cmp2/Заказ А'); await pg.wait_for_timeout(1500)
    await pg.set_input_files('#inCmp','cmp2/Архив'); await pg.wait_for_timeout(1500)
    print('bar:', await pg.inner_text('#cmpInfo'))
    await pg.locator('.tile', has_text='200001.001').locator('.cmpb').click(); await pg.wait_for_timeout(2000)
    print('pick visible', await pg.is_visible('#pickPanel'))
    for r in await pg.locator('#pickList .pk').all(): print('   ', (await r.inner_text()).replace('\n',' | '))
    await pg.screenshot(path='t41a.png')
    await pg.locator('#pickList .pk').first.click(); await pg.wait_for_timeout(2000)
    print('ov:', await pg.inner_text('#ovRes'), '|', await pg.inner_text('#ovNa'),'|', await pg.inner_text('#ovNb'))
    await pg.keyboard.press('Escape'); await pg.wait_for_timeout(500)
    await pg.keyboard.press('v'); await pg.wait_for_timeout(300)
    await pg.set_input_files('#pickInput','cmp2/Заказ Б/DXF/АБВГ.200001.002-Ст3-3-k1.dxf'); await pg.wait_for_timeout(2000)
    print('from disk:', await pg.inner_text('#ovRes'), '|', await pg.inner_text('#vName'))
    await pg.screenshot(path='t41b.png')
    print('errors',errs); await b.close()
asyncio.run(main())
