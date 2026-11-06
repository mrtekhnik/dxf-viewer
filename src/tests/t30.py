import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1200,'height':800})
    await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.set_input_files('#inFolder','kit/Заказ'); await pg.wait_for_timeout(1500)
    await pg.locator('.tile', has_text='Общий').click(); await pg.wait_for_timeout(2000)
    st="(()=>{const p=panes[0];return {z:(p.s/p.fitS).toFixed(2),fitted:p.fitted,W:p.W,H:p.H,base:p.pg[0].baseSc.toFixed(3),mid:(p.pg[0].midSc||0).toFixed(3)}})()"
    print('open', await pg.evaluate(st))
    r=await pg.evaluate("(()=>{const p=panes[0];const L=p.W/2-p.cx*p.s,T=p.H/2-(p.ph-p.cy)*p.s;const c=p.cv.getBoundingClientRect();return [c.x+L,c.y+T]})()")
    await pg.mouse.move(r[0]+2,r[1]+2)
    for i in range(8): await pg.mouse.wheel(0,-300); await pg.wait_for_timeout(50)
    print('after wheel', await pg.evaluate(st))
    await pg.wait_for_timeout(1500); print('after 1.5s', await pg.evaluate(st))
    await pg.screenshot(path='edge2.png'); await b.close()
asyncio.run(main())
