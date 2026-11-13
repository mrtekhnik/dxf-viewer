const fs=require('fs');let c=fs.readFileSync('/home/claude/dxf-viewer/src/core.part','utf8');c=c.slice(c.indexOf("<script>\n'use strict';")+9);
eval(c+';global.DXFCORE=DXFCORE;');eval(fs.readFileSync('/home/claude/dxf-viewer/src/geom.part','utf8').split('const GEO=GEOCORE()')[0]+';global.GEO=GEOCORE();');
const Core=DXFCORE();const ld=f=>{const b=fs.readFileSync(f);return Core.parseDXF(b.buffer.slice(b.byteOffset,b.byteOffset+b.length),f);};
for(const f of process.argv.slice(2)){const d=ld(f);const t={};let dims=0;for(const G of d.groups){for(const p of G.prims)t[p[0]]=(t[p[0]]||0)+1;if(G.dim)dims+=G.prims.length;}
 console.log(f.split('/').pop(),t,'dimprims',dims,'size',d.size.map(v=>v.toFixed(1)));d.log.forEach(l=>console.log('  ',l.join(' ')));}
