import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1400,'height':850})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    for folder,label in [('cmp2/Заказ Б','pair'),('cmp2/Архив','renamed')]:
      await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.set_input_files('#inFolder','cmp2/Заказ А'); await pg.wait_for_timeout(1500)
      for _ in range(3): await pg.keyboard.press('ArrowRight')
      await pg.set_input_files('#inCmp',folder); await pg.wait_for_timeout(2500)
      print(label,'| full',await pg.evaluate('VW.full'),'| set',await pg.evaluate('VW.set.map(x=>x.name)'),'| ov',await pg.inner_text('#ovRes') if await pg.is_visible('#ovRes') else '-','| pick',await pg.is_visible('#pickPanel'))
    await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.set_input_files('#inFolder','cmp2/Заказ А'); await pg.wait_for_timeout(1500)
    await pg.keyboard.press('ArrowRight'); await pg.keyboard.press('v'); await pg.wait_for_timeout(800); print('V in grid: pick',await pg.is_visible('#pickPanel'))
    print('errors',errs); await b.close()
asyncio.run(main())
