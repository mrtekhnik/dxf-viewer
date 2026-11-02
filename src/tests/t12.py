import asyncio, base64
from playwright.async_api import async_playwright
U='http://localhost:8765/dxf-viewer/'
async def main():
  async with async_playwright() as p:
    ctx=await p.chromium.launch_persistent_context('/tmp/claude-0/t/pf_h',executable_path='/usr/bin/google-chrome',viewport={'width':1300,'height':800})
    pg=ctx.pages[0]; errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto(U); await pg.wait_for_timeout(1500)
    pdf=base64.b64encode(open('dxf/деталь_01.pdf','rb').read()).decode(); dxf=base64.b64encode(open('dxf/деталь_01.dxf','rb').read()).decode()
    await pg.evaluate("""async ([a,b])=>{const root=await navigator.storage.getDirectory();const d=await root.getDirectoryHandle('Заказ 77',{create:true});const s=await d.getDirectoryHandle('DXF',{create:true});
      const w=async(dir,n,b64)=>{const f=await dir.getFileHandle(n,{create:true});const ws=await f.createWritable();await ws.write(Uint8Array.from(atob(b64),c=>c.charCodeAt(0)));await ws.close();};
      await w(d,'АБВГ.123456.009 Рама.pdf',a);await w(s,'АБВГ.123456.009-Ст3-4-k1.dxf',b);
      await openDirHandle(d);}""",[pdf,dxf])
    await pg.wait_for_timeout(1200)
    await pg.locator('.tile', has_text='Рама').click(); await pg.wait_for_timeout(2500)
    await pg.keyboard.press('Escape'); await pg.wait_for_timeout(300)
    await pg.reload(); await pg.wait_for_timeout(1500)
    await pg.click('#btnHist'); await pg.wait_for_timeout(300)
    await pg.select_option('#hKind','folder'); await pg.wait_for_timeout(100); print('folders:', (await pg.inner_text('#hBody')).replace('\n',' | '))
    await pg.select_option('#hKind','file'); await pg.wait_for_timeout(100); print('files:', (await pg.inner_text('#hBody')).replace('\n',' | '))
    await pg.locator('.h-row', has_text='Рама').click(); await pg.wait_for_timeout(2500)
    print('reopened ->', await pg.inner_text('#vName'), '| full:', await pg.evaluate('VW.full'), '| status:', await pg.inner_text('#status'))
    print('errors:', errs); await ctx.close()
asyncio.run(main())
