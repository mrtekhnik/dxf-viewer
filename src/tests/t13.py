import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
    pg=await b.new_page(viewport={'width':1200,'height':800})
    await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.set_input_files('#inFolder','kit/Заказ'); await pg.wait_for_timeout(1500)
    await pg.locator('.tile', has_text='Общий').click(); await pg.wait_for_timeout(2000)
    # zoom into the top-left corner of the sheet so that both page and outside area are visible
    r=await pg.evaluate("(()=>{const p=panes[0];const L=p.W/2-p.cx*p.s,T=p.H/2-(p.ph-p.cy)*p.s;const c=p.cv.getBoundingClientRect();return [c.x+L,c.y+T]})()")
    await pg.mouse.move(r[0]+2,r[1]+2)
    for i in range(8): await pg.mouse.wheel(0,-300); await pg.wait_for_timeout(50)
    await pg.wait_for_timeout(1500)
    info=await pg.evaluate("""(()=>{const p=panes[0],d=p.dpr;const L=p.W/2-p.cx*p.s,T=p.H/2-(p.ph-p.cy)*p.s;const g=(x,y)=>[...p.ctx.getImageData(Math.round(x*d),Math.round(y*d),1,1).data].slice(0,3);
      return {hi:!!p.pg[0].hi, outside:g(Math.max(2,L-20),Math.max(2,T-20)), inside:g(L+5,T+5)}})()""")
    print(info); await pg.screenshot(path='s_edge.png')
    # phone portrait side mode
    pg2=await b.new_page(viewport={'width':390,'height':800},is_mobile=True,has_touch=True,device_scale_factor=2)
    await pg2.goto('file:///home/claude/dxf-viewer.html'); await pg2.set_input_files('#inFiles',[f'kit/Заказ/{n}' for n in ['АБВГ.123456.002 Корпус.pdf']]+[f'kit/Заказ/DXF/{n}' for n in ['АБВГ.123456.002-08пс-2-k1.dxf','АБВГ.123456.002-01-08пс-2-k1.dxf']])
    await pg2.wait_for_timeout(1500); await pg2.locator('.tile').first.tap(); await pg2.wait_for_timeout(1200)
    await pg2.tap('#vSide'); await pg2.wait_for_timeout(2500); await pg2.screenshot(path='s_phone_side.png')
    await b.close()
asyncio.run(main())
