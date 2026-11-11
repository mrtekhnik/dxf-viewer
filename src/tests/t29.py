import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1400,'height':850})
    await pg.add_init_script("try{const s=JSON.parse(localStorage.getItem('dxfv.set')||'{}');if(s.click===undefined){s.click='1';localStorage.setItem('dxfv.set',JSON.stringify(s))}}catch(e){}")
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.set_input_files('#inFiles',['dxf/тяжёлый_1.pdf']); await pg.wait_for_timeout(3500)
    await pg.screenshot(path='bold0.png',clip={'x':400,'y':300,'width':400,'height':250})
    await pg.evaluate("SET.pdfBold=true;panes[0].draw()"); await pg.wait_for_timeout(400)
    await pg.screenshot(path='bold1.png',clip={'x':400,'y':300,'width':400,'height':250})
    print('errors',errs); await b.close()
asyncio.run(main())
