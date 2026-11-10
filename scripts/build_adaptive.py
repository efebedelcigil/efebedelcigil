"""Combine matching theme artwork without duplicating geometry or animation."""
import re,xml.etree.ElementTree as E
from pathlib import Path

A=Path(__file__).resolve().parents[1]/'assets'
NS='http://www.w3.org/2000/svg'
E.register_namespace('',NS)
PREFIXES=('hero-','toolkit-','learning-','exploring-','focus-','portfolio-','heading-','social-','still-link-','back-top-','contribution-','activity-','profile-cards-','repo-')

def combine(light,dark):
 a=E.fromstring(light);b=E.fromstring(dark);left=list(a.iter());right=list(b.iter());paints={}
 if len(left)!=len(right):raise ValueError('Theme element counts differ')
 for x,y in zip(left,right):
  if x.tag!=y.tag or x.text!=y.text or set(x.attrib)!=set(y.attrib):raise ValueError('Theme structure differs')
  for key,value in list(x.attrib.items()):
   other=y.get(key)
   if value==other:continue
   if key not in ['fill','stroke','stop-color','flood-color']:
    raise ValueError(f'Non-colour theme difference: {key}')
   pair=(key,value,other)
   if pair not in paints:paints[pair]=f'paint{len(paints)}'
   x.set('class',(x.get('class','')+' '+paints[pair]).strip())
 style=E.Element('{'+NS+'}style')
 style.text='@media(prefers-color-scheme:dark){'+''.join(f'.{name}{{{key}:{dark};}}' for (key,light,dark),name in paints.items())+'}'
 a.insert(0,style)
 return E.tostring(a,encoding='unicode')

if __name__=='__main__':
 count=0
 for path in sorted(A.glob('*-light*.svg')):
  if not path.name.startswith(PREFIXES):continue
  match=re.fullmatch(r'(.+)-light(-still)?\.svg',path.name)
  if not match or match[1].endswith('-still'):continue
  stem,suffix=match[1],match[2] or '';dark=A/f'{stem}-dark{suffix}.svg'
  if not dark.is_file():continue
  try:result=combine(path.read_text(encoding='utf-8'),dark.read_text(encoding='utf-8'))
  except ValueError as error:raise ValueError(f'{path.name}: {error}') from error
  (A/f'{stem}{suffix}.svg').write_text(result,encoding='utf-8');count+=1
 print(f'Built {count} adaptive SVGs')
