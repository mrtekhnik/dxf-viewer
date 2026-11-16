# тестовые папки xf2/A и xf2/B для t69–t72 (две версии деталей, переименованная копия)
import ezdxf, shutil, os
def part(fn,holes):
  os.makedirs(os.path.dirname(fn),exist_ok=True); d=ezdxf.new('R2000');m=d.modelspace()
  m.add_lwpolyline([(0,0),(300,0),(300,150),(0,150)],close=True)
  for x,y,r in holes: m.add_circle((x,y),r)
  d.saveas(fn)
part('xf2/A/DXF/АЮИА.100-01.01-St-3-K1.dxf',[(50,75,10),(150,75,10),(250,75,10)])
part('xf2/B/DXF/АЮИА.100-01.01-St-3-K1.dxf',[(50,75,10),(150,75,12),(250,75,10),(270,30,5)])
part('xf2/A/DXF/АЮИА.100-01.02-St-3-K2.dxf',[(30,30,5)]); part('xf2/B/DXF/АЮИА.100-01.02-St-3-K2.dxf',[(30,30,5)])
part('xf2/A/DXF/АЮИА.100-01.03-St-5-K1.dxf',[(30,30,8)]); shutil.copy('xf2/A/DXF/АЮИА.100-01.03-St-5-K1.dxf','xf2/B/DXF/АЮИА.100-01.04-St-5-K1.dxf')
