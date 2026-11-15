from pathlib import Path
import json,os
from PIL import Image
A=Path(__file__).resolve().parents[1]/'assets/components3d'
m=json.loads((A/'layout.json').read_text(encoding='utf-8'));ia,ib,ic,id=m['inverse']
def hull(points):
 points=sorted(set(points))
 def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 def chain(seq):
  result=[]
  for p in seq:
   while len(result)>1 and cross(result[-2],result[-1],p)<=0:result.pop()
   result.append(p)
  return result
 return chain(points)[:-1]+chain(reversed(points))[:-1]
for key,p in m['parts'].items():
 if os.environ.get('PCB_PART_VARIANTS') and key not in os.environ['PCB_PART_VARIANTS'].split(','):continue
 im=Image.open(A/f'part-{key}.png');alpha=im.getchannel('A');ix,iy,w,h=p['image'];points=[]
 for y in range(im.height):
  row=[x for x in range(im.width) if alpha.getpixel((x,y))>64]
  if row:
   for x in [row[0],row[-1]+1]:
    for yy in [y,y+1]:
     sx=ix+x*w/im.width;sy=iy+yy*h/im.height;points.append((ia*sx+ic*sy,ib*sx+id*sy))
 polygon=hull(points)
 p['polygon']=polygon;p['bounds']=[min(x for x,y in polygon),min(y for x,y in polygon),max(x for x,y in polygon),max(y for x,y in polygon)]
 p['envelope']='opaque-alpha-convex-hull'
(A/'layout.json').write_text(json.dumps(m,indent=2),encoding='utf-8')
