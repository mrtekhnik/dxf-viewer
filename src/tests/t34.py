import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); ctx=await b.new_context(**p.devices['Pixel 7']); pg=await ctx.new_page()
    await pg.add_init_script("try{const s=JSON.parse(localStorage.getItem('dxfv.set')||'{}');if(s.click===undefined){s.click='1';localStorage.setItem('dxfv.set',JSON.stringify(s))}}catch(e){}")
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.set_input_files('#inFiles',['dxf/деталь_01.dxf','dxf/деталь_02_R12.dxf','dxf/деталь_01.pdf']); await pg.wait_for_timeout(1500)
    print('MOB',await pg.evaluate('[MOB,MAXRUN,BGRUN]'))
    await pg.locator('.tile').first.tap(); await pg.wait_for_timeout(1000)
    print('open', await pg.evaluate('[VW.idx,VW.full]'))
    # синтетический свайп влево
    await pg.evaluate("""(()=>{const cv=panes[0].cv,r=cv.getBoundingClientRect(),y=r.top+r.height/2;
      const ev=(t,x)=>cv.dispatchEvent(new PointerEvent(t,{pointerId:5,pointerType:'touch',clientX:x,clientY:y,bubbles:true,isPrimary:true}));
      ev('pointerdown',r.left+300);ev('pointermove',r.left+250);ev('pointermove',r.left+150);ev('pointerup',r.left+100);})()""")
    await pg.wait_for_timeout(800); print('after swipe', await pg.evaluate('[VW.idx,VW.full,panes[0].fitted]'))
    await pg.screenshot(path='t34.png'); print('errors',errs); await b.close()
asyncio.run(main())
