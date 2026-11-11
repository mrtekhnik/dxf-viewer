import asyncio
from playwright.async_api import async_playwright
async def state(pg):
  out=[]
  for z in ('З1','З2','З3'):
    await pg.fill('#filter',z+'/dxf/kronsht'); await pg.wait_for_timeout(150)
    if await pg.locator('.tile').count()==0: out.append(z+':нет'); continue
    await pg.click('.tile'); await pg.wait_for_timeout(400)
    out.append(z+':'+await pg.inner_text('#vPair')); await pg.keyboard.press('Escape'); await pg.wait_for_timeout(150)
  return out
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1280,'height':800})
    await pg.add_init_script("try{const s=JSON.parse(localStorage.getItem('dxfv.set')||'{}');if(s.click===undefined){s.click='1';localStorage.setItem('dxfv.set',JSON.stringify(s))}}catch(e){}")
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file:///home/claude/dxf-viewer.html')
    await pg.set_input_files('#inFolder','orders'); await pg.wait_for_timeout(800)
    print('files:', await pg.inner_text('#status'))
    await pg.fill('#filter','З1/dxf/kronsht'); await pg.wait_for_timeout(150); await pg.click('.tile'); await pg.wait_for_timeout(400)
    await pg.click('#vPair'); await pg.wait_for_timeout(200); await pg.fill('#ppSearch','З1'); await pg.wait_for_timeout(150)
    await pg.locator('#ppList .pp-c').first.click(); await pg.wait_for_timeout(400)
    await pg.keyboard.press('Escape'); await pg.wait_for_timeout(150)
    print('folder mode:', await state(pg))
    await pg.fill('#filter','З1/dxf/kronsht'); await pg.click('.tile'); await pg.wait_for_timeout(400); await pg.click('#vPairMenu')
    await pg.select_option('#ppMode','size'); await pg.keyboard.press('Escape'); await pg.keyboard.press('Escape'); await pg.wait_for_timeout(200)
    print('size mode:', await state(pg))
    await pg.fill('#filter','З1/dxf/kronsht'); await pg.click('.tile'); await pg.wait_for_timeout(400); await pg.click('#vPairMenu')
    await pg.select_option('#ppMode','folder'); await pg.keyboard.press('Escape'); await pg.keyboard.press('Escape')
    await pg.reload(); await pg.set_input_files('#inFolder','orders/З1'); await pg.wait_for_timeout(600)
    await pg.click('.tile >> nth=1'); await pg.wait_for_timeout(400); print('reopen only З1:', await pg.inner_text('#vName'), await pg.inner_text('#vPair'))
    print(errs); await b.close()
asyncio.run(main())
