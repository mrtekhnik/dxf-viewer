# размеры мелких отверстий: в просмотре текст размера не меньше 7 px; «Размеры: скрыть» прячет и текст
import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1400,'height':800})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.set_input_files('#inFolder','dimsmall'); await pg.wait_for_timeout(1500)
    await pg.locator('.tile').first.dblclick(); await pg.wait_for_timeout(2000)
    # перехват fillText: какие надписи и каким кеглем рисуются в окне просмотра
    js="""(()=>{const p=panes[0],out=[];const P=CanvasRenderingContext2D.prototype,f=P.fillText;P.fillText=function(t,x,y){out.push([t,parseFloat(this.font)]);return f.apply(this,arguments);};try{p.paint();}finally{P.fillText=f;}return [p.s,out];})()"""
    s,out=await pg.evaluate(js); print('масштаб',round(s,3),out)
    small=[o for o in out if '6' in o[0] or 'Ø' in o[0] or '%%c' in o[0]]
    if not small: errs.append('нет текста размера отверстия: '+str(out))
    elif min(o[1] for o in small)<9.5: errs.append('мелко: '+str(small))
    await pg.evaluate("SET.dims=false;0"); s,out2=await pg.evaluate(js); print('скрыть:',out2)
    if out2: errs.append('при «скрыть» текст остался')
    print('errors',errs); await b.close()
asyncio.run(main())
