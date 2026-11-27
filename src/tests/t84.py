# подписи Ø: все отверстия (мелкие тоже) без наложения + сводка; «только крупные»; подписи в лупе
import asyncio
from playwright.async_api import async_playwright
CAP="""(()=>{const out=[];const P=CanvasRenderingContext2D.prototype,f=P.fillText;P.fillText=function(t){out.push(String(t));return f.apply(this,arguments);};try{panes[0].paint();}finally{P.fillText=f;}return out;})()"""
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1400,'height':800})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.set_input_files('#inFolder','holes'); await pg.wait_for_timeout(1500)
    await pg.locator('.tile').first.dblclick(); await pg.wait_for_timeout(1500)
    await pg.evaluate("SET.mholes=true;SET.mhSmall='sum';0"); await pg.keyboard.press('d'); await pg.wait_for_timeout(400)
    t=await pg.evaluate(CAP); lab=[x for x in t if x.startswith('Ø')]; summ=[x for x in t if x.startswith('Отверстия')]
    print('подписей',len(lab),'сводка',summ)
    summ=[x for x in t if x.startswith('Ø') and '×' in x]
    if len(lab)-len(summ)>4: errs.append('цвет по диаметру: лишние цифры у мелких: '+str(lab))
    if 'Ø5,0  ×40' not in summ: errs.append('сводка: '+str(summ))
    await pg.evaluate("SET.mhSmall='all';0"); t=await pg.evaluate(CAP); la=[x for x in t if x.startswith('Ø')]; print('цифры у всех',len(la))
    if len(la)<30: errs.append('мало подписей в «у всех»: '+str(len(la)))
    await pg.evaluate("SET.mhSmall='big';0"); t=await pg.evaluate(CAP); lab2=[x for x in t if x.startswith('Ø')]; print('только крупные',lab2)
    if len(lab2)>2: errs.append('«крупные»: '+str(t))
    # лупа над мелким отверстием
    await pg.evaluate("SET.mhSmall='sum';0")
    pos=await pg.evaluate("(()=>{const p=panes[0],e=measEntP(p).E.find(e=>e.t==='C'&&e.r<3),q=m2s(p,e.cx,e.cy),r=p.cv.getBoundingClientRect();return [r.left+q[0],r.top+q[1]]})()")
    await pg.click('#vLoupe'); await pg.mouse.move(pos[0],pos[1]+20); await pg.mouse.click(pos[0],pos[1]+20); await pg.wait_for_timeout(300)
    await pg.mouse.move(pos[0]+1,pos[1]+20); await pg.wait_for_timeout(500)
    t=await pg.evaluate("""(()=>{const out=[];const P=CanvasRenderingContext2D.prototype,f=P.fillText;P.fillText=function(t){out.push(String(t));return f.apply(this,arguments);};try{loupeDraw();}finally{P.fillText=f;}return out;})()""")
    print('в лупе',t)
    if not any(x.startswith('Ø5') for x in t): errs.append('в лупе нет подписи: '+str(t))
    print('errors',errs); await b.close()
asyncio.run(main())
