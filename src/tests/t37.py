import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1300,'height':800})
    await pg.add_init_script("try{const s=JSON.parse(localStorage.getItem('dxfv.set')||'{}');if(s.click===undefined){s.click='1';localStorage.setItem('dxfv.set',JSON.stringify(s))}}catch(e){}")
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.set_input_files('#inFolder','tree/Изделие 320'); await pg.wait_for_timeout(1500)
    print('lv', await pg.evaluate('[SET.pdfLv,pdfFilter()]'))
    st="[VW.idx,view.length,VW.set.length?VW.set[0].name:'']"
    await pg.click('#btnPreview'); await pg.wait_for_timeout(600)
    await pg.keyboard.press('End'); await pg.wait_for_timeout(500); print('dock End', await pg.evaluate(st))
    await pg.keyboard.press('Home'); await pg.wait_for_timeout(500); print('dock Home', await pg.evaluate(st))
    await pg.click('#btnPreview'); await pg.wait_for_timeout(500)
    await pg.keyboard.press('End'); await pg.wait_for_timeout(300); print('grid End', await pg.evaluate("[...document.querySelectorAll('#grid .tile.cur')].map(t=>t._it&&t._it.name)"))
    print('errors',errs); await b.close()
asyncio.run(main())
