import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1400,'height':850})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.set_input_files('#inFolder','cmp3/A'); await pg.wait_for_timeout(1500)
    await pg.set_input_files('#inCmp','cmp3/B/PDF_DXF 2'); await pg.wait_for_timeout(2500)
    print('bar:', await pg.inner_text('#cmpInfo'), '|', await pg.inner_text('#cmpOnlyBtn'))
    for t in await pg.locator('.tile').all():
      if await t.locator('.cmpb').count(): print('  ', (await t.locator('.nm').inner_text()), '→', await t.locator('.cmpb').inner_text(), '|', await t.locator('.cmpb').get_attribute('title'))
    print('errors',errs); await b.close()
asyncio.run(main())
