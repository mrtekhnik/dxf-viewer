import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1300,'height':700})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.set_input_files('#inFolder','tree/Изделие 320'); await pg.wait_for_timeout(1500)
    await pg.click('#btnBrowse'); await pg.keyboard.press('ArrowRight'); await pg.keyboard.press('ArrowRight'); await pg.wait_for_timeout(800)
    await pg.screenshot(path='t33a.png')
    await pg.set_input_files('#inFiles',['dxf/деталь_01.pdf']); await pg.wait_for_timeout(2000)
    await pg.screenshot(path='t33b.png')
    print('errors',errs); await b.close()
asyncio.run(main())
