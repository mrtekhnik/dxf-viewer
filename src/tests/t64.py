import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page()
    await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.set_input_files('#inFiles',['cmp2/Заказ А/DXF/АБВГ.200001.003-Ст3-3-k1.dxf','cmp2/Заказ А/DXF/АБВГ.200001.002-Ст3-3-k1.dxf']); await pg.wait_for_timeout(800)
    msgs=[]
    pg.once('dialog',lambda d:(msgs.append(d.message),asyncio.ensure_future(d.dismiss())))
    await pg.click('#btnClose'); await pg.wait_for_timeout(300); print('cancel -> items',await pg.evaluate('items.length'),msgs)
    pg.once('dialog',lambda d:asyncio.ensure_future(d.accept()))
    await pg.click('#btnClose'); await pg.wait_for_timeout(300); print('ok -> items',await pg.evaluate('items.length'))
    await b.close()
asyncio.run(main())
