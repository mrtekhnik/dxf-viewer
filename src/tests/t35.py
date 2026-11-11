import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1300,'height':800})
    await pg.add_init_script("try{const s=JSON.parse(localStorage.getItem('dxfv.set')||'{}');if(s.click===undefined){s.click='1';localStorage.setItem('dxfv.set',JSON.stringify(s))}}catch(e){}")
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.set_input_files('#inFolder','tree/Изделие 320'); await pg.wait_for_timeout(1500)
    st="(()=>({dir:curDir,zone:KB.zone,idx:VW.idx,shown:VW.set.length?VW.set[0].name:'',tiles:[...$('grid').children].map(t=>(t.classList.contains('cur')?'*':'')+(t._it?t._it.name.slice(0,14):'['+t.querySelector('.nm').textContent+']')).slice(0,7)}))()"
    for mode in ['grid','dock']:
      if mode=='dock': await pg.click('#btnPreview'); await pg.wait_for_timeout(500)
      else: await pg.click('#btnBrowse')
      await pg.wait_for_timeout(300)
      await pg.locator('.ftile', has_text='02 Рама').click(); await pg.wait_for_timeout(400)
      await pg.locator('.ftile.up').click(); await pg.wait_for_timeout(400); print(mode,'mouse up:', await pg.evaluate(st))
      for k in (['ArrowRight','ArrowRight','Enter'] if mode=='grid' else ['ArrowRight','Enter']): await pg.keyboard.press(k); await pg.wait_for_timeout(250)
      print(mode,'→→Enter:', await pg.evaluate(st))
      for k in ['ArrowRight','ArrowRight']: await pg.keyboard.press(k); await pg.wait_for_timeout(250)
      print(mode,'→→:', await pg.evaluate(st))
      await pg.keyboard.press('Backspace'); await pg.wait_for_timeout(300); await pg.keyboard.press('ArrowLeft'); await pg.wait_for_timeout(250)
      print(mode,'Bksp ←:', await pg.evaluate(st))
      if mode=='grid':
        await pg.keyboard.press('Escape'); await pg.wait_for_timeout(300)
    print('errors', errs); await b.close()
asyncio.run(main())
