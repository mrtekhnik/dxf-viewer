import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1300,'height':800})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.set_input_files('#inFolder','tree/Изделие 320'); await pg.wait_for_timeout(1500)
    st="(()=>({dir:curDir,zone:KB.zone,tiles:[...$('grid').children].map(t=>(t.classList.contains('cur')?'*':'')+(t._it?t._it.name:'['+t.querySelector('.nm').textContent+']')).slice(0,8),full:VW.full}))()"
    print('dbg', await pg.evaluate('[HASSUB,!!TREE_ROOT,items.length,$("btnTree").hidden]')); await pg.click('#btnBrowse'); await pg.wait_for_timeout(300); print('folders:', await pg.evaluate(st))
    await pg.keyboard.press('ArrowRight'); print('→', await pg.evaluate(st))
    await pg.keyboard.press('Enter'); await pg.wait_for_timeout(300); print('enter', await pg.evaluate(st))
    await pg.keyboard.press('ArrowDown'); await pg.keyboard.press('Enter'); await pg.wait_for_timeout(300); print('enter2', await pg.evaluate(st)); await pg.keyboard.press('Escape'); await pg.wait_for_timeout(300)
    await pg.keyboard.press('Backspace'); await pg.wait_for_timeout(300); print('bksp', await pg.evaluate(st))
    await pg.keyboard.press('ArrowLeft'); await pg.keyboard.press('ArrowLeft'); await pg.wait_for_timeout(200); print('← to tree', await pg.evaluate(st))
    await pg.keyboard.press('ArrowDown'); await pg.wait_for_timeout(200); print('tree ↓', await pg.evaluate(st))
    await pg.keyboard.press('ArrowRight'); await pg.wait_for_timeout(200); print('tree →', await pg.evaluate(st))
    await pg.keyboard.press('End'); await pg.wait_for_timeout(200); print('tree End', await pg.evaluate(st))
    await pg.keyboard.press('Backspace'); await pg.wait_for_timeout(200); print('tree Bksp', await pg.evaluate(st))
    await pg.keyboard.press('Enter'); await pg.wait_for_timeout(200); print('tree Enter', await pg.evaluate(st))
    await pg.click('#btnBrowse'); await pg.wait_for_timeout(300); print('all:', await pg.evaluate(st))
    await pg.screenshot(path='t32.png')
    print('errors', errs); await b.close()
asyncio.run(main())
