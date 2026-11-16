# Проверка перед резкой: правила применяются сразу при вводе и запоминаются (все правки подряд, после перезапуска)
import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); ctx=await b.new_context(viewport={'width':1400,'height':850}); pg=await ctx.new_page(); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.set_input_files('#inFiles',['xf2/A/DXF/АЮИА.100-01.01-St-3-K1.dxf']); await pg.wait_for_timeout(1500)
    await pg.evaluate('showItem(0);setFull(true)'); await pg.wait_for_timeout(1200)
    await pg.click('#vChk'); await pg.wait_for_timeout(1500)
    n0=await pg.evaluate('panes[0].chk&&panes[0].chk.r&&panes[0].chk.r.issues.length'); print('issues',n0)
    await pg.evaluate('rulesOpen()'); await pg.wait_for_timeout(300)
    inp=pg.locator('#rulesBody input[type=number]')
    # отверстие не меньше: 8 × s = 24 мм > Ø20 → замечания должны появиться без потери фокуса
    await inp.nth(0).fill('8'); await pg.wait_for_timeout(1200)
    n1=await pg.evaluate('panes[0].chk&&panes[0].chk.r&&panes[0].chk.r.issues.length'); print('after holeK=8',n1)
    if not (n1 and n1>(n0 or 0)): errs.append('правило не применилось сразу: %s -> %s'%(n0,n1))
    await inp.nth(1).fill('2.5'); await inp.nth(2).fill('3.3'); await pg.wait_for_timeout(800)
    saved=await pg.evaluate("(()=>{const r=JSON.parse(localStorage.getItem('dxfv.set')).rules;return r.P[r.m]})()")
    print('saved',saved['holeK'],saved['holeAbs'],saved['webK'])
    if (saved['holeK'],saved['holeAbs'],saved['webK'])!=(8,2.5,3.3): errs.append('не все правки сохранены: '+str([saved['holeK'],saved['holeAbs'],saved['webK']]))
    await pg.reload(); await pg.wait_for_timeout(800)
    v=await pg.evaluate("(()=>{const r=rules();return [r.P[r.m].holeK,r.P[r.m].holeAbs,r.P[r.m].webK]})()"); print('after reload',v)
    if v!=[8,2.5,3.3]: errs.append('после перезапуска: '+str(v))
    await pg.evaluate("(()=>{const r=rules();r.P[r.m]=Object.assign({},RULE_DEF[r.m]);saveSet();})()")
    print('errors',errs); await b.close()
asyncio.run(main())
