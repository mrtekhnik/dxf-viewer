import asyncio, glob, subprocess
from playwright.async_api import async_playwright
U='http://localhost:8765/dxf-viewer/'
async def main():
  async with async_playwright() as p:
    ctx=await p.chromium.launch_persistent_context('/tmp/claude-0/t/prof_pwa',executable_path='/usr/bin/google-chrome',viewport={'width':1200,'height':760})
    pg=ctx.pages[0]; errs=[]; pg.on('pageerror',lambda e: errs.append(str(e))); pg.on('console',lambda m: errs.append(m.text[:150]) if m.type=='error' else None)
    await pg.goto(U); await pg.wait_for_function("navigator.serviceWorker.controller!==null||new Promise(r=>navigator.serviceWorker.ready.then(()=>r(true)))",timeout=15000)
    await pg.reload(); await pg.wait_for_timeout(1500)
    print('SW controller:', await pg.evaluate('!!navigator.serviceWorker.controller'), '| caches:', await pg.evaluate('caches.keys()'))
    await pg.set_input_files('#inFiles',sorted(glob.glob('dxf/деталь_01.*'))); await pg.wait_for_timeout(2500)
    print('online thumbs:', await pg.locator('.tile img:not([hidden])').count())
    # offline
    await ctx.set_offline(True); await pg.reload(); await pg.wait_for_timeout(1000)
    print('offline title:', await pg.title(), '|', await pg.inner_text('.brand'))
    await pg.set_input_files('#inFiles',sorted(glob.glob('dxf/деталь_01.*')+['dxf/сборка_СБ.pdf'])); await pg.wait_for_timeout(3000)
    print('offline thumbs (incl. PDF):', await pg.locator('.tile img:not([hidden])').count(), 'of', await pg.locator('.tile').count())
    await ctx.set_offline(False)
    # update flow: change index -> rebuild
    s=open('/home/claude/dxf-viewer.src.html').read(); open('/home/claude/dxf-viewer.src.html','w').write(s.replace('· v1.7','· v1.7t'))
    subprocess.run(['python3','build.py'],capture_output=True)
    await pg.evaluate("navigator.serviceWorker.getRegistration().then(r=>r.update())"); await pg.wait_for_timeout(3000)
    print('update bar visible:', await pg.is_visible('#updBar'))
    await pg.click('#updBtn'); await pg.wait_for_timeout(2500)
    print('after update:', await pg.inner_text('.brand'))
    open('/home/claude/dxf-viewer.src.html','w').write(s); subprocess.run(['python3','build.py'],capture_output=True)
    print('errors:', errs); await ctx.close()
asyncio.run(main())
