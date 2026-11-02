const fs=require('fs');const src=fs.readFileSync('/home/claude/dxf-viewer.src.html','utf8');
const a=src.indexOf('function DXFCORE(){');const b=src.indexOf('/* =====================================================================\n   ОСНОВНОЙ ПОТОК');
eval(src.slice(a,b));const Core=DXFCORE();
const buf=fs.readFileSync(process.argv[2]);const doc=Core.parseDXF(buf.buffer.slice(buf.byteOffset,buf.byteOffset+buf.length),'x');
console.log(doc.log.map(l=>l.join(': ')).join('\n'));console.log('size',doc.size,'origin',doc.origin);
for(const G of doc.groups){if(G.texts)console.log('texts',JSON.stringify(G.texts));}
const ml=doc.groups.flatMap(G=>G.prims.filter(p=>p[0]==='P'&&p[2].length<=12).map(p=>JSON.stringify(p.slice(0,2).concat([p[2].map(v=>+v.toFixed(1))]))));console.log(ml.slice(0,10).join('\n'));
