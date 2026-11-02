import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); ctx=await b.new_context(viewport={'width':1400,'height':850}); pg=await ctx.new_page()
    errs=[]; pg.on('pageerror',lambda e: errs.append('M:'+str(e)))
    await pg.goto('file:///home/claude/dxf-viewer.html')
    # (3) scope
    await pg.set_input_files('#inFolder','inv/СК Рама'); await pg.wait_for_timeout(1200)
    await pg.locator('.tr', has_text='PDF,DXF').first.click(); await pg.wait_for_timeout(300)
    await pg.locator('.tile', has_text='Профіль').click(); await pg.wait_for_timeout(600); await pg.keyboard.press('r'); await pg.wait_for_timeout(1500)
    print('scope dir caps:', [c.replace('\n',' | ') for c in await pg.locator('#stage .pcap').all_inner_texts()])
    print('single caption shown:', await pg.evaluate("$('stage').classList.contains('capone')"))
    await pg.keyboard.press('r'); await pg.wait_for_timeout(500); print('single caption shown:', await pg.evaluate("$('stage').classList.contains('capone')"), await pg.locator('#stage .pcap').first.is_visible())
    await pg.keyboard.press('Escape')
    # (4) order
    await pg.set_input_files('#inFolder','kit/Заказ'); await pg.wait_for_timeout(1200)
    await pg.locator('.tile', has_text='Корпус').click(); await pg.wait_for_timeout(500)
    print('order:', await pg.evaluate("targets(view[VW.idx]).map(x=>x.name)"))
    # (1) monitors
    await pg.evaluate("Object.defineProperty(screen,'isExtended',{get:()=>true});updateBar()")
    async with ctx.expect_page() as pi: await pg.click('#vMon')
    p2=await pi.value; await p2.wait_for_timeout(2000)
    seq=[]
    for i in range(5):
      seq.append((await pg.evaluate("panes[0].it&&panes[0].it.name"), await p2.evaluate("VW.set.map(x=>x.name).join(', ')")))
      await pg.keyboard.press('ArrowRight'); await pg.wait_for_timeout(1300)
    for s in seq: print('  main:',s[0],' | second:',s[1])
    await pg.click('#vPair'); await pg.wait_for_timeout(1500)
    print('after swap main:', await pg.evaluate("panes[0].it&&panes[0].it.name"), '| second:', await p2.evaluate("VW.set.map(x=>x.name).join(', ')"), '|', await pg.inner_text('#status'))
    print('errors', errs); await b.close()
asyncio.run(main())
