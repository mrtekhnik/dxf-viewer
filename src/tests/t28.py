import asyncio
from playwright.async_api import async_playwright
JS_DARK="""(()=>{const p=panes[0],c=p.ctx,w=p.cv.width,h=p.cv.height,d=c.getImageData(0,0,w,h).data;let k=0,g=0;
  for(let i=0;i<d.length;i+=4){const l=(d[i]+d[i+1]+d[i+2])/3;if(l<70)k++;else if(l<200)g++;}return {black:k,gray:g}})()"""
async def run(b,url,label):
  pg=await b.new_page(viewport={'width':1400,'height':850},device_scale_factor=1)
  await pg.add_init_script("try{const s=JSON.parse(localStorage.getItem('dxfv.set')||'{}');if(s.click===undefined){s.click='1';localStorage.setItem('dxfv.set',JSON.stringify(s))}}catch(e){}")
  errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
  await pg.goto(url); await pg.set_input_files('#inFiles',['dxf/деталь_01.pdf','dxf/тяжёлый_1.pdf']); await pg.wait_for_timeout(1500)
  await pg.keyboard.press('Escape') if await pg.evaluate('VW.full') else None
  await pg.locator('.tile', has_text='деталь_01').click(); await pg.wait_for_timeout(2500)
  fit=await pg.evaluate(JS_DARK)
  await pg.screenshot(path=f'pdf_fit_{label}.png', clip={'x':300,'y':250,'width':500,'height':300})
  # тяжёлый лист: приблизить, дождаться, перетаскивать
  await pg.keyboard.press('Escape'); await pg.locator('.tile', has_text='тяжёлый').click(); await pg.wait_for_timeout(3000)
  await pg.evaluate("window._n=0;const o=Pane.prototype.renderHi;Pane.prototype.renderHi=function(){window._n++;return o.apply(this,arguments)};0")
  box=await pg.locator('#stage canvas').first.bounding_box(); cx,cy=box['x']+700,box['y']+400
  await pg.mouse.move(cx,cy)
  for i in range(4): await pg.mouse.wheel(0,-300); await pg.wait_for_timeout(40)
  await pg.wait_for_timeout(2500); n_zoom=await pg.evaluate('_n')
  import time
  await pg.mouse.down()
  for i in range(20): await pg.mouse.move(cx+i*8,cy+i*4); await pg.wait_for_timeout(30)
  await pg.mouse.up(); await pg.wait_for_timeout(300)
  for i in range(3):
    await pg.mouse.down(); await pg.mouse.move(cx-60,cy-30,steps=6); await pg.mouse.up(); await pg.wait_for_timeout(300)
  await pg.wait_for_timeout(1500); n_pan=await pg.evaluate('_n')-n_zoom
  print(label,'| fit pixels:',fit,'| renderHi после приближения:',n_zoom,'| перерисовок при перетаскиваниях:',n_pan, '| ошибки',errs)
  await pg.close()
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
    await run(b,'file:///tmp/claude-0/t/oldb/src/dist/dxf-viewer.html','СТАРАЯ')
    await run(b,'file:///home/claude/dxf-viewer.html','НОВАЯ ')
    pg=await b.new_page(); await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.set_input_files('#inFiles',['dxf/деталь_01.dxf','dxf/деталь_02_R12.dxf']); await pg.wait_for_timeout(800)
    await pg.add_init_script("try{const s=JSON.parse(localStorage.getItem('dxfv.set')||'{}');if(s.click===undefined){s.click='1';localStorage.setItem('dxfv.set',JSON.stringify(s))}}catch(e){}")
    await pg.locator('.tile').first.click(); await pg.wait_for_timeout(500)
    s0=await pg.evaluate('[SET.side,SET.lineK]')
    await pg.keyboard.press('Control+r') if False else await pg.evaluate("document.dispatchEvent(new KeyboardEvent('keydown',{key:'r',ctrlKey:true,bubbles:true}));document.dispatchEvent(new KeyboardEvent('keydown',{key:'B',ctrlKey:true,shiftKey:true,bubbles:true}))")
    s1=await pg.evaluate('[SET.side,SET.lineK]')
    await pg.keyboard.press('w'); s2=await pg.evaluate('[SET.side,SET.lineK]')
    print('клавиши: до',s0,'| Ctrl+R и Ctrl+Shift+B',s1,'| W',s2)
    await b.close()
asyncio.run(main())
