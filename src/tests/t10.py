import asyncio, glob, time, sys
from playwright.async_api import async_playwright
async def run(p,url,prof):
  ctx=await p.chromium.launch_persistent_context(prof,executable_path='/usr/bin/google-chrome',viewport={'width':1400,'height':850})
  pg=ctx.pages[0]
  await pg.add_init_script("try{const s=JSON.parse(localStorage.getItem('dxfv.set')||'{}');if(s.click===undefined){s.click='1';localStorage.setItem('dxfv.set',JSON.stringify(s))}}catch(e){}")
  await pg.goto(url); await pg.wait_for_timeout(1500)
  if url.startswith('http'): await pg.reload(); await pg.wait_for_timeout(1000)
  await pg.set_input_files('#inFiles',sorted(glob.glob('dxf/тяжёлый_*.pdf'))); await pg.wait_for_timeout(300)
  await pg.click('.tile'); await pg.wait_for_function('panes[0]&&!panes[0].loading&&panes[0].doc',timeout=30000)
  ts=[]
  for i in range(6):
    await pg.wait_for_timeout(1200); t=time.time(); await pg.keyboard.press('ArrowRight'); await pg.wait_for_timeout(30)
    await pg.wait_for_function('panes[0]&&!panes[0].loading&&panes[0].doc',timeout=30000); ts.append(round(time.time()-t,2))
  await ctx.close(); return ts
async def main():
  async with async_playwright() as p:
    print('file :', await run(p,'file:///home/claude/dxf-viewer.html','/tmp/claude-0/t/pf1'))
    print('http :', await run(p,'http://localhost:8765/dxf-viewer/','/tmp/claude-0/t/pf2'))
asyncio.run(main())
