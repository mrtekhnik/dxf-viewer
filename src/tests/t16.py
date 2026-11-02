import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    ctx=await p.chromium.launch_persistent_context('/tmp/claude-0/t/pf_x',executable_path='/usr/bin/google-chrome',viewport={'width':1100,'height':700})
    pg=ctx.pages[0]; errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.set_input_files('#inFiles',['dxf/деталь_01.dxf','dxf/деталь_01.pdf']); await pg.wait_for_timeout(1200)
    await pg.locator('.tile', has_text='деталь_01.dxf').click(); await pg.wait_for_timeout(1200)
    await pg.screenshot(path='x0.png'); print('0:', await pg.inner_text('#vDims'))
    await pg.keyboard.press('q'); await pg.wait_for_timeout(400); await pg.screenshot(path='x1.png'); print('Q:', await pg.inner_text('#vDims'), '| reset visible:', await pg.is_visible('#vXfReset'))
    await pg.keyboard.press('m'); await pg.wait_for_timeout(400); await pg.screenshot(path='x2.png'); print('M:', await pg.inner_text('#vDims'))
    # coordinate check: hover a known model point: the top-right corner of outline (220,120) original coords
    xy=await pg.evaluate("""(()=>{const p=panes[0];const m=xfMat(p.xf);const o=p.doc.origin;const w=mApply(m,220-o[0],120-o[1]);const r=p.cv.getBoundingClientRect();
      return [r.x+p.W/2+(w[0]-p.cx)*p.s, r.y+p.H/2-(w[1]-p.cy)*p.s]})()""")
    await pg.mouse.move(xy[0],xy[1]); await pg.wait_for_timeout(100); print('coord at (220,120):', await pg.inner_text('#vCoord'))
    # tab to pdf: xf buttons hidden
    await pg.keyboard.press('Tab'); await pg.wait_for_timeout(1200); print('pdf xf hidden:', await pg.is_hidden('#vXf'))
    await pg.keyboard.press('Escape')
    await pg.reload(); await pg.set_input_files('#inFiles',['dxf/деталь_01.dxf']); await pg.wait_for_timeout(800)
    await pg.wait_for_timeout(1000); print('after reload:', await pg.inner_text('#vDims'))
    await pg.keyboard.press('0'); await pg.wait_for_timeout(300); print('reset:', await pg.inner_text('#vDims'))
    print('errors:', errs); await ctx.close()
asyncio.run(main())
