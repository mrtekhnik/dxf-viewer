# телефон: панели, свайпы ← → файлы, ↑ ↓ страницы, края экрана, лист не ёрзает, щипок, шапка «⋯»
import asyncio,glob,os
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); ctx=await b.new_context(**p.devices['Pixel 5']); pg=await ctx.new_page()
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    cdp=await ctx.new_cdp_session(pg)
    async def touch(pts_seq,dt=16):
      # pts_seq: список кадров; кадр — список точек (x,y)
      prev=0
      for i,fr in enumerate(pts_seq):
        typ='touchStart' if i==0 else ('touchEnd' if i==len(pts_seq)-1 else 'touchMove')
        if typ=='touchEnd': await cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
        else: await cdp.send('Input.dispatchTouchEvent',{'type':typ,'touchPoints':[{'x':x,'y':y,'id':k} for k,(x,y) in enumerate(fr)]})
        await asyncio.sleep(dt/1000)
    async def swipe(x0,y0,x1,y1,n=8):
      await touch([[(x0+(x1-x0)*i/n,y0+(y1-y0)*i/n)] for i in range(n+1)]+[[]]); await pg.wait_for_timeout(700)
    async def tap(x,y): await touch([[(x,y)],[]],dt=30); 
    await pg.goto('file:///home/claude/dxf-viewer.html')
    fs=sorted(f for f in glob.glob('tree/Изделие 320/**/*.*',recursive=True) if os.path.isfile(f))+['dxf/деталь_01.pdf','blk/many.pdf']
    await pg.set_input_files('#inFiles',fs); await pg.wait_for_timeout(2500)
    print('mui',await pg.evaluate("document.body.classList.contains('mui')"),'header menu',await pg.is_visible('#mHMenu'),'pins hidden',not await pg.is_visible('#btnPins'),'brand',await pg.is_visible('.brand'))
    await pg.tap('#mHMenu'); await pg.wait_for_timeout(300); print('sheet pins visible',await pg.is_visible('#btnPins'),await pg.is_visible('#btnSet'))
    await pg.screenshot(path='m1_head.png'); await pg.tap('.brand'); await pg.wait_for_timeout(300); print('sheet closed', not await pg.is_visible('#btnSet'))
    await pg.locator('.tile').first.tap(); await pg.wait_for_timeout(2000)
    print('viewer full',await pg.evaluate('VW.full'),'ui shown',await pg.evaluate("document.body.classList.contains('mui-ui')"),'cont off',await pg.evaluate('!panes[0].cont'))
    await pg.screenshot(path='m2_ui.png')
    await pg.wait_for_timeout(2700); print('auto-hidden',not await pg.evaluate("document.body.classList.contains('mui-ui')"))
    W,H=393,727
    s0=await pg.evaluate('[panes[0].cx,panes[0].cy,panes[0].s]')
    await touch([[(200,400)],[(215,415)],[(230,430)],[(240,440)],[]]); await pg.wait_for_timeout(300)
    print('no drift when fitted', s0==await pg.evaluate('[panes[0].cx,panes[0].cy,panes[0].s]'))
    i0=await pg.evaluate('VW.idx'); await swipe(330,400,80,410); print('swipe left -> idx',i0,'->',await pg.evaluate('VW.idx'))
    await swipe(80,400,330,410); print('swipe right -> idx',await pg.evaluate('VW.idx'))
    await tap(370,400); await pg.wait_for_timeout(900); print('tap right edge ->',await pg.evaluate('VW.idx'))
    await tap(20,400); await pg.wait_for_timeout(900); print('tap left edge ->',await pg.evaluate('VW.idx'))
    await tap(200,400); await pg.wait_for_timeout(600); print('tap center -> ui',await pg.evaluate("document.body.classList.contains('mui-ui')"))
    await tap(200,400); await pg.wait_for_timeout(600); print('tap center -> ui',await pg.evaluate("document.body.classList.contains('mui-ui')"))
    # многостраничный PDF
    n=await pg.evaluate("view.findIndex(x=>x.name==='деталь_01.pdf')"); await pg.evaluate(f'showItem({n})'); await pg.wait_for_timeout(1500)
    print('pages',await pg.evaluate('panes[0].doc.pages'),'page',await pg.evaluate('panes[0].pageNo'))
    await swipe(200,600,205,250); print('swipe up -> page',await pg.evaluate('panes[0].pageNo'),'idx same',await pg.evaluate('VW.idx')==n)
    await swipe(200,250,205,600); print('swipe down -> page',await pg.evaluate('panes[0].pageNo'))
    await tap(200,700); await pg.wait_for_timeout(500); print('tap bottom -> page',await pg.evaluate('panes[0].pageNo'))
    await tap(200,30); await pg.wait_for_timeout(500); print('tap top -> page',await pg.evaluate('panes[0].pageNo'))
    # двойное касание — приблизить, перетаскивание с ограничением, двойное — вписать
    await tap(200,400); await pg.wait_for_timeout(80); await tap(200,400); await pg.wait_for_timeout(500)
    z=await pg.evaluate('[panes[0].fitted,panes[0].s/panes[0].fitView().s]'); print('double tap zoom',z)
    R="(()=>{const p=panes[0],e=p.pg[0],s=p.s,L=p.W/2+(e.ox-p.cx)*s,T=p.H/2-((p.ph-e.oy)-p.cy)*s;return [L,T,L+e.w*s,T+e.h*s,p.W,p.H]})()"
    for (a,b_,c,d) in [(200,400,-600,-600),(200,400,900,1200),(200,300,200,-900),(200,300,200,1500)]:
      await swipe(a,b_,c,d,n=12); r=await pg.evaluate(R)
      ok=(r[2]-r[0]<=r[4]+1 or (r[0]<=11 and r[2]>=r[4]-11)) and (r[3]-r[1]<=r[5]+1 or (r[1]<=11 and r[3]>=r[5]-11))
      if not ok: errs.append('page left screen: '+str([round(v) for v in r]))
    print('clamped to page edges', not any('page left' in e for e in errs))
    await pg.evaluate('(()=>{const p=panes[0];const f=p.fitView();p.cx=f.cx;p.cy=f.cy;p.draw();})()'); await pg.wait_for_timeout(100)
    c0=await pg.evaluate('panes[0].cx'); await touch([[(200+i*12,400)] for i in range(6)]+[[]],dt=12); c1=await pg.evaluate('panes[0].cx'); await pg.wait_for_timeout(500); c2=await pg.evaluate('panes[0].cx')
    print('zoomed fling', c1!=c0 and c2!=c1)
    await tap(200,400); await pg.wait_for_timeout(80); await tap(200,400); await pg.wait_for_timeout(500); print('double tap fit',await pg.evaluate('panes[0].fitted'))
    # щипок
    await touch([[(150,400),(250,400)],[(130,400),(270,400)],[(100,400),(300,400)],[(60,400),(340,400)],[]]); await pg.wait_for_timeout(400)
    print('pinch zoom',await pg.evaluate('panes[0].fitted'),round(await pg.evaluate('panes[0].s/panes[0].fitView().s'),2))
    await touch([[(60,400),(340,400)],[(150,400),(250,400)],[(190,400),(210,400)],[]]); await pg.wait_for_timeout(400)
    print('pinch back -> fitted',await pg.evaluate('panes[0].fitted'))
    # нижняя панель и «⋯»
    await tap(200,400); await pg.wait_for_timeout(600)
    await pg.tap('#mMore'); await pg.wait_for_timeout(300); print('sheet visible',await pg.is_visible('#vLoupe'),await pg.is_visible('#vTxt'))
    await pg.screenshot(path='m3_sheet.png')
    await pg.evaluate("document.body.classList.remove('mui-sheet')"); await pg.wait_for_timeout(100)
    print('text in menu, not bottom:', await pg.is_hidden('#mTool'), '| top cont btn', await pg.is_visible('#mCont'))
    m=await pg.evaluate("view.findIndex(x=>x.name==='many.pdf')"); await pg.evaluate(f'showItem({m})'); await pg.wait_for_timeout(1500); n=m
    await pg.evaluate('muiUi(true)'); await pg.wait_for_timeout(200)
    await pg.tap('#mCont'); await pg.wait_for_timeout(1500); print('cont on',await pg.evaluate('panes[0].cont'))
    await pg.evaluate("document.body.classList.remove('mui-sheet','mui-ui')")
    cy0=await pg.evaluate('panes[0].cy'); await touch([[(200,500-i*15)] for i in range(6)]+[[]],dt=12); cy1=await pg.evaluate('panes[0].cy'); await pg.wait_for_timeout(600); cy2=await pg.evaluate('panes[0].cy')
    print('dbg', await pg.evaluate('[MT.vx,MT.vy,performance.now()-MT.pt,MT.fl,panes[0].cont,panes[0].fitted]'), cy0,cy1,cy2)
    print('cont scroll moved', cy1!=cy0, 'fling continued', cy2!=cy1, 'idx same', await pg.evaluate(f'VW.idx')==n)
    await pg.evaluate("muiUi(true)"); await pg.wait_for_timeout(200)
    await pg.tap('#mCont'); await pg.wait_for_timeout(1200); print('cont off',not await pg.evaluate('panes[0].cont'))
    await pg.evaluate("SET.flashT='off';flash('проверка')"); print('flash off -> no toast', not await pg.evaluate("$('status').classList.contains('flash')"))
    await pg.evaluate("SET.flashT='2';flash('проверка')"); await pg.wait_for_timeout(2300); print('flash 2s gone', not await pg.evaluate("$('status').classList.contains('flash')"))
    await pg.evaluate("document.body.classList.remove('mui-sheet')")
    await pg.tap('#mClose') if await pg.is_visible('#mClose') else None
    await pg.wait_for_timeout(500); print('closed',not await pg.evaluate('VW.full'))
    print('errors',errs); await b.close()
asyncio.run(main())
