# телефон, замедленный процессор ×4: сколько ждать чёткости после щипка и после сдвига
import asyncio,sys,time
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); ctx=await b.new_context(**p.devices['Pixel 5']); pg=await ctx.new_page(); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    cdp=await ctx.new_cdp_session(pg); await cdp.send('Emulation.setCPUThrottlingRate',{'rate':4})
    await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.set_input_files('#inFiles',[sys.argv[1]]); await pg.wait_for_timeout(4000)
    await pg.evaluate("muiUi(false)")
    sharp="(()=>{const p=panes[0],e=p.pg[0],dh=MOB?Math.min(p.dpr,2):p.dpr,S=p.s*dh;if(e.base&&e.baseSc>=S*0.98||e.mid&&e.midSc>=S*0.98)return 'mid';const h=e.hv,v=p.pageView(e,p.viewRectAll());return h&&h.s===p.s&&v.x0>=h.x0-1e-6&&v.x1<=h.x1+1e-6&&v.y0>=h.y0-1e-6&&v.y1<=h.y1+1e-6?'hi':'';})()"
    async def wait_sharp():
      t=time.time()
      while time.time()-t<15:
        r=await pg.evaluate(sharp)
        if r: return round(time.time()-t,2),r
        await asyncio.sleep(0.05)
      return None,''
    await pg.wait_for_timeout(1500)
    await pg.evaluate("panes[0].zoomAt(200,350,2)"); print('zoom x2 ->',await wait_sharp())
    await pg.evaluate("panes[0].zoomAt(200,350,2)"); print('zoom x4 ->',await wait_sharp())
    for k in range(3):
      await pg.wait_for_timeout(3000)
      0 and print('dbg',await pg.evaluate("(()=>{const p=panes[0],e=p.pg[0],h=e.hv,v=p.pageView(e,p.viewRectAll());return {h:h&&[h.x0,h.x1,h.y0,h.y1].map(Math.round),v:[v.x0,v.x1,v.y0,v.y1].map(Math.round),pg:[e.w,e.h]}})()"))
      print('imm',await pg.evaluate("(()=>{const p=panes[0];p.cx+=p.W*0.3/p.s;p.draw();const e=p.pg[0],h=e.hv,v=p.pageView(e,p.viewRectAll());return [h&&h.s===p.s,[v.x0,v.x1,v.y0,v.y1].map(Math.round),h&&[h.x0,h.x1,h.y0,h.y1].map(Math.round)]})()"))
      print('pan 30% ->',await wait_sharp())
    await pg.wait_for_timeout(3000)
    await pg.evaluate("(()=>{const p=panes[0];p.cy-=p.H*0.3/p.s;p.draw();})()"); print('pan down 30% ->',await wait_sharp())
    print(errs); await b.close()
asyncio.run(main())
