import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1300,'height':800})
    await pg.add_init_script("try{const s=JSON.parse(localStorage.getItem('dxfv.set')||'{}');if(s.click===undefined){s.click='1';localStorage.setItem('dxfv.set',JSON.stringify(s))}}catch(e){}")
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.wait_for_timeout(800)
    await pg.evaluate("""(()=>{const now=Date.now(),H=3600e3;
      const f=(t,path,root,rn)=>histPush({t,kind:'file',name:path.split('/').pop(),path,type:/pdf$/.test(path)?'pdf':'dxf',root,rootName:rn});
      histPush({t:now-30*H,kind:'folder',name:'Изделие 320',path:'',type:'',root:'r1',rootName:'Изделие 320',count:246});
      f(now-29*H,'Изделие 320/02 Рама/02.01 Боковина/АЮИА.320-02.01 Боковина.pdf','r1','Изделие 320');
      f(now-29*H+60e3,'Изделие 320/02 Рама/02.01 Боковина/DXF/АЮИА.320-02.01-St-8-k2.dxf','r1','Изделие 320');
      histPush({t:now-2*H,kind:'folder',name:'Изделие 415',path:'',type:'',root:'r2',rootName:'Изделие 415',count:58});
      f(now-2*H+60e3,'Изделие 415/02 Рама/02.01 Боковина/АЮИА.415-02.01 Боковина.pdf','r2','Изделие 415');
      f(now-H,'Изделие 415/02 Рама/02.01 Боковина/DXF/АЮИА.415-02.01-St-8-k2.dxf','r2','Изделие 415');
      f(now-H/2,'Изделие 415/03 Крышка/АЮИА.415-03 Крышка.pdf','r2','Изделие 415');
      f(now-H/3,'Изделие 415/АЮИА.415.00 СБ.pdf','r2','Изделие 415');})()""")
    await pg.click('#btnHist'); await pg.select_option('#hView','group'); await pg.wait_for_timeout(300)
    print((await pg.inner_text('#hBody')).replace('\n',' | '))
    await pg.screenshot(path='hgroup.png')
    await pg.locator('.hg.proj', has_text='Изделие 320').click(); await pg.wait_for_timeout(200)
    print('after expand 320 rows:', await pg.locator('.hg').count())
    await pg.fill('#hSearch','крышка'); await pg.wait_for_timeout(200); print('search:', (await pg.inner_text('#hBody')).replace('\n',' | '))
    print('errors', errs); await b.close()
asyncio.run(main())
