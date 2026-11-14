# «иероглифы» cp1251: русский и украинский, знаки чертежа не портятся
import asyncio
from playwright.async_api import async_playwright
EXP='1. *Розміри для довідок.\n2. Гострі крайки притупити.\n3. Їх шліфувати, ґрунт та є\nПлита основи\nØ20 2×45° ±0,1 Ra 12,5'
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1400,'height':900}); errs=[]
    pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.set_input_files('#inFiles',['blk/txt_uk.pdf']); await pg.wait_for_timeout(2000)
    await pg.keyboard.press('t'); await pg.keyboard.press('Control+a'); await pg.wait_for_timeout(1200)
    t=await pg.input_value('#txtArea')
    if t!=EXP: errs.append('text: '+repr(t))
    print('errors',errs); await b.close()
asyncio.run(main())
