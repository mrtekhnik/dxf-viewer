import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1400,'height':850})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.set_input_files('#inFolder','cmp2/Заказ А'); await pg.wait_for_timeout(1500)
    await pg.evaluate("SET.layout='list';applyLayout&&applyLayout()") if await pg.evaluate("typeof applyLayout==='function'") else None
    await pg.locator('.tile', has_text='200001.003').click(); await pg.wait_for_timeout(700)
    print('after click: full',await pg.evaluate('VW.full'),'cur', await pg.evaluate("[...document.querySelectorAll('.tile.cur')].map(t=>t._it&&t._it.name)"), 'idx',await pg.evaluate('VW.idx'))
    if await pg.evaluate('VW.full'): await pg.keyboard.press('Escape'); await pg.wait_for_timeout(400)
    print('after esc cur', await pg.evaluate("[...document.querySelectorAll('.tile.cur')].map(t=>t._it&&t._it.name)"), await pg.evaluate('VW.idx'))
    await pg.set_input_files('#inCmp','cmp2/Заказ Б'); await pg.wait_for_timeout(2500)
    print('full',await pg.evaluate('VW.full'),'set',await pg.evaluate('VW.set.map(x=>x.name)'))
    print('errors',errs); await b.close()
asyncio.run(main())
