import datetime,json,unittest,xml.etree.ElementTree as E
from pathlib import Path
from public_calendar import parse_calendar,cell_map
from circuit_route import circuit_route,spark_gate
from contribution_geometry import BoardGeometry,ChipGeometry
class CalendarTests(unittest.TestCase):
 def test_week_boundaries(self):
  cells,weeks=cell_map({'2026-11-07':0,'2026-11-08':1,'2026-11-09':2})
  self.assertEqual(cells,{'2026-11-07':(0,6),'2026-11-08':(1,0),'2026-11-09':(1,1)});self.assertEqual(weeks,2)
 def test_leap_year_partial_weeks(self):
  start=datetime.date(2024,1,1);days={(start+datetime.timedelta(days=i)).isoformat():i%5 for i in range(366)}
  cells,weeks=cell_map(days);self.assertEqual(len(set(cells.values())),366)
  for d,(x,y) in cells.items():self.assertEqual(y,(datetime.date.fromisoformat(d).weekday()+1)%7)
 def test_incomplete_rejected(self):
  with self.assertRaises(ValueError):parse_calendar('<td data-date="2026-11-10" data-level="1"></td>')
 def test_missing_tooltips_rejected(self):
  start=datetime.date(2025,11,10)
  fragment=''.join(f'<td id="d{i}" data-date="{start+datetime.timedelta(days=i)}" data-level="0"></td>' for i in range(365))
  with self.assertRaisesRegex(ValueError,'Missing daily'):parse_calendar(fragment)
 def test_projected_packages_do_not_overlap(self):
  cases=[(53,ChipGeometry(),(1,.10,-.24,.88)),(53,ChipGeometry(),(1,.025,-.1,.94)),(54,ChipGeometry(),(1,.025,-.1,.94)),(80,ChipGeometry(),(1,.025,-.1,.94)),(54,ChipGeometry(18,19),(.9,.16,-.3,.85)),(26,ChipGeometry(9,11),(.8,-.08,.2,.95))]
  for weeks,chip,projection in cases:
   layout=BoardGeometry(weeks,projection,chip);boxes=[]
   for col in sorted(set([0,1,2,weeks-1])):
    for row in range(7):
     for level in range(1,5):boxes.append((col,row,layout.project_package_bounds(layout.package_origin((col,row),level),level)))
   for a in boxes:
    for b in boxes:
     if a[:2]==b[:2]:continue
     x,y=a[2],b[2]
     self.assertTrue(x[2]<=y[0] or y[2]<=x[0] or x[3]<=y[1] or y[3]<=x[1],(weeks,a[:2],b[:2]))
   self.assertGreaterEqual(min(chip.width,chip.height)*layout.scale,4)
 def test_invalid_perspective_rejected(self):
  with self.assertRaises(ValueError):BoardGeometry(53,(1,1,1,1))
 def test_mounting_hole_clearance(self):
  for weeks in [26,53,54,80]:
   layout=BoardGeometry(weeks)
   for x,y in layout.mounts():self.assertGreaterEqual(min(x,y,layout.width-x,layout.height-y)-3.2,10)
 def test_seeded_copper_clearance(self):
  from pcb_background import tracks,crosses,distance
  layout=BoardGeometry(53);routes,vias=tracks(layout.width,layout.height)
  self.assertEqual((routes,vias),tracks(layout.width,layout.height));self.assertGreater(len(routes),20)
  for i,route in enumerate(routes):
   for x,y in route:self.assertTrue(18<=x<=layout.width-18 and 18<=y<=layout.height-18)
   for other in routes[:i]:
    for a,b in zip(route,route[1:]):
     for c,d in zip(other,other[1:]):
      self.assertFalse(crosses(a,b,c,d));self.assertGreaterEqual(min(distance(a,c,d),distance(b,c,d),distance(c,a,b),distance(d,a,b)),3.5)
 def test_current_layering(self):
  A=Path(__file__).resolve().parents[1]/'assets'
  for theme in ['dark','light']:
   nodes=list(E.parse(A/f'contribution-{theme}.svg').getroot().iter())
   current=[i for i,e in enumerate(nodes) if e.get('pathLength')=='1000']
   pads=[i for i,e in enumerate(nodes) if e.get('data-level')=='0']
   chips=[i for i,e in enumerate(nodes) if e.get('data-date') and e.get('data-level')!='0']
   self.assertTrue(current)
   if pads:self.assertLess(max(pads),min(current))
   if chips:self.assertGreater(min(chips),max(current))
 def test_sparks_follow_current_and_stop_in_still(self):
  A=Path(__file__).resolve().parents[1]/'assets'
  for theme in ['dark','light']:
   root=E.parse(A/f'contribution-{theme}.svg').getroot();nodes=list(root.iter())
   wire=next(e for e in nodes if e.get('pathLength')=='1000')
   sparks=next(e for e in nodes if e.get('data-current-sparks')=='true')
   motion=next(e for e in sparks.iter() if e.tag.endswith('animateMotion'))
   self.assertEqual(motion.get('path'),wire.get('d'));self.assertEqual(motion.get('dur'),'14s')
   self.assertLess(nodes.index(sparks),min(i for i,e in enumerate(nodes) if e.get('data-date') and e.get('data-level')!='0'))
   for filename in [f'contribution-{theme}-still.svg',f'contribution-still-{theme}.svg']:
    self.assertFalse(any('animate' in e.tag for e in E.parse(A/filename).getroot().iter()),filename)
 def test_spark_gate_fades_before_occlusion(self):
  gate=spark_gate([(0,0),(40,0),(0,0)],[(15,-4,25,4)],fade=6)
  self.assertEqual(gate[0][1],1);self.assertEqual(gate[-1][1],1)
  self.assertTrue(any(0<v<1 for t,v in gate))
  for t,v in gate:
   x=80*t if t<=.5 else 80*(1-t)
   if 15<=x<=25:self.assertEqual(v,0)
  self.assertTrue(all(a[0]<b[0] for a,b in zip(gate,gate[1:])))
 def test_projected_spark_keepout(self):
  points=[(0,10),(40,10),(0,10)]
  gate=spark_gate(points,[(9,4,26,15)],projection=(1,.025,-.1,.94))
  for t,v in gate:
   x=80*t if t<=.5 else 80*(1-t);sx,sy=x-1,.025*x+9.4
   if 9<=sx<=26 and 4<=sy<=15:self.assertEqual(v,0)
  self.assertTrue(any(v>0 for t,v in gate))
 def test_rendered_parity(self):
  A=Path(__file__).resolve().parents[1]/'assets';data=json.loads((A/'public-profile.json').read_text());days=data['days'];cells,weeks=cell_map(days);layout=BoardGeometry(weeks)
  from pcb_components import KINDS,contacts
  for theme in ['dark','light']:
   root=E.parse(A/f'contribution-{theme}.svg').getroot();nodes=[e for e in root.iter() if e.get('data-date')]
   self.assertEqual(len([e for e in root.iter() if e.get('data-grid')=='horizontal']),8)
   self.assertEqual(len(nodes),len(days));self.assertEqual({e.get('data-date'):int(e.get('data-level')) for e in nodes},days)
   for e in nodes:
    d=e.get('data-date');level=days[d];self.assertEqual(e.get('data-component'),KINDS[level])
    origin=layout.package_origin(cells[d],level);bounds=layout.chip.bounds(*origin,level);cx,cy=layout.center(cells[d])
    self.assertAlmostEqual(float(e.get('x')),bounds[0]);self.assertAlmostEqual(float(e.get('y')),bounds[1])
    self.assertAlmostEqual((bounds[0]+bounds[2])/2,cx);self.assertAlmostEqual((bounds[1]+bounds[3])/2,cy)
    for px,py in contacts(layout.chip,*origin,level):
     self.assertGreaterEqual(px-1.4,bounds[0]-.001);self.assertLessEqual(px+1.4,bounds[2]+.001)
     self.assertGreaterEqual(py-1.1,bounds[1]-.001);self.assertLessEqual(py+1.1,bounds[3]+.001)
   self.assertEqual(len([e for e in root.iter() if e.get('data-component-sprite')])-4,sum(v>0 for v in days.values()))
  active={cells[d] for d,v in days.items() if v};self.assertTrue(active<=set(circuit_route(active,width=weeks)))
if __name__=='__main__':unittest.main()
