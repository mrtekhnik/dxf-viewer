# допуски сравнения 0.001/0.005/0.02 и «включительно»
import asyncio,base64
from playwright.async_api import async_playwright
def b64(f): return base64.b64encode(open('tolx/'+f,'rb').read()).decode()
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page()
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.wait_for_timeout(800)
    opts=await pg.evaluate("[...$('ovTol').options].map(o=>o.value)"); print(opts)
    for v in ['0.001','0.005','0.02']:
      if v not in opts: errs.append('нет допуска '+v)
    js="""async([a,b,tol])=>{const ab=s=>Uint8Array.from(atob(s),c=>c.charCodeAt(0)).buffer;const A=await Pool.parse(ab(a),'a'),B=await Pool.parse(ab(b),'b');const r=await geoCompare(A,B,tol);return r.same;}"""
    for f,tol,exp in [('b02.dxf',0.02,True),('b02.dxf',0.01,False),('b003.dxf',0.005,True),('b003.dxf',0.001,False),('a.dxf',0.001,True)]:
      r=await pg.evaluate(js,[b64('a.dxf'),b64(f),tol]); print(f,tol,r)
      if r!=exp: errs.append(f'{f} допуск {tol}: {r}, ждали {exp}')
    print('errors',errs); await b.close()
asyncio.run(main())
