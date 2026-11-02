import asyncio, glob
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--allow-file-access-from-files'])
    pg=await b.new_page(viewport={'width':1280,'height':800})
    errs=[]; pg.on('console',lambda m: errs.append(m.type+': '+m.text) if m.type in('error','warning') else None); pg.on('pageerror',lambda e: errs.append('PAGEERR '+str(e)))
    await pg.goto('file:///home/claude/dxf-viewer.html')
    files=sorted(glob.glob('dxf/*.dxf'))
    await pg.set_input_files('#inFiles',files)
    await pg.wait_for_timeout(4000)
    print(await pg.inner_text('#status'))
    await pg.screenshot(path='grid.png')
    await pg.click('#btnLog'); await pg.click('#logAll'); await pg.wait_for_timeout(6000)
    print(await pg.inner_text('#status'))
    print(await pg.inner_text('#logBody'))
    await pg.click('#logClose')
    for name in ['деталь_01.dxf','деталь_02_R12.dxf','деталь_03_extrusion.dxf','большой_60k.dxf']:
      await pg.fill('#filter',name); await pg.wait_for_timeout(200)
      await pg.click('.tile'); await pg.wait_for_timeout(1500)
      print(name, await pg.inner_text('.vinfo'))
      await pg.screenshot(path='v_'+name+'.png')
      await pg.keyboard.press('Escape'); await pg.wait_for_timeout(300)
    # zoom + nav test
    await pg.fill('#filter',''); await pg.wait_for_timeout(200)
    await pg.click('.tile'); await pg.wait_for_timeout(800)
    await pg.mouse.move(640,400); await pg.mouse.wheel(0,-600); await pg.wait_for_timeout(200)
    await pg.keyboard.press('ArrowRight'); await pg.wait_for_timeout(800)
    print(await pg.inner_text('#vName'))
    print('ERRS',errs)
    await b.close()
asyncio.run(main())
