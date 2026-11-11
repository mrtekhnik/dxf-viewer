const fs=require('fs');let c=fs.readFileSync('/home/claude/dxf-viewer/src/core.part','utf8');c=c.slice(c.indexOf("<script>\n'use strict';")+9);
eval(c+';global.DXFCORE=DXFCORE;');eval(fs.readFileSync('/home/claude/dxf-viewer/src/geom.part','utf8').split('const GEO=GEOCORE()')[0]+';global.GEO=GEOCORE();');
const Core=DXFCORE();const ld=f=>{const b=fs.readFileSync(f);return Core.parseDXF(b.buffer.slice(b.byteOffset,b.byteOffset+b.length),f);};
const [fa,fb]=process.argv.slice(2);const r=GEO.compare(ld(fa),ld(fb),0.1);console.log(r.same, r.desc.map((d,i)=>(i+1)+') '+d.text).join('\n'));
