import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
    for w in [1920,1700,1600,1440,1366,1280,1100,900]:
      pg=await b.new_page(viewport={'width':w,'height':500})
      await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.set_input_files('#inFolder','tree/Изделие 320'); await pg.wait_for_timeout(900)
      print(w,await pg.evaluate("document.querySelector('header').offsetHeight"), await pg.evaluate("[...document.querySelectorAll('header .grp')].map(g=>g.offsetWidth).join(' ')"))
      await pg.screenshot(path=f't47_{w}.png',clip={'x':0,'y':0,'width':w,'height':110}); await pg.close()
    await b.close()
asyncio.run(main())
