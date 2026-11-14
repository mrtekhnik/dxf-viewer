# размеры: перетащить размерную линию, выбрать и удалить; ✕ справа в просмотре в окне
import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1400,'height':850})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.set_input_files('#inFiles',['cmp2/Заказ А/DXF/АБВГ.200001.003-Ст3-3-k1.dxf','cmp2/Заказ А/DXF/АБВГ.200001.002-Ст3-3-k1.dxf']); await pg.wait_for_timeout(1500)
    await pg.locator('.tile').first.dblclick(); await pg.wait_for_timeout(800)
    await pg.keyboard.press('d'); await pg.wait_for_timeout(200)
    bb=await pg.locator('#stage canvas').first.bounding_box()
    sc=lambda x,y: pg.evaluate(f"(()=>{{const p=panes[0],o=p.doc.origin;return m2s(p,{x}-o[0],{y}-o[1])}})()")
    async def click(x,y):
      q=await sc(x,y); await pg.mouse.move(bb['x']+q[0],bb['y']+q[1]); await pg.wait_for_timeout(60); await pg.mouse.click(bb['x']+q[0],bb['y']+q[1]); await pg.wait_for_timeout(400)
    await click(0,0); print('pts',await pg.evaluate('panes[0].ms.pts.length'),await pg.evaluate('SET.mmode')); await click(250,60); print('pts',await pg.evaluate('panes[0].ms.pts.length')); await click(120,-6); print('after3',await pg.evaluate('panes[0].ms.items.length'),errs)
    await pg.select_option('#measMode','dist'); await click(50,60); await click(150,150)
    print('items', await pg.evaluate("panes[0].ms.items.map(i=>i.t)"))
    # где размерная линия горизонтального размера
    G=await pg.evaluate("(()=>{const p=panes[0],it=p.ms.items[0],G=dimGeom(p,it);return [(G.a2[0]+G.b2[0])/2+40,G.a2[1],it.o[1]]})()")
    X,Y=bb['x']+G[0],bb['y']+G[1]
    await pg.mouse.move(X,Y); await pg.wait_for_timeout(100); print('cursor', await pg.evaluate("panes[0].cv.style.cursor"))
    s0=await pg.evaluate('[panes[0].cx,panes[0].cy]')
    await pg.mouse.down(); await pg.mouse.move(X+10,Y+20,steps=3); await pg.mouse.move(X+10,Y+60,steps=5); await pg.mouse.up(); await pg.wait_for_timeout(200)
    print('o.y before',round(G[2],2),'after',round(await pg.evaluate('panes[0].ms.items[0].o[1]'),2),'view not panned',s0==await pg.evaluate('[panes[0].cx,panes[0].cy]'),'sel',await pg.evaluate("panes[0].ms.sel===panes[0].ms.items[0]"))
    await pg.screenshot(path='t63a.png')
    await pg.keyboard.press('Escape'); print('esc deselect', await pg.evaluate("!panes[0].ms.sel"), 'meas still on', await pg.evaluate('MEAS.on'))
    # выбрать «расстояние» кликом по надписи и удалить
    T=await pg.evaluate("(()=>{const p=panes[0],it=p.ms.items[1],a=m2s(p,...it.a),b=m2s(p,...it.b);return [(a[0]+b[0])/2-14,(a[1]+b[1])/2-12]})()")
    await pg.mouse.move(bb['x']+T[0],bb['y']+T[1]); await pg.wait_for_timeout(80); await pg.mouse.click(bb['x']+T[0],bb['y']+T[1]); await pg.wait_for_timeout(200)
    print('dist selected', await pg.evaluate("panes[0].ms.sel&&panes[0].ms.sel.t"), 'items',await pg.evaluate("panes[0].ms.items.length"))
    await pg.keyboard.press('Delete'); await pg.wait_for_timeout(200); print('after delete', await pg.evaluate("panes[0].ms.items.map(i=>i.t)"))
    # пустое место — новый размер работает как прежде
    await pg.select_option('#measMode','dim'); await click(0,0); await click(250,60); await click(130,-4); print('new items', await pg.evaluate("panes[0].ms.items.map(i=>i.t)"))
    # ✕ справа
    vb=await pg.locator('.vbar').bounding_box(); cb=await pg.locator('#vClose').bounding_box(); print('close at right', cb['x']+cb['width']>vb['x']+vb['width']-12, await pg.is_visible('#vClose'))
    print('errors',errs); await b.close()
asyncio.run(main())
