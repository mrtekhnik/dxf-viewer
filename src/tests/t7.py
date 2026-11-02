import asyncio,sys
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page()
    await pg.goto('file:///home/claude/dxf-viewer.html')
    for d in ('hg/a','hg/b'):
      await pg.set_input_files('#inFolder',d); await pg.wait_for_timeout(600)
      await pg.fill('#filter','Боковина'); await pg.wait_for_timeout(150); await pg.click('.tile'); await pg.wait_for_timeout(500)
      print(d, await pg.inner_text('#vPair'), await pg.get_attribute('#vPair','title')); await pg.keyboard.press('Escape')
    await b.close()
asyncio.run(main())
