# DXFXF: геометрия после поворота/зеркала совпадает с ezdxf (8 матриц)
import subprocess
Ms=["0 1 -1 0 0 0","-1 0 0 -1 0 0","0 -1 1 0 0 0","-1 0 0 1 0 0","1 0 0 -1 0 0","0 1 1 0 0 0","0.8660254037844387 0.5 -0.5 0.8660254037844387 10 -5","-0.8660254037844387 0.5 0.5 0.8660254037844387 3 4"]
errs=[]
for M in Ms:
  r=subprocess.run(['node','run.js','test.dxf','o.dxf',*M.split()],cwd='xf',capture_output=True,text=True)
  if r.returncode:errs.append(M+' run');continue
  c=subprocess.run(['python3','cmp.py','test.dxf','o.dxf',*M.split()],cwd='xf',capture_output=True,text=True).stdout
  for l in c.splitlines():
    if l.startswith('BAD') and float(l.split()[-1])>0.03: errs.append(M+' '+l)
  l=subprocess.run(['python3','lines.py','test.dxf','o.dxf'],cwd='xf',capture_output=True,text=True).stdout
  if 'BAD 0 []' not in l: errs.append(M+' bytes '+l)
print('errors',errs)
