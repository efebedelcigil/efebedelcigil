from pathlib import Path
import json,xml.etree.ElementTree as E
from functools import lru_cache
A=Path(__file__).resolve().parents[1]/'assets'
M=json.loads((A/'icon-map.json').read_text(encoding='utf-8'))
@lru_cache(maxsize=80)
def source(label):return (A/'icons'/(M[label]+'.svg')).read_text(encoding='utf-8')
def logo(label,x,y,c,bg=None,size=18):
 r=E.fromstring(source(label));r.set('x',str(x));r.set('y',str(y));r.set('width',str(size));r.set('height',str(size));r.set('stroke',c);r.set('stroke-width','1.7');r.set('fill','none')
 for e in r.iter():
  for k in ['class','style']:e.attrib.pop(k,None)
  if e.get('stroke')=='currentColor':e.set('stroke',c)
 return E.tostring(r,encoding='unicode')
