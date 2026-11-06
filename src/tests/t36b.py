import asyncio
from playwright.async_api import async_playwright
JS="""(()=>{const src=document.createElement('canvas');src.width=400;src.height=200;const g=src.getContext('2d');g.fillStyle='#fff';g.fillRect(0,0,400,200);
 g.strokeStyle='#000';for(let i=0;i<30;i++){g.lineWidth=0.15+i*0.02;g.beginPath();g.moveTo(5+i*13,5);g.lineTo(12+i*13,195);g.stroke();}
 const out={};const F={'old0':'','old2 contrast1.9':'contrast(1.9) saturate(0.8)','old4 contrast3.5':'contrast(3.5) saturate(0.6)'};
 for(const k of [-1,0,1,2,3])F['new '+k]='url(#pdflv'+k+')';
 for(const n in F){const c=document.createElement('canvas');c.width=400;c.height=200;const x=c.getContext('2d');x.filter=F[n]||'none';x.drawImage(src,0,0);
   const d=x.getImageData(0,0,400,200).data;let vis=0,sum=0;for(let i=0;i<d.length;i+=4){const v=d[i];if(v<200)vis++;sum+=255-v;}out[n]=[vis,Math.round(sum/1000)];}
 return out;})()"""
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page()
    await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.wait_for_timeout(500)
    for k,v in (await pg.evaluate(JS)).items(): print(k,v)
    await b.close()
asyncio.run(main())
