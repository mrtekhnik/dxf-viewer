import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
    for w in [1920,1600,1366,1100,400]:
      pg=await b.new_page(viewport={'width':w,'height':500}); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
      await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.set_input_files('#inFolder','tree/Изделие 320'); await pg.wait_for_timeout(1200)
      if w==1920: await pg.click('#btnOpen'); await pg.wait_for_timeout(200)
      print(w,'header h',await pg.evaluate("document.querySelector('header').offsetHeight"),errs)
      await pg.screenshot(path=f't47_{w}.png',clip={'x':0,'y':0,'width':w,'height':170})
    await b.close()
asyncio.run(main())
