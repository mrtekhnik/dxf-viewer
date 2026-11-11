import asyncio, glob, time
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    ctx=await p.chromium.launch_persistent_context('/tmp/claude-0/t/prof',executable_path='/usr/bin/google-chrome',viewport={'width':390,'height':800},is_mobile=True,has_touch=True,device_scale_factor=2)
    pg=ctx.pages[0]; errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.add_init_script("try{const s=JSON.parse(localStorage.getItem('dxfv.set')||'{}');if(s.click===undefined){s.click='1';localStorage.setItem('dxfv.set',JSON.stringify(s))}}catch(e){}")
    files=sorted(glob.glob('dxf/*'))
    for run in (1,2):
      await pg.goto('file:///home/claude/dxf-viewer.html')
      t=time.time(); await pg.set_input_files('#inFiles',files)
      await pg.wait_for_function("document.querySelectorAll('.tile img:not([hidden])').length>=6",timeout=20000)
      print('run',run,'first thumbs %.2fs'%(time.time()-t))
    await pg.screenshot(path='m_grid.png')
    await pg.fill('#filter','деталь_01.pdf'); await pg.wait_for_timeout(300); await pg.tap('.tile'); await pg.wait_for_timeout(2500)
    await pg.screenshot(path='m_view.png')
    print(errs); await ctx.close()
asyncio.run(main())
