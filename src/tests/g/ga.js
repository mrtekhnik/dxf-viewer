const fs=require('fs');let c=fs.readFileSync('/home/claude/dxf-viewer/src/core.part','utf8');c=c.slice(c.indexOf("<script>\n'use strict';")+9);
eval(c+';global.DXFCORE=DXFCORE;');eval(fs.readFileSync('/home/claude/dxf-viewer/src/geom.part','utf8').split('const GEO=GEOCORE()')[0]+';global.GEO=GEOCORE();');
const Core=DXFCORE();const ld=f=>{const b=fs.readFileSync(f);return Core.parseDXF(b.buffer.slice(b.byteOffset,b.byteOffset+b.length),f);};
const R={s:+process.argv[2]||3,join:0.01,minLen:0.1,gapMax:2,holeK:1,holeAbs:1,webK:1,webAbs:1,chk:{open:1,gap:1,dup:1,small:1,hole:1,web:1,text:1,out:1}};
for(const f of process.argv.slice(3)){const t=Date.now();const r=GEO.analyze(ld(f),R);
 console.log(f.split('/').pop(),'area',r.area.toFixed(1),'cut',r.cut.toFixed(1),'pierce',r.pierces,'holes',r.holes,'open',r.open,'size',r.size&&r.size.map(v=>v.toFixed(1)).join('x'),Date.now()-t+'ms');
 for(const i of r.issues.slice(0,8))console.log('   -',i.k,i.text);}
