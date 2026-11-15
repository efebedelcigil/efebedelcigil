from pathlib import Path
import runpy,json,math,itertools,xml.etree.ElementTree as E
ROOT=Path(__file__).resolve().parents[1]
import json
from contribution_geometry import BoardGeometry
from contribution_routing import physical_route,configure_sizes
from pcb_components import META
from public_calendar import cell_map
original=json.loads((ROOT/'assets/public-profile.json').read_text())['days'];cells,weeks=cell_map(original);g=BoardGeometry(weeks);route=physical_route;levels=META;checked=0;N={'configure_sizes':configure_sizes}
from circuit_route import circuit_route
from contribution_geometry import BoardGeometry
from pcb_components import contacts
mid=(26,3);day=next(d for d,c in cells.items() if c==mid);zero={d:0 for d in original}
for level in range(1,5):
 data=zero.copy();data[day]=level;_,info=route(g,cells,data,circuit_route({mid},width=g.weeks)[:-1]);part=info['parts'][mid];l,t,r,b=part['keep'];ox,oy=part['origin'];directions=[(ox,t-4),(r+4,oy),(ox,b+4),(l-4,oy)]
 for incoming,outgoing in itertools.product(directions,repeat=2):
  entry=min(part['pins'],key=lambda p:math.dist(p,incoming));exit=min((p for p in part['pins'] if p!=entry),key=lambda p:math.dist(p,outgoing));a=info['port'](part,entry);z=info['port'](part,exit)
  approach=info['astar'](incoming,a)+[entry];departure=[exit]+info['astar'](z,outgoing)
  assert approach[-1]==entry and departure[0]==exit and entry!=exit
  assert (a[1]==entry[1] and z[1]==exit[1]) or (a[0]==entry[0] and z[0]==exit[0])
  checked+=1
pairs=0
for one,two,direction in itertools.product(range(1,5),range(1,5),[(1,0),(-1,0),(0,1),(0,-1)]):
 other=(mid[0]+direction[0],mid[1]+direction[1]);otherday=next(d for d,c in cells.items() if c==other);data=zero.copy();data[day]=one;data[otherday]=two
 points,info=route(g,cells,data,circuit_route({mid,other},width=g.weeks)[:-1]);assert all(c['entry_error']==0 and c['exit_error']==0 for c in info['terminal_checks']);pairs+=1
# Every type in every neighboring position: use actual projected render polygons.
for dx,dy in itertools.product([-1,0,1],repeat=2):
 if not(dx or dy):continue
 for a,b in itertools.product(range(1,5),repeat=2):
  pairdata=zero.copy()
  for date,cell in cells.items():
   if cell==(25,3):pairdata[date]=a
   elif cell==(25+dx,3+dy):pairdata[date]=b
  N['configure_sizes'](g,cells,pairdata)
  x=g.project_package_bounds(g.package_origin((25,3),a),a);y=g.project_package_bounds(g.package_origin((25+dx,3+dy),b),b)
  assert x[2]<=y[0] or y[2]<=x[0] or x[3]<=y[1] or y[3]<=x[1]
# Dense calendars and empty fallback preserve all terminals and finite geometry.
for value in range(5):
 data={d:value for d in original};active={cells[d] for d in data if value};points,info=route(g,cells,data,circuit_route(active,width=g.weeks)[:-1]);assert points and all(math.isfinite(v) for p in points for v in p)
 if value:assert len(info['terminal_checks'])==len(original)
import random
for seed in range(4):
 rng=random.Random(seed);data={d:rng.randrange(5) for d in original};active={cells[d] for d,v in data.items() if v};points,info=route(g,cells,data,circuit_route(active,width=g.weeks)[:-1]);assert len(info['terminal_checks'])==len(active)
for theme in ['dark','light']:
 root=E.parse(ROOT/'assets'/f'contribution-{theme}.svg').getroot();mapping={n.get('data-date'):int(n.get('data-level')) for n in root.iter() if n.get('data-date')};assert mapping==original
 assert any(n.get('data-legend-empty') for n in root.iter());assert any(n.get('data-edge-via') for n in root.iter());assert any(n.get('data-current-layer') for n in root.iter());assert any(n.get('data-halo') for n in root.iter())
print('Terminal directions, 64 adjacent pairs, 128 projected pairs, empty/dense and 4 mixed calendars passed')
