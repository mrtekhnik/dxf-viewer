import ezdxf, math
from ezdxf import bbox
# 1) вся деталь — блок, вставлен с поворотом; внутри — вложенный блок отверстия, массив
doc=ezdxf.new('R2010'); msp=doc.modelspace()
hole=doc.blocks.new('HOLE'); hole.add_circle((0,0),5); hole.add_line((-7,0),(7,0),dxfattribs={'layer':'AXIS'})
part=doc.blocks.new('PART',base_point=(10,10))
part.add_lwpolyline([(10,10),(210,10),(210,110,),(10,110)],close=True)
part.add_lwpolyline([(170,10,0),(210,50,0)],dxfattribs={})
part.add_blockref('HOLE',(40,40))
part.add_blockref('HOLE',(60,80),dxfattribs={'xscale':2,'yscale':2})
ins=part.add_blockref('HOLE',(100,40)); ins.dxf.column_count=3; ins.dxf.column_spacing=30; ins.dxf.row_count=2; ins.dxf.row_spacing=30
part.add_arc((150,60),20,0,90)
msp.add_blockref('PART',(0,0),dxfattribs={'rotation':30})
msp.add_blockref('PART',(400,0),dxfattribs={'xscale':-1})   # зеркально
d=msp.add_linear_dim(base=(0,140),p1=(0,0),p2=(200,0),dimstyle='EZDXF'); d.render()
r=msp.add_blockref('PART',(0,300)); r.add_attrib('POS','Поз. 7',(50,350))
doc.saveas('blk/blocks_test.dxf')
# 2) ожидаемые величины: одна деталь без поворота для сравнения площади
doc2=ezdxf.new('R2010'); m2=doc2.modelspace()
m2.add_lwpolyline([(0,0),(200,0),(200,100),(0,100)],close=True)
for (x,y,r) in [(30,30,5),(50,70,10)]+[(90+30*i,30+30*j,5) for i in range(3) for j in range(2)]: m2.add_circle((x,y),r)
doc2.saveas('blk/plain.dxf')
print('ok')
