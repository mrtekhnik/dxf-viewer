import ezdxf, math, random
D='dxf/'
# 1: R2000 sheet metal part with bulges, circles, arcs, colors, lineweights, spline, text, insert
d=ezdxf.new('R2000'); m=d.modelspace()
d.layers.add('Контур', color=7, lineweight=50)
d.layers.add('Гибы', color=1)
d.layers.add('Скрытый', color=3).off()
m.add_lwpolyline([(0,0,0),(200,0,0.4142),(220,20,0),(220,120,0),(0,120,0)], format='xyb', close=True, dxfattribs={'layer':'Контур'})
for x in (30,90,150): m.add_circle((x,60),8,dxfattribs={'layer':'Контур'})
m.add_arc((110,60),25,200,340,dxfattribs={'color':4})
m.add_line((0,40),(220,40),dxfattribs={'layer':'Гибы','linetype':'CONTINUOUS'})
m.add_line((-500,-500),(-400,-400),dxfattribs={'layer':'Скрытый'})
m.add_spline([(0,130),(50,160),(100,130),(150,160)])
m.add_text('Деталь 1',dxfattribs={'height':5}).set_placement((10,-10))
b=d.blocks.new('B1'); b.add_circle((0,0),3); m.add_blockref('B1',(200,100))
d.saveas(D+'деталь_01.dxf')
# 2: R12 with POLYLINE, cp1251, large coords
d=ezdxf.new('R12'); m=d.modelspace()
d.layers.add('Слой_кириллица',color=2)
m.add_polyline2d([(1e6,2e6),(1e6+100,2e6),(1e6+100,2e6+50),(1e6,2e6+50)],close=True,dxfattribs={'layer':'Слой_кириллица'})
p=m.add_polyline2d([(1e6+20,2e6+10,0,0,1),(1e6+40,2e6+10,0,0,1)],format='xyseb',close=True)
m.add_circle((1e6+70,2e6+25),5,dxfattribs={'color':5})
d.encoding='cp1251'
d.saveas(D+'деталь_02_R12.dxf',encoding='cp1251')
# 3: arcs with extrusion -Z (as SolidWorks does)
d=ezdxf.new('R2010'); m=d.modelspace()
m.add_line((0,0),(100,0)); m.add_line((0,0),(0,50))
m.add_arc((20,10),10,0,90,dxfattribs={'extrusion':(0,0,-1),'color':1})  # OCS center (20,10) -> WCS (-20,10)
m.add_circle((50,25),5,dxfattribs={'extrusion':(0,0,-1),'color':3})     # -> (-50,25)
m.add_lwpolyline([(10,40,0),(30,40,1),(30,45,0)],format='xyb',dxfattribs={'extrusion':(0,0,-1),'color':6})
m.add_ellipse((70,30),(10,0),0.5)
d.saveas(D+'деталь_03_extrusion.dxf')
# 4: broken file
open(D+'битый.dxf','w').write('0\nSECTION\n2\nENTITIES\n0\nLINE\n8\n0\n10\nabc\n20\n0\n11\n10\nGARBAGE\n0\nCIRCLE\n10\n5\n20\n5\n40\n2\n0\nENDSEC\n0\nEOF\n')
# 5: empty / non dxf
open(D+'пустой.dxf','w').write('hello world')
# 6: big file
d=ezdxf.new('R2000'); m=d.modelspace(); random.seed(1)
for i in range(60000):
  x,y=random.random()*1000,random.random()*600; m.add_line((x,y),(x+random.random()*20,y+random.random()*20),dxfattribs={'color':random.randint(1,255)})
d.saveas(D+'большой_60k.dxf')
for i in range(40):
  d=ezdxf.new('R2000'); m=d.modelspace(); w=50+i*5
  m.add_lwpolyline([(0,0),(w,0),(w,40),(0,40)],close=True); m.add_circle((w/2,20),5+i%7)
  d.saveas(D+f'деталь_{i+10:03d}.dxf')
