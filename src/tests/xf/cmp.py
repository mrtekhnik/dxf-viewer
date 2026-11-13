import ezdxf, sys, math
from ezdxf.math import Matrix44, Vec3
from ezdxf import path as P
src,out,a,b,c,d,e,f=sys.argv[1],sys.argv[2],*map(float,sys.argv[3:9])
m=Matrix44([a,b,0,0, c,d,0,0, 0,0,(1 if a*d-b*c>0 else -1),0, e,f,0,1])
A=ezdxf.readfile(src); B=ezdxf.readfile(out)
def pts(ent):
    t=ent.dxftype()
    if t=='HATCH':
        ps=[]
        for p in P.from_hatch(ent): ps+=list(p.flattening(0.01))
        return ps
    if t=='INSERT':
        ps=[]
        for v in ent.virtual_entities():
            ps+=pts(v)
        return ps
    if t in ('TEXT','MTEXT','DIMENSION','POINT','SOLID'):
        return None
    return list(P.make_path(ent).flattening(0.01))
def hd(p,q):
    if not p or not q: return 0 if not p and not q else 1e9
    def sd(x,a,b):
        ab=b-a; L=ab.magnitude_square
        if L<1e-18: return (x-a).magnitude
        t=max(0,min(1,(x-a).dot(ab)/L)); return (x-(a+ab*t)).magnitude
    def one(p,q): return max(min([sd(x,q[i],q[i+1]) for i in range(len(q)-1)]+[(x-q[-1]).magnitude]) for x in p)
    return max(one(p,q),one(q,p))
bad=0;n=0
for ea in A.modelspace():
    eb=B.entitydb.get(ea.dxf.handle); t=ea.dxftype()
    ex=ea.copy(); 
    try: ex.transform(m)
    except Exception as er: print('ezdxf cannot',t,er); continue
    pa=pts(ex); 
    if pa is None:
        if t=='POINT': err=(Vec3(ex.dxf.location)-Vec3(eb.dxf.location)).magnitude
        elif t=='SOLID': err=max((Vec3(ex.dxf.get(k)).replace(z=0)-Vec3(eb.dxf.get(k)).replace(z=0)).magnitude for k in ('vtx0','vtx1','vtx2','vtx3')) if ex.dxf.extrusion.z>0 else 0
        elif t=='DIMENSION': err=max((Vec3(ex.dxf.get(k))-Vec3(eb.dxf.get(k))).magnitude for k in ('defpoint','defpoint2','defpoint3') if ex.dxf.hasattr(k))
        else: 
            print(t, ea.dxf.get('text',''), 'ins', [round(x,2) for x in (eb.dxf.insert)], 'rot', round(eb.dxf.get('rotation',0),2), 'flags', eb.dxf.get('text_generation_flag',None) if t=='TEXT' else eb.dxf.get('attachment_point'), 'al', (eb.dxf.get('halign'),eb.dxf.get('valign'),[round(x,2) for x in eb.dxf.get('align_point',(0,0,0))]) if t=='TEXT' else '', '| ezdxf rigid ins',[round(x,2) for x in ex.dxf.insert],'rot',round(ex.dxf.get('rotation',0),2))
            continue
    else:
        pb=pts(eb); err=hd(pa,pb)
    n+=1
    if err>1e-6: bad+=1; print('BAD',t,ea.dxf.handle,err)
print('checked',n,'bad',bad)
