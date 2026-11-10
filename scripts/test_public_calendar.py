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
 def test_rendered_parity(self):
  A=Path(__file__).resolve().parents[1]/'assets';data=json.loads((A/'public-profile.json').read_text());days=data['days'];cells,weeks=cell_map(days)
  palettes={'dark':['#161b22','#0e4429','#006d32','#26a641','#39d353'],'light':['#ebedf0','#9be9a8','#40c463','#30a14e','#216e39']}
  for theme in ['dark','light']:
   root=E.parse(A/f'contribution-{theme}.svg').getroot();nodes=[e for e in root.iter() if e.get('data-date')]
   self.assertEqual(len(nodes),len(days));self.assertEqual({e.get('data-date'):int(e.get('data-level')) for e in nodes},days)
   for e in nodes:
    d=e.get('data-date');self.assertEqual(e.get('fill'),palettes[theme][days[d]])
    self.assertAlmostEqual(float(e.get('x')),20+cells[d][0]*948/(weeks-1));self.assertEqual(float(e.get('y')),20+cells[d][1]*21-(3+days[d]*.65 if days[d] else 0))
  active={cells[d] for d,v in days.items() if v};self.assertTrue(active<=set(circuit_route(active,width=weeks)))
if __name__=='__main__':unittest.main()
