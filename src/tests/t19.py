import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    ctx=await p.chromium.launch_persistent_context('/tmp/claude-0/t/pf_26',executable_path='/usr/bin/google-chrome',viewport={'width':1300,'height':800})
    pg=ctx.pages[0]; errs=[]; pg.on('pageerror',lambda e: errs.append(str(e))); pg.on('console',lambda m: errs.append(m.text[:150]) if m.type=='error' else None)
    await pg.goto('file:///home/claude/dxf-viewer.html')
    # texts
    await pg.set_input_files('#inFiles',['ml/multileader.dxf']); await pg.wait_for_timeout(1500)
    print('log:', await pg.evaluate("items[0].log.map(l=>l[1]).join(' | ')"))
    await pg.screenshot(path='ml_view.png'); await pg.keyboard.press('Escape')
    # keyboard in grid without preview
    await pg.set_input_files('#inFolder','tree/Изделие 320'); await pg.wait_for_timeout(1500)
    await pg.keyboard.press('ArrowRight'); await pg.keyboard.press('ArrowRight'); await pg.keyboard.press('ArrowDown'); await pg.wait_for_timeout(100)
    print('grid sel:', await pg.evaluate("VW.idx"), 'cols', await pg.evaluate("gridCols()"), '| cur tile:', await pg.locator('.tile.cur .nm').inner_text())
    await pg.keyboard.press('Enter'); await pg.wait_for_timeout(800); print('enter -> full:', await pg.evaluate('VW.full'), await pg.inner_text('#vName'))
    await pg.keyboard.press('Escape'); await pg.wait_for_timeout(300)
    # list without preview
    await pg.click('#btnLayout'); await pg.wait_for_timeout(200); await pg.keyboard.press('ArrowDown'); await pg.wait_for_timeout(100)
    print('list sel:', await pg.locator('.tile.cur .nm').inner_text(), '| viewer hidden', await pg.is_hidden('#viewer'))
    # preview on with list
    await pg.click('#btnPreview'); await pg.wait_for_timeout(1200); await pg.keyboard.press('ArrowRight'); await pg.wait_for_timeout(800)
    print('list+preview:', await pg.inner_text('#vName')); await pg.screenshot(path='lp.png')
    # grid + preview
    await pg.click('#btnLayout'); await pg.wait_for_timeout(1200); await pg.keyboard.press('ArrowDown'); await pg.wait_for_timeout(800)
    print('grid+preview:', await pg.inner_text('#vName')); await pg.screenshot(path='gp.png')
    print('errors:', errs); await ctx.close()
asyncio.run(main())
