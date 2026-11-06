import math,os,shutil
def dxf(ents):
    o=['0','SECTION','2','ENTITIES']
    for e in ents:
        if e[0]=='C': o+=['0','CIRCLE','8','0','10',f'{e[1]:.6f}','20',f'{e[2]:.6f}','40',f'{e[3]:.6f}']
        if e[0]=='L': o+=['0','LINE','8','0','10',f'{e[1]:.6f}','20',f'{e[2]:.6f}','11',f'{e[3]:.6f}','21',f'{e[4]:.6f}']
        if e[0]=='P':
            pts=e[2];o+=['0','LWPOLYLINE','8','0','90',str(len(pts)),'70','1' if e[1] else '0']
            for x,y,b in pts: o+=['10',f'{x:.6f}','20',f'{y:.6f}','42',f'{b:.6f}']
    o+=['0','ENDSEC','0','EOF'];return '\n'.join(o)+'\n'
def part(holes,ang=0,mir=False,tx=0,ty=0,rev=False,w=300,h=150):
    t=math.tan(math.pi/8);c,s=math.cos(ang),math.sin(ang);m=-1 if mir else 1
    f=lambda x,y:(c*x*m-s*y+tx,s*x*m+c*y+ty)
    P=[(0,0,0),(w-20,0,t),(w,20,0),(w,h,0),(0,h,0)]
    pp=[(*f(x,y),(-b if mir else b)) for x,y,b in P]
    ents=[('P',True,pp)]+[('C',*f(x,y),r) for x,y,r in holes]+[('L',*f(60,110),*f(200,110))]
    return dxf(ents[::-1] if rev else ents)
H=[(50,60,10),(150,60,10),(250,60,10)]
A='cmp2/Заказ А/DXF';B='cmp2/Заказ Б/DXF';os.makedirs(A,exist_ok=True);os.makedirs(B,exist_ok=True)
for d,args in [(A,{}),(B,{})]: open(d+'/АБВГ.200001.001-Ст3-3-k1.dxf','w').write(part(H))           # одинаковые
open(A+'/АБВГ.200001.002-Ст3-3-k1.dxf','w').write(part(H))
open(B+'/АБВГ.200001.002-Ст3-3-k1.dxf','w').write(part(H,ang=math.radians(90),tx=500,ty=40,rev=True))  # пересохранён в другом положении
open(A+'/АБВГ.200001.003-Ст3-3-k1.dxf','w').write(part(H))
open(B+'/АБВГ.200001.003-Ст3-3-k1.dxf','w').write(part([(50,60,10),(150,63,10),(250,60,12)],ang=math.radians(33),mir=True,tx=-80))  # изменён
open(A+'/АБВГ.200001.004-Ст3-3-k1.dxf','w').write(part(H))
open(B+'/АБВГ.200001.004-Ст3-3-k1.dxf','w').write(part(H).replace('300.000000','300.050000'))  # сдвиг 0.05 — в допуске
print('ok')
