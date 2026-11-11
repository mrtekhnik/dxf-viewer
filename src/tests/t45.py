import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1500,'height':850})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.set_input_files('#inFolder','cmp2/Заказ А'); await pg.wait_for_timeout(1500)
    await pg.set_input_files('#inCmp','cmp2/Заказ Б'); await pg.wait_for_timeout(2500)
    await pg.locator('.tile', has_text='200001.003').locator('.cmpb').click(); await pg.wait_for_timeout(2500)
    print('two:', await pg.inner_text('#ovRes'), '| panes', await pg.evaluate('VW.set.length'), await pg.evaluate('panes.slice(0,2).map(p=>p.ov&&p.ov.side)'))
    await pg.screenshot(path='t45a.png')
    await pg.click('#ovListBtn'); await pg.wait_for_timeout(300); print('list:', (await pg.inner_text('#ovList')).replace('\n',' | '))
    await pg.locator('#ovList .ovl').nth(1).click(); await pg.wait_for_timeout(500); await pg.screenshot(path='t45b.png')
    print('sync:', await pg.evaluate('panes.slice(0,2).map(p=>[p.s.toFixed(3),p.cx.toFixed(1),p.cy.toFixed(1)])'))
    await pg.keyboard.press('n'); await pg.wait_for_timeout(2000); print('over:', await pg.evaluate('VW.set.length'), await pg.inner_text('#ovRes'))
    await pg.evaluate("SET.blink=true"); await pg.keyboard.press(' '); await pg.wait_for_timeout(300); print('blink', await pg.evaluate('OV.blink')); await pg.screenshot(path='t45c.png')
    await pg.keyboard.press('n'); await pg.wait_for_timeout(2000); print('back two:', await pg.evaluate('VW.set.length'))
    print('idx before', await pg.evaluate('[VW.idx,VW.cmp&&VW.cmp.manual,SET.cmpView,OV&&OV.mode,VW.set.length]')); await pg.keyboard.press('ArrowRight'); await pg.wait_for_timeout(2500); print('next pair:', await pg.inner_text('#ovRes'), await pg.evaluate('VW.set.map(x=>x.name)'))
    await pg.keyboard.press('Escape'); await pg.wait_for_timeout(800); print('esc:', await pg.is_visible('#ovBar'), await pg.evaluate('VW.set.length'))
    print('errors',errs); await b.close()
asyncio.run(main())
