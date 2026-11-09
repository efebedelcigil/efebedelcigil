from pathlib import Path
import sys,xml.etree.ElementTree as E
ROOT=Path(__file__).resolve().parents[1]
from build_hero import make_svg
ns={'s':'http://www.w3.org/2000/svg'}
r=E.parse(ROOT/'assets/hero-dark.svg').getroot();nodes={e.get('id'):e for e in r.iter() if e.get('id')}
images={}
for key,e in nodes.items():
 if e.get('data-layer'):
  images[int(key[1:])]=(e.find('s:image',ns).get('href').split(',')[1],e.get('data-layer'))
seq=[]
for a in nodes['robotTrack'].findall('s:animate',ns):
 vals=[int(x[2:]) for x in a.get('values').split(';')]
 seq.extend(vals if not seq else vals[:504])
seq=seq[:558]+[seq[54]]
def data(k):return nodes[k].get('href').split(',')[1]
for theme in ('dark','light'):
 for mobile in (False,True):
  for still in (False,True):
   name='hero-'+('mobile-' if mobile else '')+theme+('-still' if still else '')+'.svg'
   (ROOT/'assets'/name).write_text(make_svg(theme,mobile,images,seq,data('background'),data('steady'),data('glance-background'),still),encoding='utf-8')
