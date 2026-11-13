import asyncio, base64, subprocess, os
from playwright.async_api import async_playwright
F1='cmp2/Заказ А/DXF/АБВГ.200001.003-Ст3-3-k1.dxf'; F2='xf/test.dxf'
async def main():
  pass
  errs=[]
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); ctx=await b.new_context(viewport={'width':1400,'height':850}); pg=await ctx.new_page()
    pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('dialog',lambda d:asyncio.ensure_future(d.accept()))
    await pg.add_init_script("localStorage.setItem('dxfv.set',JSON.stringify({click:'1'}))")
    await pg.goto('http://localhost:8765/dxf-viewer/'); await pg.wait_for_timeout(800)
    d1=base64.b64encode(open(F1,'rb').read()).decode(); d2=base64.b64encode(open(F2,'rb').read()).decode()
    await pg.evaluate("""async([a,b])=>{const r=await navigator.storage.getDirectory();for await(const [n] of r.entries())await r.removeEntry(n,{recursive:true});
      const d=await r.getDirectoryHandle('Заказ',{create:true});const s=await d.getDirectoryHandle('DXF',{create:true});
      const put=async(dir,n,b64)=>{const h=await dir.getFileHandle(n,{create:true});const w=await h.createWritable();await w.write(Uint8Array.from(atob(b64),c=>c.charCodeAt(0)));await w.close();};
      await put(s,'деталь.dxf',a);await put(s,'тест.dxf',b);window.__od=d;await openDirHandle(d);}""",[d1,d2])
    await pg.wait_for_timeout(1500)
    print('items',await pg.evaluate('items.map(i=>i.name+":"+!!i.h+!!i.dh)'))
    async def openi(name):
      await pg.evaluate(f"(()=>{{const i=view.findIndex(x=>x.name==='{name}');showItem(i);setFull(true);}})()"); await pg.wait_for_timeout(1000)
    await openi('деталь.dxf')
    bb0=await pg.evaluate('panes[0].doc.bbox.slice()'); o0=await pg.evaluate('panes[0].doc.origin.slice()')
    print('save btn visible',await pg.is_visible('#vXfSave'))
    await pg.keyboard.press('e'); await pg.wait_for_timeout(200)
    await pg.click('#vXfSave'); await pg.wait_for_timeout(200); print('menu:',await pg.inner_text('#xfDesc'),'|',await pg.inner_text('#xfNote'))
    await pg.screenshot(path='t60a.png')
    await pg.click('#xfGo'); await pg.wait_for_timeout(2500)
    print('status',await pg.inner_text('#status'))
    names=await pg.evaluate("(async()=>{const s=await (await window.__od.getDirectoryHandle('DXF'));const o=[];for await(const [n] of s.entries())o.push(n);return o;})()"); print('files',sorted(names))
    print('xf now',await pg.evaluate('JSON.stringify(panes[0].xf)'),'bbox',await pg.evaluate('panes[0].doc.bbox.map(v=>+v.toFixed(3))'), 'old',[round(v,3) for v in bb0], 'orig', await pg.evaluate('panes[0].doc.origin'), o0)
    out=await pg.evaluate("(async()=>{const s=await window.__od.getDirectoryHandle('DXF');const f=await (await s.getFileHandle('деталь.dxf')).getFile();const u=new Uint8Array(await f.arrayBuffer());let t='';for(const c of u)t+=String.fromCharCode(c);return btoa(t);})()")
    open('xf/w1.dxf','wb').write(base64.b64decode(out))
    bk=await pg.evaluate("(async()=>{const s=await window.__od.getDirectoryHandle('DXF');const f=await (await s.getFileHandle('деталь.bak')).getFile();return f.size;})()")
    print('bak size',bk,'orig size',os.path.getsize(F1))
    # зеркало по вертикали на тестовом файле
    await openi('тест.dxf')
    await pg.keyboard.press('Shift+M'); await pg.wait_for_timeout(200)
    print('xf',await pg.evaluate('JSON.stringify(panes[0].xf)'),'chip',await pg.inner_text('.pchip') if await pg.query_selector('.pchip') else '')
    await pg.click('#vXfSave'); await pg.wait_for_timeout(200); print('txtRow visible',await pg.is_visible('#xfTxtRow'))
    await pg.fill('#xfAng','30'); await pg.click('#xfAngL'); await pg.wait_for_timeout(200); print('menu after angle:',await pg.inner_text('#xfDesc'))
    await pg.evaluate("$('xfMenu').hidden=true;panes[0].fit()"); await pg.wait_for_timeout(300); await pg.screenshot(path='t60_pre.png')
    await pg.click('#vXfSave'); await pg.wait_for_timeout(200)
    await pg.click('#xfGo'); await pg.wait_for_timeout(3000); print('status',await pg.inner_text('#status'))
    await pg.evaluate("panes[0].fit()"); await pg.wait_for_timeout(300); await pg.screenshot(path='t60_post.png')
    out=await pg.evaluate("(async()=>{const s=await window.__od.getDirectoryHandle('DXF');const f=await (await s.getFileHandle('тест.dxf')).getFile();const u=new Uint8Array(await f.arrayBuffer());let t='';for(const c of u)t+=String.fromCharCode(c);return btoa(t);})()")
    open('xf/w2.dxf','wb').write(base64.b64decode(out))
    await pg.screenshot(path='t60b.png')
    await b.close()
  print('errors',errs)
asyncio.run(main())
