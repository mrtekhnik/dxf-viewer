# текст из PDF: рамка, клик, Ctrl+A, исправление cp1251, повёрнутый текст
import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); ctx=await b.new_context(viewport={'width':1400,'height':900}); await ctx.grant_permissions(['clipboard-read','clipboard-write'])
    pg=await ctx.new_page(); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.set_input_files('#inFiles',['blk/txt_test.pdf']); await pg.wait_for_timeout(1800)
    print('btn', await pg.is_visible('#vTxt'))
    await pg.keyboard.press('t'); await pg.wait_for_timeout(500); print('on',await pg.evaluate('TXT.on'))
    bb=await pg.locator('#stage canvas').first.bounding_box()
    # координаты листа → экран
    sc=lambda x,y: pg.evaluate(f"(()=>{{const p=panes[0],e=p.pg[0],s=p.s,L=p.W/2+(e.ox-p.cx)*s,T=p.H/2-((p.ph-e.oy)-p.cy)*s;return [L+{x}*s,T+(e=>e.h)(e)*0+{y}*s]}})()")
    H=await pg.evaluate('panes[0].pg[0].h')
    a=await sc(90,H-520); c=await sc(450,H-460)
    await pg.mouse.move(bb['x']+a[0],bb['y']+a[1]); await pg.mouse.down(); await pg.mouse.move(bb['x']+c[0],bb['y']+c[1],steps=6); await pg.mouse.up(); await pg.wait_for_timeout(600)
    print('rect ->',repr(await pg.input_value('#txtArea')))
    print('clipboard', repr(await pg.evaluate('navigator.clipboard.readText()')))
    await pg.screenshot(path='t65a.png')
    # клик по повёрнутому тексту
    q=await sc(595,H-350); await pg.mouse.click(bb['x']+q[0],bb['y']+q[1]); await pg.wait_for_timeout(500)
    print('click rotated ->',repr(await pg.input_value('#txtArea')))
    # Ctrl+клик добавляет
    q=await sc(120,H-296); await pg.keyboard.down('Control'); await pg.mouse.click(bb['x']+q[0],bb['y']+q[1]); await pg.keyboard.up('Control'); await pg.wait_for_timeout(500)
    print('ctrl add ->',repr(await pg.input_value('#txtArea')))
    await pg.keyboard.press('Control+a'); await pg.wait_for_timeout(500); print('ctrl+a ->',repr(await pg.input_value('#txtArea')))
    await pg.keyboard.press('Escape'); await pg.wait_for_timeout(200); print('esc1 box hidden',await pg.is_hidden('#txtBox'),'on',await pg.evaluate('TXT.on'))
    await pg.keyboard.press('Escape'); await pg.wait_for_timeout(200); print('esc2 on',await pg.evaluate('TXT.on'),'viewer',await pg.is_visible('#viewer'))
    print('errors',errs); await b.close()
asyncio.run(main())
