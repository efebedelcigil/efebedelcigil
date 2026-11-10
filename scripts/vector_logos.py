from pathlib import Path
import json,xml.etree.ElementTree as E
from functools import lru_cache
from labels import match_key,lookup_index
A=Path(__file__).resolve().parents[1]/'assets'
M=lookup_index(json.loads((A/'icon-map.json').read_text(encoding='utf-8')))
@lru_cache(maxsize=80)
def source(label):return (A/'icons'/(M[match_key(label)]+'.svg')).read_text(encoding='utf-8')
BRANDS=lookup_index(json.loads((A/'brand-map.json').read_text(encoding='utf-8')))
def logo(label,x,y,c,bg=None,size=18):
 if match_key(label) in BRANDS:
  r=E.parse(A/'logos'/(BRANDS[match_key(label)]+'.svg')).getroot()
  for e in r.iter():
   for k in ['style','class']:e.attrib.pop(k,None)
   if e.get('fill')!='none':e.set('fill',bg if bg and e.get('fill','').lower() in ('#fff','#ffffff','white') else c)
   if e.get('stroke') and e.get('stroke')!='none':e.set('stroke',c)
   if e.tag.endswith('style'):e.text=''
 else:
  r=E.fromstring(source(label));r.set('stroke',c);r.set('stroke-width','1.7');r.set('fill','none')
  for e in r.iter():
   for k in ['class','style']:e.attrib.pop(k,None)
   if e.get('stroke')=='currentColor':e.set('stroke',c)
 r.set('x',str(x));r.set('y',str(y));r.set('width',str(size));r.set('height',str(size))
 return E.tostring(r,encoding='unicode')
