import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1400,'height':850})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.set_input_files('#inFiles',['kit/Заказ/АБВГ.123456.002 Корпус.pdf']); await pg.wait_for_timeout(2500)
    for lv in [-2,-1,0,1,2,3]:
      await pg.evaluate(f"setContrast({lv},true)"); await pg.wait_for_timeout(400)
      r=await pg.evaluate("""(()=>{const c=panes[0].cv,x=c.getContext('2d').getImageData(0,0,c.width,c.height).data;let nw=0,dk=0;
        for(let i=0;i<x.length;i+=4){const v=(x[i]+x[i+1]+x[i+2])/3;if(v<235&&v>40)nw++;if(v<120&&v>=0)dk++;}return [nw,dk,$('vCtN').textContent]})()""")
      print(lv, r)
    await pg.evaluate("setContrast(3,true)"); await pg.wait_for_timeout(400); await pg.screenshot(path='t36.png')
    print('errors',errs); await b.close()
asyncio.run(main())
