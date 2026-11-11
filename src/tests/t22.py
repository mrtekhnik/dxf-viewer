import asyncio, base64
from playwright.async_api import async_playwright
U='http://localhost:8765/dxf-viewer/'
async def main():
  async with async_playwright() as p:
    ctx=await p.chromium.launch_persistent_context('/tmp/claude-0/t/pf_30a',executable_path='/usr/bin/google-chrome',viewport={'width':1300,'height':800})
    pg=ctx.pages[0]; errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.add_init_script("try{const s=JSON.parse(localStorage.getItem('dxfv.set')||'{}');if(s.click===undefined){s.click='1';localStorage.setItem('dxfv.set',JSON.stringify(s))}}catch(e){}")
    await pg.goto(U); await pg.wait_for_timeout(1500)
    d1=base64.b64encode(open('dxf/деталь_01.dxf','rb').read()).decode(); d2=base64.b64encode(open('dxf/деталь_015.dxf','rb').read()).decode(); pdf=base64.b64encode(open('dxf/сборка_СБ.pdf','rb').read()).decode()
    await pg.evaluate("""async ([a,b,c])=>{const root=await navigator.storage.getDirectory();
      const mk=async(parent,names)=>{let d=parent;for(const n of names)d=await d.getDirectoryHandle(n,{create:true});return d;};
      const w=async(dir,n,b64)=>{const f=await dir.getFileHandle(n,{create:true});const ws=await f.createWritable();await ws.write(Uint8Array.from(atob(b64),c=>c.charCodeAt(0)));await ws.close();};
      const top=await mk(root,['Изделие 500']);
      await w(await mk(top,['01 Рама','01.01 Боковина','DXF']),'A.500-01.01.01-St-4-k1.dxf',a);
      await w(await mk(top,['01 Рама','01.01 Боковина']),'A.500-01.01.01 Боковина.pdf',c);
      await w(await mk(top,['02 Крышка','DXF']),'A.500-02.01-St-2-k1.dxf',b);
      window._top=top; await openDirHandle(top);}""",[d1,d2,pdf])
    await pg.wait_for_timeout(1000)
    await pg.locator('.tr', has_text='01 Рама').locator('.cr').click() if False else None
    await pg.click('#treeExpand'); await pg.locator('.tr', has_text='01.01 Боковина').click(); await pg.select_option('#typeSel','dxf'); await pg.wait_for_timeout(600)
    print('before:', (await pg.inner_text('#treeBody')).replace('\n',' '), '| tiles', await pg.locator('#grid .tile').count())
    # LW button visible for file with lineweights?
    await pg.locator('.tile').first.click(); await pg.wait_for_timeout(1000)
    print('lw btn visible (file with lw):', await pg.is_visible('#vLw'))
    await pg.keyboard.press('b'); await pg.wait_for_timeout(200); print('lineK:', await pg.evaluate('SET.lineK'), '|', await pg.inner_text('#status'))
    await pg.keyboard.press('Escape')
    await pg.click('#btnClose'); await pg.reload(); await pg.wait_for_timeout(1500)
    await pg.evaluate("(async()=>{const root=await navigator.storage.getDirectory();await openDirHandle(await root.getDirectoryHandle('Изделие 500'));})()"); await pg.wait_for_timeout(1200)
    print('after reopen:', (await pg.inner_text('#treeBody')).replace('\n',' '), '| type', await pg.input_value('#typeSel'), '| status', await pg.inner_text('#status'))
    await pg.click('.tr.all'); await pg.select_option('#typeSel',''); await pg.wait_for_timeout(300)
    await pg.locator('.tile', has_text='02.01').click(); await pg.wait_for_timeout(1000); print('lw btn visible (file without lw):', await pg.is_visible('#vLw'))
    print('errors', errs); await ctx.close()
asyncio.run(main())
