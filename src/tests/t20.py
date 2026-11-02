import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1300,'height':850})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.set_input_files('#inFiles',['real/r1.dxf']); await pg.wait_for_timeout(2500)
    await pg.screenshot(path='r1_all.png')
    # zoom to the multileader area: original coords around (-100, 110)
    await pg.evaluate("""(()=>{const p=panes[0],o=p.doc.origin;p.cx=-100-o[0];p.cy=110-o[1];p.s=p.fitS*9;p.draw();})()""")
    await pg.wait_for_timeout(500); await pg.screenshot(path='r1_zoom.png')
    print(await pg.evaluate("items[0].log.map(l=>l[1]).join(' | ')"), errs); await b.close()
asyncio.run(main())
