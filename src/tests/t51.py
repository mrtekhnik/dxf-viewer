import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1300,'height':850})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file:///home/claude/dxf-viewer.html'); await pg.set_input_files('#inFiles',['blk/blocks_test.dxf']); await pg.wait_for_timeout(1500)
    await pg.screenshot(path='t51a.png')
    await pg.set_input_files('#inFiles',['blk/plain.dxf','blk/part_rot.dxf','blk/part_mir.dxf']); await pg.wait_for_timeout(1500)
    for n in ['part_rot','part_mir']:
      r=await pg.evaluate(f"(async()=>{{const a=items.find(x=>x.name==='plain.dxf'),b=items.find(x=>x.name==='{n}.dxf');const r=await geoCompare(await getDoc(a),await getDoc(b),0.1);return [r.same,r.clusters.length]}})()")
      an=await pg.evaluate(f"(async()=>{{const b=items.find(x=>x.name==='{n}.dxf');const r=await geoCompare.analyze(await getDoc(b),{{chk:{{}}}});return [Math.round(r.area),r.pierces]}})()")
      print(n,'compare same,clusters',r,'area,pierces',an)
    print('plain area', await pg.evaluate("(async()=>{const b=items.find(x=>x.name==='plain.dxf');const r=await geoCompare.analyze(await getDoc(b),{chk:{}});return [Math.round(r.area),r.pierces]})()"))
    print('errors',errs); await b.close()
asyncio.run(main())
