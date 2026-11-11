"""Give all border animations one image resource and one animation clock."""
import re,xml.etree.ElementTree as E
from pathlib import Path

A=Path(__file__).resolve().parents[1]/'assets'
NS='http://www.w3.org/2000/svg'
E.register_namespace('',NS)

def names():
 import json
 base=['toolkit','learning','exploring','focus','portfolio']
 return base+[n+'-mobile' for n in base]+['social-github','social-linkedin','contribution']+['repo-'+r['name'] for r in json.loads((A/'public-profile.json').read_text(encoding='utf-8')).get('pinned',[])]

def build(still=False):
 root=E.Element('{'+NS+'}svg',{'role':'img'})
 offset=0;max_width=0
 for index,name in enumerate(names()):
  prefix=f'm{index}__'
  source=A/f'{name}{"-still" if still else ""}.svg'
  node=E.fromstring(source.read_text(encoding='utf-8'))
  _,_,width,height=map(float,node.get('viewBox').split())
  E.SubElement(root,'{'+NS+'}view',{'id':name,'viewBox':f'0 {offset:g} {width:g} {height:g}'})
  ids={e.get('id'):prefix+e.get('id') for e in node.iter() if e.get('id')}
  for e in node.iter():
   if e.get('id'):e.set('id',ids[e.get('id')])
   if e.get('class'):e.set('class',' '.join(prefix+c for c in e.get('class').split()))
   for key,value in list(e.attrib.items()):
    value=re.sub(r'url\(#([^)]*)\)',lambda m:'url(#'+ids[m[1]]+')',value)
    if key.endswith('href') and value.startswith('#'):value='#'+ids[value[1:]]
    e.set(key,value)
   if e.tag.endswith('style') and e.text:e.text=re.sub(r'\.paint(\d+)',lambda m:'.'+prefix+'paint'+m[1],e.text)
  node.set('x','0');node.set('y',f'{offset:g}');root.append(node)
  offset+=height+20;max_width=max(max_width,width)
 root.set('viewBox',f'0 0 {max_width:g} {offset:g}')
 # No intrinsic width/height: fragment viewBox supplies each module's ratio.
 path=A/f'card-halos{"-still" if still else ""}.svg'
 path.write_text(E.tostring(root,encoding='unicode'),encoding='utf-8')
 print(f'Built {path.name}: {len(names())} synchronized views')

if __name__=='__main__':
 build();build(True)
