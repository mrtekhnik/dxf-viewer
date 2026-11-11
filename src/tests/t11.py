import asyncio, glob
from playwright.async_api import async_playwright
async def name(pg): return (await pg.inner_text('#vName')).split('· ')[-1]
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1400,'height':850})
    await pg.add_init_script("try{const s=JSON.parse(localStorage.getItem('dxfv.set')||'{}');if(s.click===undefined){s.click='1';localStorage.setItem('dxfv.set',JSON.stringify(s))}}catch(e){}")
    errs=[]; pg.on('pageerror',lambda e: errs.append('PAGEERR '+str(e))); pg.on('console',lambda m: errs.append(m.text[:200]) if m.type=='error' else None)
    await pg.goto('file:///home/claude/dxf-viewer.html')
    await pg.set_input_files('#inFolder','kit/Заказ'); await pg.wait_for_timeout(2500)
    print('status:', await pg.inner_text('#status'))
    # 1 grid -> click PDF -> Tab cycle
    await pg.locator('.tile', has_text='Корпус').click(); await pg.wait_for_timeout(1500)
    seq=[await name(pg)+' | '+await pg.inner_text('#vPair')]
    for i in range(4):
      await pg.keyboard.press('Tab'); await pg.wait_for_timeout(700); seq.append(await name(pg)+' | '+await pg.inner_text('#vPair'))
    print('TAB:'); [print('  ',s) for s in seq]
    await pg.keyboard.press('Shift+Tab'); await pg.wait_for_timeout(600); print('shift-tab:', await name(pg))
    # 2 side mode
    await pg.keyboard.press('r'); await pg.wait_for_timeout(2500)
    print('side panes:', await pg.locator('#stage .pane').count(), '| caps:', await pg.locator('#stage .pcap').all_inner_texts())
    await pg.screenshot(path='s_side.png')
    await pg.keyboard.press('ArrowRight'); await pg.wait_for_timeout(2000)
    print('next set panes:', await pg.locator('#stage .pane').count(), await pg.locator('#stage .pcap').all_inner_texts())
    await pg.screenshot(path='s_side2.png')
    await pg.keyboard.press('r'); await pg.wait_for_timeout(400)
    await pg.keyboard.press('Escape'); await pg.wait_for_timeout(400)
    print('viewer hidden after esc:', await pg.is_hidden('#viewer'))
    # 3 explorer mode
    await pg.evaluate("$(SET.layout==='list'?'btnGrid':'btnList').click()"); await pg.click('#btnPreview'); await pg.wait_for_timeout(500)
    await pg.locator('.tile', has_text='Общий').click(); await pg.wait_for_timeout(2000)
    await pg.screenshot(path='s_expl.png')
    await pg.keyboard.press('ArrowDown'); await pg.wait_for_timeout(1000); print('explorer down ->', await name(pg))
    # 4 PDF zoom bg check: zoom out heavy pdf far, check corner pixel colors
    await pg.locator('.tile', has_text='Общий').click(); await pg.wait_for_timeout(1500)
    box=await pg.locator('#stage canvas').first.bounding_box()
    cx,cy=box['x']+box['width']/2, box['y']+box['height']/2
    await pg.mouse.move(cx,cy)
    for i in range(5): await pg.mouse.wheel(0,-300); await pg.wait_for_timeout(60)
    await pg.wait_for_timeout(900)
    for i in range(9): await pg.mouse.wheel(0,300); await pg.wait_for_timeout(60)
    await pg.wait_for_timeout(900)
    px=await pg.evaluate("""()=>{const c=document.querySelector('#stage canvas');const x=c.getContext('2d').getImageData(3,3,1,1).data;return [...x].slice(0,3)}""")
    print('corner pixel after zoom in/out (should be dark bg):', px)
    await pg.screenshot(path='s_zoomout.png')
    # 5 theme light + bg white
    await pg.click('#btnSet'); await pg.select_option('#sTheme','light'); await pg.wait_for_timeout(300); await pg.click('#setClose')
    await pg.locator('.tile', has_text='002-08пс').click(); await pg.wait_for_timeout(2500)
    await pg.screenshot(path='s_light.png')
    await pg.keyboard.press('Enter'); await pg.wait_for_timeout(700); print('full after enter:', await pg.evaluate('VW.full'))
    await pg.keyboard.press('Escape'); await pg.wait_for_timeout(500); print('full after esc:', await pg.evaluate('VW.full'), 'docked visible:', await pg.is_visible('#viewer'))
    # 6 history
    await pg.click('#btnHist'); await pg.wait_for_timeout(300); print('HIST:', (await pg.inner_text('#hBody'))[:300].replace('\n',' | '))
    await pg.screenshot(path='s_hist.png')
    print('errors:', errs); await b.close()
asyncio.run(main())
