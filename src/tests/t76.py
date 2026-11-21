# лупа: участок с запасом — движение рисуется из запаса быстро и совпадает с точной отрисовкой (DXF и PDF)
import asyncio
from playwright.async_api import async_playwright
CMPJS="""(()=>{const p=LOUPE.p,R=LR(),d=devicePixelRatio||1,k=LOUPE.k,L=$('loupe');
  const c=document.createElement('canvas');c.width=c.height=2*R*d;const x=c.getContext('2d');
  if(!p.isPdf){const [wx,wy]=p.s2w(LOUPE.x,LOUPE.y);x.fillStyle=dxfBg();x.fillRect(0,0,c.width,c.height);renderDoc(x,p.doc,{s:p.s*k,cx:wx,cy:wy,W:2*R,H:2*R,dpr:d,xf:p.xf,hidden:p.hidden,lw:SET.lw,texts:SET.texts,k:SET.lineK});}
  const a=L.getContext('2d').getImageData(R*d-40,R*d-60,80,40).data,b=x.getImageData(R*d-40,R*d-60,80,40).data;let n=0;for(let i=0;i<a.length;i+=4)if(Math.abs(a[i]-b[i])+Math.abs(a[i+1]-b[i+1])+Math.abs(a[i+2]-b[i+2])>60)n++;return n/(a.length/4);})()"""
async def run(pg,folder,name,errs,pdf):
  await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.set_input_files('#inFolder',folder); await pg.wait_for_timeout(1500)
  await pg.locator('.tile', has_text=name).first.dblclick(); await pg.wait_for_timeout(2500)
  bb=await pg.locator('#stage canvas').first.bounding_box()
  await pg.click('#vLoupe'); await pg.mouse.move(bb['x']+500,bb['y']+300); await pg.mouse.click(bb['x']+500,bb['y']+300); await pg.wait_for_timeout(1500)
  await pg.evaluate("window._lt=[];const f=loupeDraw;loupeDraw=function(){const t=performance.now();f();_lt.push(performance.now()-t);};0")
  for i in range(30): await pg.mouse.move(bb['x']+500+i*2,bb['y']+300+i); await pg.wait_for_timeout(16)
  await pg.wait_for_timeout(1200)
  r=await pg.evaluate("[_lt.length,_lt.slice(1).reduce((a,b)=>a+b,0)/Math.max(1,_lt.length-1),Math.max(..._lt),!!LC.cv,loupeHas(LOUPE.p,LOUPE.x,LOUPE.y,LOUPE.k,LR(),loupeSig(LOUPE.p,LOUPE.k,devicePixelRatio||1))]")
  print(name,'вызовов',r[0],'среднее мс',round(r[1],2),'макс',round(r[2],1),'запас',r[3],'курсор в запасе',r[4])
  if not r[3] or not r[4]: errs.append(name+': нет запаса '+str(r))
  if r[1]>8: errs.append(name+': медленно '+str(r[1]))
  if not pdf:
    diff=await pg.evaluate(CMPJS); print(' отличие от точной отрисовки',diff)
    if diff>0.02: errs.append(name+': картинка не совпадает '+str(diff))
  else:
    # PDF: точный участок — то же, что старая отрисовка страницы в этом месте
    diff=await pg.evaluate("""(async()=>{const p=LOUPE.p,R=LR(),d=devicePixelRatio||1,k=LOUPE.k,s=p.s*k,[wx,wy]=p.s2w(LOUPE.x,LOUPE.y);
      const e=p.pg.find(e=>{const y=p.ph-wy;return y>=e.oy-1&&y<=e.oy+e.h+1;});const S=s*d,x0=wx-e.ox-R/s,y0=(p.ph-wy)-e.oy-R/s;
      const c=document.createElement('canvas');c.width=c.height=2*R*d;await e.page.render({canvasContext:c.getContext('2d'),viewport:e.page.getViewport({scale:S,rotation:e.rot,offsetX:-x0*S,offsetY:-y0*S})}).promise;
      const a=$('loupe').getContext('2d').getImageData(R*d-40,R*d-60,80,40).data,b=c.getContext('2d').getImageData(R*d-40,R*d-60,80,40).data;let n=0;for(let i=0;i<a.length;i+=4)if(Math.abs(a[i]-b[i])+Math.abs(a[i+1]-b[i+1])+Math.abs(a[i+2]-b[i+2])>60)n++;return n/(a.length/4);})()""")
    print(' отличие от точной отрисовки',diff)
    if diff>0.03: errs.append(name+': картинка не совпадает '+str(diff))
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1400,'height':850})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await run(pg,'dxf','большой_60k',errs,False)
    await run(pg,'pair','Корпус.pdf',errs,True)
    print('errors',errs); await b.close()
asyncio.run(main())
