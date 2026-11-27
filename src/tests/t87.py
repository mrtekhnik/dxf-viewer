# этап Б: виды размеров как в AutoCAD, «Измерить» (линейка), тема AutoCAD, меню ⤴ (поделиться, сохранить, перетащить)
import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1400,'height':800})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.set_input_files('#inFolder','holes'); await pg.wait_for_timeout(1500)
    await pg.locator('.tile').filter(has_text='Лист с отв').first.dblclick(); await pg.wait_for_timeout(1500)
    opts=await pg.evaluate("[...$('measMode').options].map(o=>o.textContent)"); print('виды',opts)
    for n in ['Линейный','Параллельный','Угловой','Длина дуги','Радиус','Диаметр']:
      if n not in opts: errs.append('нет вида '+n)
    await pg.keyboard.press('d'); await pg.wait_for_timeout(200)
    P="""(()=>{const p=panes[0],r=p.cv.getBoundingClientRect(),b=p.doc.bbox;window._sc=(x,y)=>{const q=m2s(p,b[0]+x,b[1]+y);return [r.left+q[0],r.top+q[1]];};return 1})()"""
    await pg.evaluate(P)
    async def clk(x,y,dx=0,dy=0):
      q=await pg.evaluate(f"_sc({x},{y})"); await pg.mouse.move(q[0]+dx,q[1]+dy); await pg.wait_for_timeout(40); await pg.mouse.click(q[0]+dx,q[1]+dy); await pg.wait_for_timeout(120)
    last="(()=>{const M=msOf(panes[0]),it=M.items[M.items.length-1];return it?{t:it.t,dir:it.dir,k:it.k||null,txt:measText(it).main}:null})()"
    # Диаметр по окружности Ø46 (центр 800,550 r 23)
    await pg.evaluate("SET.mmode='dia';0"); await clk(823,550)
    await clk(860,600)
    r=await pg.evaluate(last); print('диаметр',r)
    if not r or r['k']!='D' or 'Ø46' not in r['txt']: errs.append('Диаметр: '+str(r))
    await pg.evaluate("SET.mmode='rad';0"); await clk(823,550); await clk(860,500)
    r=await pg.evaluate(last); print('радиус',r)
    if not r or r['k']!='R' or 'R23' not in r['txt']: errs.append('Радиус: '+str(r))
    # Линейный: точки по диагонали, курсор между ними — всё равно гор./верт.
    await pg.evaluate("SET.mmode='lin';0"); await clk(0,0); await clk(1700,1100); await clk(850,560)
    r=await pg.evaluate(last); print('линейный',r)
    if not r or r['dir'] not in ('h','v'): errs.append('Линейный: '+str(r))
    await pg.evaluate("SET.mmode='ali';0"); await clk(0,0); await clk(1700,1100); await clk(400,800)
    r=await pg.evaluate(last); print('параллельный',r)
    if not r or r['dir']!='al': errs.append('Параллельный: '+str(r))
    # Измерить: показывается только последнее, на выходе пропадает
    await pg.evaluate('measToggle(false);0'); await pg.wait_for_timeout(200)
    await pg.evaluate("msOf(panes[0]).items.length=0;0")
    await pg.keyboard.press('u'); await pg.wait_for_timeout(200); await pg.evaluate(P)
    st=await pg.evaluate("[MEAS.on,MEAS.ruler,$('vRuler').classList.contains('on'),$('measBox').hidden]"); print('линейка',st)
    if st!=[True,True,True,True]: errs.append('линейка не включилась: '+str(st))
    await clk(0,0); await clk(1700,0); await clk(0,0); await clk(0,1100)
    r=await pg.evaluate("msOf(panes[0]).items.map(i=>[i.t,Math.round(Math.hypot(i.b[0]-i.a[0],i.b[1]-i.a[1]))])"); print('измерения',r)
    if r!=[['dist',1100]]: errs.append('линейка: '+str(r))
    await pg.click('#vRuler'); await pg.wait_for_timeout(200)
    r=await pg.evaluate("[MEAS.on,(panes[0].ms&&panes[0].ms.items.length)||0]")
    if r[0]: errs.append('линейка не выключилась')
    # тема AutoCAD
    await pg.evaluate("SET.theme='acad';applyTheme();bgChanged&&bgChanged();0"); await pg.wait_for_timeout(300)
    t=await pg.evaluate("[document.documentElement.dataset.theme,dxfBg(),getComputedStyle(document.body).backgroundColor]"); print('тема',t)
    if t[0]!='acad' or t[1]!='#212830': errs.append('тема: '+str(t))
    # меню ⤴
    await pg.click('#vShare'); await pg.wait_for_timeout(200)
    m=await pg.evaluate("[$('shareMenu').hidden,$('shTab').hidden,!!$('shDrag')]"); print('меню',m)
    if m[0] or not m[1]: errs.append('меню ⤴: '+str(m))
    await pg.evaluate("window._saved=null;window.showSaveFilePicker=async o=>({name:o.suggestedName,createWritable:async()=>({write:async f=>{window._saved=[o.suggestedName,f.size]},close:async()=>{}})});0")
    await pg.click('#shSave'); await pg.wait_for_timeout(500)
    sv=await pg.evaluate("[window._saved,curItem().file.size]"); print('сохранить',sv)
    if not sv[0] or sv[0][1]!=sv[1]: errs.append('сохранить копию: '+str(sv))
    d=await pg.evaluate("""(()=>{const dt=new DataTransfer();const ev=new DragEvent('dragstart',{dataTransfer:dt,bubbles:true});$('shDrag').dispatchEvent(ev);return dt.getData('DownloadURL');})()""")
    print('перетащить',d[:60])
    if not d.startswith('application/dxf:Лист с отв.dxf:blob:'): errs.append('DownloadURL: '+d)
    print('errors',errs); await b.close()
asyncio.run(main())
