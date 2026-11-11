import asyncio, base64
from playwright.async_api import async_playwright
U='http://localhost:8765/dxf-viewer/'
async def main():
  async with async_playwright() as p:
    ctx=await p.chromium.launch_persistent_context('/tmp/claude-0/t/pf_pin',executable_path='/usr/bin/google-chrome',viewport={'width':1300,'height':800})
    pg=ctx.pages[0]; errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.add_init_script("try{const s=JSON.parse(localStorage.getItem('dxfv.set')||'{}');if(s.click===undefined){s.click='1';localStorage.setItem('dxfv.set',JSON.stringify(s))}}catch(e){}")
    pg.on('dialog', lambda d: asyncio.ensure_future(d.accept()))
    await pg.goto(U); await pg.wait_for_timeout(1500)
    pdf=base64.b64encode(open('dxf/деталь_01.pdf','rb').read()).decode(); dxf=base64.b64encode(open('dxf/деталь_01.dxf','rb').read()).decode()
    await pg.evaluate("""async ([a,b])=>{const root=await navigator.storage.getDirectory();
      const mk=async(parent,names)=>{let d=parent;for(const n of names)d=await d.getDirectoryHandle(n,{create:true});return d;};
      const w=async(dir,n,b64)=>{const f=await dir.getFileHandle(n,{create:true});const ws=await f.createWritable();await ws.write(Uint8Array.from(atob(b64),c=>c.charCodeAt(0)));await ws.close();};
      const top=await mk(root,['Изделие 320']);
      const r=await mk(top,['02 Рама','02.01 Боковина']);await w(r,'АЮИА.320-02.01.00.00.02 Боковина.pdf',a);await w(await mk(r,['DXF']),'АЮИА.320-02.01.00.00.02-St-8-k2.DXF',b);
      const k=await mk(top,['03 Крышка']);await w(k,'АЮИА.320-03.00.00.01 Крышка.pdf',a);
      await openDirHandle(top);}""",[pdf,dxf])
    await pg.wait_for_timeout(1200)
    # pin subfolder via tree selection
    await pg.locator('.tr', has_text='02.01 Боковина').click(); await pg.wait_for_timeout(300)
    await pg.click('#btnPins'); await pg.wait_for_timeout(200); print('add opts:', await pg.locator('#pinAdd button').all_inner_texts())
    await pg.locator('#pinAdd button').first.click(); await pg.wait_for_timeout(200)
    await pg.click('#pinClose')
    # pin a file
    await pg.locator('.tile', has_text='Крышка').click() if await pg.locator('.tile', has_text='Крышка').count() else None
    await pg.locator('.tr.all').click(); await pg.wait_for_timeout(200)
    await pg.locator('.tile', has_text='Крышка').click(); await pg.wait_for_timeout(1500)
    await pg.click('#vPin'); await pg.wait_for_timeout(200); await pg.keyboard.press('Escape'); await pg.wait_for_timeout(300)
    await pg.click('#btnPins'); await pg.wait_for_timeout(200)
    print('pins:', (await pg.inner_text('#pinList')).replace('\n',' | '))
    await pg.screenshot(path='pins.png')
    await pg.click('#pinClose'); await pg.keyboard.press('Escape')
    await pg.click('#btnClose'); await pg.wait_for_timeout(200)
    await pg.reload(); await pg.wait_for_timeout(1500)
    await pg.click('#btnPins'); await pg.wait_for_timeout(200)
    await pg.locator('.pin', has_text='02.01 Боковина').click(); await pg.wait_for_timeout(1800)
    print('open folder pin ->', await pg.inner_text('#status'), '| tiles', await pg.locator('#grid .tile .nm').all_inner_texts())
    await pg.click('#btnPins'); await pg.locator('.pin', has_text='Крышка').click(); await pg.wait_for_timeout(1800)
    print('open file pin ->', await pg.inner_text('#vName'), '| full', await pg.evaluate('VW.full'))
    print('errors:', errs); await ctx.close()
asyncio.run(main())
