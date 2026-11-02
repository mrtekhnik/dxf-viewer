import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    ctx=await p.chromium.launch_persistent_context('/tmp/claude-0/t/pf_24',executable_path='/usr/bin/google-chrome',viewport={'width':1400,'height':820})
    pg=ctx.pages[0]; errs=[]; pg.on('pageerror',lambda e: errs.append(str(e))); pg.on('console',lambda m: errs.append(m.text[:150]) if m.type=='error' else None)
    pg.on('dialog', lambda d: asyncio.ensure_future(d.accept()))
    await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.set_input_files('#inFolder','tree/Изделие 320'); await pg.wait_for_timeout(1800)
    # 1 rotation chip + badge + original toggle
    await pg.locator('.tile', has_text='00.02-St-8').click(); await pg.wait_for_timeout(1200)
    await pg.keyboard.press('e'); await pg.wait_for_timeout(300)
    print('chip:', await pg.locator('.pane .pxf').first.inner_text(), '| visible', await pg.locator('.pane .pxf').first.is_visible())
    await pg.screenshot(path='v_chip.png')
    await pg.locator('.pane .pxf button').first.click(); await pg.wait_for_timeout(300)
    print('orig:', await pg.locator('.pane .pxf').first.inner_text(), '| dims', await pg.inner_text('#vDims'))
    await pg.locator('.pane .pxf button').first.click(); await pg.wait_for_timeout(300)
    print('back:', await pg.inner_text('#vDims'))
    await pg.keyboard.press('Escape'); await pg.wait_for_timeout(300)
    print('badge:', await pg.locator('.tile', has_text='00.02-St-8').locator('.xfb').inner_text())
    # 4 bg settings
    await pg.click('#btnSet'); await pg.wait_for_timeout(200)
    await pg.select_option('#sBgDxf','#212830'); await pg.select_option('#sBgPdf','#ffffff'); await pg.select_option('#sPdfDark','1'); await pg.wait_for_timeout(200)
    print('xf count:', await pg.inner_text('#xfCount'))
    # 5 captions: grid show size + date
    cbs=pg.locator('#capT tr'); 
    await cbs.nth(4).locator('input').first.check(); await cbs.nth(5).locator('input').first.check(); await cbs.nth(2).locator('input').first.check(); await pg.wait_for_timeout(200)
    await pg.screenshot(path='v_settings.png')
    await pg.click('#setClose'); await pg.wait_for_timeout(1800)
    print('meta sample:', await pg.locator('.tile .meta').first.inner_text())
    # 8 size plus
    w0=(await pg.locator('.tile').first.bounding_box())['width']
    for i in range(3): await pg.click('#szPlus')
    await pg.wait_for_timeout(200); w1=(await pg.locator('.tile').first.bounding_box())['width']; print('tile width', round(w0),'->',round(w1))
    await pg.screenshot(path='v_grid.png')
    # 6/7 tree splitter + expand selected
    await pg.locator('.tr', has_text='02 Рама').click(); await pg.wait_for_timeout(300)
    await pg.click('#treeExpand'); await pg.wait_for_timeout(200); print('tree after expand Рама:', (await pg.inner_text('#treeBody')).replace('\n',' '))
    await pg.click('#treeFold'); await pg.wait_for_timeout(200); print('after fold Рама:', (await pg.inner_text('#treeBody')).replace('\n',' '))
    b=await pg.locator('#split2').bounding_box(); await pg.mouse.move(b['x']+3,b['y']+200); await pg.mouse.down(); await pg.mouse.move(b['x']+120,b['y']+200,steps=5); await pg.mouse.up()
    print('tree width:', round((await pg.locator('#tree').bounding_box())['width']))
    # PDF dark view
    await pg.locator('.tr.all').click(); await pg.wait_for_timeout(300)
    await pg.locator('.tile', has_text='Боковина.pdf').click(); await pg.wait_for_timeout(1500); await pg.screenshot(path='v_pdfdark.png'); await pg.keyboard.press('Escape')
    # 3 history: delete one row, clear period
    await pg.click('#btnHist'); await pg.wait_for_timeout(200); n0=await pg.locator('.h-row').count()
    await pg.locator('.h-row').first.hover(); await pg.locator('.h-row .h-del').first.click(); await pg.wait_for_timeout(200)
    print('hist rows', n0, '->', await pg.locator('.h-row').count())
    await pg.click('#hClear'); await pg.wait_for_timeout(300); print('after clear:', await pg.inner_text('#hBody'))
    await pg.click('#hClose')
    # 2 close
    await pg.click('#btnClose'); await pg.wait_for_timeout(300)
    print('after close: tiles', await pg.locator('.tile').count(), '| empty visible', await pg.is_visible('#empty'), '| tree hidden', await pg.is_hidden('#tree'), '| close btn hidden', await pg.is_hidden('#btnClose'))
    print('errors:', errs); await ctx.close()
asyncio.run(main())
