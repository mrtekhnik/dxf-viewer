import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1400,'height':800})
    await pg.add_init_script("try{const s=JSON.parse(localStorage.getItem('dxfv.set')||'{}');if(s.click===undefined){s.click='1';localStorage.setItem('dxfv.set',JSON.stringify(s))}}catch(e){}")
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.set_input_files('#inFolder','inv/СК Рама'); await pg.wait_for_timeout(1500)
    await pg.locator('.tile', has_text='Профіль').click(); await pg.wait_for_timeout(800)
    print('pair btn:', await pg.inner_text('#vPair'))
    await pg.keyboard.press('r'); await pg.wait_for_timeout(2000)
    caps=await pg.locator('#stage .pcap').all_inner_texts(); print('panes', len(caps)); [print('  ',c.replace('\n',' | ')) for c in caps]
    print('dup title:', await pg.locator('.pcap .dup').first.get_attribute('title'))
    print('dims bar:', await pg.inner_text('#vDims'))
    await pg.screenshot(path='caps.png')
    await pg.keyboard.press('r'); await pg.keyboard.press('Escape')
    await pg.click('#btnSet'); await pg.wait_for_timeout(200); print('capV:', (await pg.inner_text('#capV')).replace('\n',' | '))
    print('errors', errs); await b.close()
asyncio.run(main())
