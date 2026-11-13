import asyncio,zipfile,io
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); ctx=await b.new_context(viewport={'width':1500,'height':900},accept_downloads=True); pg=await ctx.new_page()
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.set_input_files('#inFolder','kit/Заказ'); await pg.wait_for_timeout(1500)
    await pg.click('#btnTable'); await pg.wait_for_timeout(2500)
    print('title', await pg.inner_text('#tblTitle'), '|', await pg.inner_text('#tblProg'))
    print((await pg.inner_text('#tblBody')).replace('\t',' | ')[:900])
    print('SUM:', (await pg.inner_text('#tblSum')).replace('\t',' | '))
    await pg.screenshot(path='t50a.png')
    async with pg.expect_download() as dl: await pg.click('#tblXlsx')
    d=await dl.value; path=await d.path(); z=zipfile.ZipFile(path); print('xlsx files', z.namelist()); print(z.read('xl/worksheets/sheet2.xml')[:400])
    import shutil; shutil.copy(path,'t50.xlsx')
    await pg.click('#tblColBtn'); await pg.locator('#tblColMenu input').nth(5).uncheck(); await pg.wait_for_timeout(200); print('cols after uncheck', await pg.locator('#tblBody th').count())
    await pg.locator('#tblMachine').select_option('plasma'); await pg.wait_for_timeout(2500); print('plasma issues col', await pg.evaluate("TBL.rows.map(r=>r.r&&r.r.issues.length)"))
    await pg.locator('#tblBody tr').nth(1).click(); await pg.wait_for_timeout(1200); print('opened', await pg.evaluate('VW.set.map(x=>x.name)'))
    await pg.keyboard.press('c'); await pg.wait_for_timeout(1500); print('chk list:', (await pg.inner_text('#chkList')).replace('\n',' | ')[:400])
    await pg.locator('#chkList .ovl').first.click() if await pg.locator('#chkList .ovl').count() else None
    await pg.wait_for_timeout(300); await pg.screenshot(path='t50b.png')
    await pg.click('#chkList button:has-text("Правила")'); await pg.wait_for_timeout(300); await pg.screenshot(path='t50c.png')
    print('errors',errs); await b.close()
asyncio.run(main())
