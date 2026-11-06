const fs=require('fs');eval(fs.readFileSync('/home/claude/dxf-viewer/src/geom.part','utf8')+';global.GEO=GEOCORE();');
// деталь: прямоугольник 200x100 со скруглением (полилиния с bulge) и 3 отверстия
function part(holes,slot){const t=Math.tan(Math.PI/8); // 90° дуга
  const P=[0,0,0, 190,0,t, 200,10,0, 200,100,0, 0,100,0];
  const prims=[['P',true,P]];for(const [x,y,r] of holes)prims.push(['C',x,y,r]);
  if(slot)prims.push(['L',50,80,120,80]);
  return {groups:[{prims}]};}
function xform(doc,ang,mir,tx,ty){const c=Math.cos(ang),s=Math.sin(ang),m=mir?-1:1;
  const f=(x,y)=>{x*=m;return [c*x-s*y+tx,s*x+c*y+ty];};
  return {groups:doc.groups.map(G=>({prims:G.prims.map(p=>{
    if(p[0]==='C'){const [x,y]=f(p[1],p[2]);return ['C',x,y,p[3]];}
    if(p[0]==='L'){const a=f(p[1],p[2]),b=f(p[3],p[4]);return ['L',...a,...b];}
    if(p[0]==='P'){const a=p[2].slice();for(let i=0;i<a.length;i+=3){const q=f(a[i],a[i+1]);a[i]=q[0];a[i+1]=q[1];if(mir)a[i+2]=-a[i+2];}return ['P',p[1],a];}
  })}))};}
const A=part([[40,50,8],[100,50,8],[160,50,8]],true);
for(const [ang,mir] of [[0,false],[0.7,false],[Math.PI/2,true],[2.9,true],[1.234,false]]){
  for(const variant of ['same','moved hole']){
    const base=variant==='same'?A:part([[40,50,8],[100,52,8],[160,50,8]],true);
    const B=xform(base,ang,mir,500,-300);
    const t0=Date.now();const r=GEO.compare(A,B,0.1);
    console.log(ang.toFixed(2),mir,variant,'same=',r.same,'clusters',r.clusters.length,'fracA',r.a.frac.toFixed(4),'fracB',r.b.frac.toFixed(4),'badA',r.a.bad.toFixed(2),Date.now()-t0+'ms');
  }}
