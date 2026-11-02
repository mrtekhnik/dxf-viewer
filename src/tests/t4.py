import asyncio, glob
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page()
    await pg.goto('file:///home/claude/dxf-viewer.html')
    fs=sorted(glob.glob('pair/*.pdf')+glob.glob('pair/DXF/*.dxf'))
    await pg.set_input_files('#inFiles',fs); await pg.wait_for_timeout(1500)
    n=await pg.locator('.tile').count()
    for i in range(n):
      await pg.locator('.tile').nth(i).click(); await pg.wait_for_timeout(500)
      name=(await pg.inner_text('#vName')).split('· ')[-1]
      pr=await pg.get_attribute('#vPair','title') if await pg.is_visible('#vPair') else '—'
      print(f'{name:40s} -> {pr}')
      await pg.keyboard.press('Escape'); await pg.wait_for_timeout(200)
    await b.close()
asyncio.run(main())
