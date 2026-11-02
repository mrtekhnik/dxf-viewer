import asyncio, glob
from playwright.async_api import async_playwright
async def info(pg):
  name=(await pg.inner_text('#vName')).split('· ')[-1]; return name, await pg.inner_text('#vPair')
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1280,'height':800})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file:///home/claude/dxf-viewer.html')
    await pg.set_input_files('#inFiles',sorted(glob.glob('pair/*.pdf')+glob.glob('pair/DXF/*.dxf'))); await pg.wait_for_timeout(1500)
    n=await pg.locator('.tile').count()
    for i in range(n):
      await pg.locator('.tile').nth(i).click(); await pg.wait_for_timeout(400)
      print('%-40s %s'%await info(pg)); await pg.keyboard.press('Escape'); await pg.wait_for_timeout(150)
    # executions panel + Tab memory
    await pg.fill('#filter','Корпус'); await pg.wait_for_timeout(200); await pg.click('.tile'); await pg.wait_for_timeout(600)
    await pg.click('#vPairMenu'); await pg.wait_for_timeout(300); print('PANEL:\n'+await pg.inner_text('#ppLinked'))
    await pg.screenshot(path='panel.png')
    await pg.locator('#ppLinked .pp-name').nth(1).click(); await pg.wait_for_timeout(600); print('chose', await info(pg))
    await pg.keyboard.press('Tab'); await pg.wait_for_timeout(600); print('tab', await info(pg))
    await pg.keyboard.press('Tab'); await pg.wait_for_timeout(600); print('tab back', await info(pg))
    # manual link for mess
    await pg.keyboard.press('Escape'); await pg.fill('#filter','Кронштейн старый'); await pg.wait_for_timeout(200); await pg.click('.tile'); await pg.wait_for_timeout(600)
    print('mess', await info(pg)); await pg.click('#vPairMenu'); await pg.wait_for_timeout(300)
    print('list top3:', (await pg.inner_text('#ppList')).split('\n')[:3])
    await pg.locator('#ppList .pp-c', has_text='kronsht').click(); await pg.wait_for_timeout(600); print('linked ->', await info(pg))
    await pg.reload(); await pg.set_input_files('#inFiles',sorted(glob.glob('pair/*.pdf')+glob.glob('pair/DXF/*.dxf'))); await pg.wait_for_timeout(800)
    await pg.fill('#filter','kronsht'); await pg.wait_for_timeout(200); await pg.click('.tile'); await pg.wait_for_timeout(500); print('after reload', await info(pg))
    print(errs); await b.close()
asyncio.run(main())
