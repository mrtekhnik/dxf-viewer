# Выбор папки: AbortError — сообщение с кнопкой запасного способа; подпапка с ошибкой — остальное прочитано;
# файл с ошибкой getFile — в «не прочитано»; всё — в журнале
import asyncio, base64
from playwright.async_api import async_playwright
D1=base64.b64encode(open('xf2/A/DXF/АЮИА.100-01.01-St-3-K1.dxf','rb').read()).decode()
async def main():
  errs=[]
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1400,'height':850}); pg.on('pageerror',lambda e:errs.append(str(e)))
    await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.wait_for_timeout(500)
    # 1) окно выбора бросает AbortError
    await pg.evaluate("window.showDirectoryPicker=async()=>{throw new DOMException('The user aborted a request.','AbortError')};window.__clicked=0;$('inFolder').click=()=>{window.__clicked++};$('inCmp').click=()=>{window.__clicked+=10};0")   # ;0 — иначе Playwright вызовет присвоенную функцию
    await pg.evaluate("$('btnFolder').click()"); await pg.wait_for_timeout(300)
    vis=await pg.is_visible('#noteBox'); t=await pg.inner_text('#noteBox'); print('abort note:',vis,t.replace('\n',' | ')[:160])
    if not vis or 'Открыть другим способом' not in t or 'перетащить' not in t: errs.append('нет сообщения при AbortError')
    await pg.click('#noteB .pri'); await pg.wait_for_timeout(100)
    if await pg.evaluate('window.__clicked')!=1: errs.append('кнопка запасного способа не открыла inFolder')
    await pg.evaluate("$('cmpPick').click()"); await pg.wait_for_timeout(300); await pg.click('#noteB .pri')
    if await pg.evaluate('window.__clicked')!=11: errs.append('сравнение: кнопка не открыла inCmp')
    # 2)+3) папка: подпапка «Сломанная» не читается, один файл не читается
    await pg.evaluate("""(b64)=>{const bytes=Uint8Array.from(atob(b64),c=>c.charCodeAt(0));
      const F=(name,bad)=>({kind:'file',name,getFile:async()=>{if(bad)throw new DOMException('A requested file or directory could not be found','NotFoundError');return new File([bytes],name,{lastModified:1700000000000});}});
      const Dd=(name,list,bad)=>({kind:'directory',name,entries:async function*(){if(bad)throw new DOMException('Access is denied','NotAllowedError');for(const x of list)yield [x.name,x];}});
      window.__root=Dd('Заказ',[F('a1.dxf'),F('a2.dxf',true),Dd('Сломанная',[F('x.dxf')],true),Dd('Хорошая',[F('b1.dxf'),F('b2.dxf')])]);}""",D1)
    await pg.evaluate("window.showDirectoryPicker=async()=>window.__root"); await pg.evaluate("$('btnFolder').click()"); await pg.wait_for_timeout(1500)
    n=await pg.evaluate('items.map(i=>i.path).sort()'); print('files',n)
    if n!=['Заказ/a1.dxf','Заказ/Хорошая/b1.dxf','Заказ/Хорошая/b2.dxf']: errs.append('прочитаны не все доступные файлы: '+str(n))
    t=await pg.inner_text('#noteBox'); print('unread note:',t.replace('\n',' | ')[:300])
    if 'Не прочитано файлов: 1, папок: 1' not in t or 'a2.dxf' not in t or 'Сломанная' not in t: errs.append('нет списка непрочитанного: '+t)
    await pg.locator('#noteB button',has_text='Журнал').click(); await pg.wait_for_timeout(300)
    lg=await pg.inner_text('#logBody'); print('log:',lg.replace('\n',' | ')[:500])
    for w in ['Открыто окно выбора папки','Выбор прерван','Chrome вернул папку «Заказ»','прочитано файлов 3, ошибок 2','Сломанная','a2.dxf']:
      if w not in lg: errs.append('в журнале нет: '+w)
    await pg.evaluate("$('logPanel').hidden=true")
    # 4) корень не читается — общая ошибка с кнопкой (не автоматический click)
    await pg.evaluate("window.__clicked=0;window.showDirectoryPicker=async()=>({kind:'directory',name:'Сеть',entries:async function*(){throw new DOMException('Access is denied','NotAllowedError')}})")
    await pg.evaluate("$('btnFolder').click()"); await pg.wait_for_timeout(600)
    t=await pg.inner_text('#noteBox'); print('root fail:',t.replace('\n',' | ')[:200])
    if 'не читается' not in t or 'NotAllowedError' not in t or await pg.evaluate('window.__clicked')!=0: errs.append('ошибка корня: '+t)
    await b.close()
  print('errors',errs)
asyncio.run(main())
