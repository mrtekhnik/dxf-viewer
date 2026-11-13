const fs=require('fs'),vm=require('vm');
const code=fs.readFileSync('/home/claude/dxf-viewer/src/xform.part','utf8')+';this.DXFXF=DXFXF;';
const ctx={};vm.createContext(ctx);vm.runInContext(code,ctx);
const [,,inp,outp,a,b,c,d,e,f,mode]=process.argv;
const r=ctx.DXFXF.run(new Uint8Array(fs.readFileSync(inp)),[+a,+b,+c,+d,+e,+f],{text:mode||'auto'});
if(r.err){console.log('ERR',r.err);process.exit(1);}
fs.writeFileSync(outp,Buffer.from(r.bytes));console.log(JSON.stringify({n:r.n,skipped:r.skipped,txtMir:r.txtMir,txtRead:r.txtRead}));
