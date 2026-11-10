import datetime,json,unittest,xml.etree.ElementTree as E
from pathlib import Path
from public_calendar import parse_calendar,cell_map
from circuit_route import circuit_route
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
  # Worst case: tall package next to low packages, including pins and shadows.
  step=948/53
  boxes=[]
  for col in range(3):
   for row in range(3):
    for level in range(1,5):
     x=20+col*step;y=20+row*30;lift=2+level*2
     points=[(xx-.1*yy,.025*xx+.94*yy) for xx in (x-1,x+14) for yy in (y-lift,y+16)]
     boxes.append((col,row,level,min(p[0] for p in points),min(p[1] for p in points),max(p[0] for p in points),max(p[1] for p in points)))
  for a in boxes:
   for b in boxes:
    if a[:2]==b[:2]:continue
    self.assertTrue(a[5]<=b[3] or b[5]<=a[3] or a[6]<=b[4] or b[6]<=a[4],(a,b))
 def test_rendered_parity(self):
  A=Path(__file__).resolve().parents[1]/'assets';data=json.loads((A/'public-profile.json').read_text());days=data['days'];cells,weeks=cell_map(days)
  palettes={'dark':['#172536']+['#293a4b']*4,'light':['#dfe7ed']+['#405567']*4}
  for theme in ['dark','light']:
   root=E.parse(A/f'contribution-{theme}.svg').getroot();nodes=[e for e in root.iter() if e.get('data-date')]
   self.assertEqual(len([e for e in root.iter() if e.get('data-grid')=='horizontal']),8)
   self.assertEqual(len(nodes),len(days));self.assertEqual({e.get('data-date'):int(e.get('data-level')) for e in nodes},days)
   for e in nodes:
    d=e.get('data-date');self.assertEqual(e.get('fill'),palettes[theme][days[d]])
    dies=[n for n in root.iter() if n.get('data-die')==d]
    self.assertEqual(len(dies),int(days[d]>0))
    if dies:self.assertEqual(float(dies[0].get('width')),4+days[d]*1.5)
    self.assertAlmostEqual(float(e.get('x')),20+cells[d][0]*948/(weeks-1));self.assertEqual(float(e.get('y')),20+cells[d][1]*30-(2+days[d]*2 if days[d] else 0))
  active={cells[d] for d,v in days.items() if v};self.assertTrue(active<=set(circuit_route(active,width=weeks)))
if __name__=='__main__':unittest.main()
