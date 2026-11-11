import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1400,'height':850})
    await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.set_input_files('#inFolder','kit/Заказ'); await pg.wait_for_timeout(1200)
    await pg.locator('.tile', has_text='Корпус').click(); await pg.wait_for_timeout(1500)
    q="(()=>{const p=panes[0],e=p.pg[0];return [p.W,p.H,p.pw,p.ph,e.w,e.h,e.baseSc,p.s*p.dpr,p.fitS*p.dpr,p.dpr]})()"
    print(await pg.evaluate(q))
    await pg.keyboard.press('f'); await pg.wait_for_timeout(1000); print(await pg.evaluate(q))
    await b.close()
asyncio.run(main())
