import asyncio,glob
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':900,'height':600})
    await pg.add_init_script("try{const s=JSON.parse(localStorage.getItem('dxfv.set')||'{}');if(s.click===undefined){s.click='1';localStorage.setItem('dxfv.set',JSON.stringify(s))}}catch(e){}")
    await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.set_input_files('#inFiles',sorted(glob.glob('sp/*.dxf'))); await pg.wait_for_timeout(1500)
    n=await pg.locator('.tile').count()
    for i in range(n):
      await pg.locator('.tile').nth(i).click(); await pg.wait_for_timeout(400)
      print((await pg.inner_text('#vName')).split('· ')[-1], await pg.inner_text('#vDims'), '|warn:',await pg.is_visible('#vWarn'))
      await pg.keyboard.press('Escape'); await pg.wait_for_timeout(100)
    await pg.screenshot(path='sp.png'); await b.close()
asyncio.run(main())
