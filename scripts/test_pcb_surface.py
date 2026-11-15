import unittest,math,json,xml.etree.ElementTree as E
from pathlib import Path
from contribution_geometry import BoardGeometry
from contribution_routing import configure_sizes
from pcb_surface import surface_regions,surface_art
class SurfaceTests(unittest.TestCase):
 def test_only_active_packages_receive_surface_treatment(self):
  cells={'a':(3,2),'b':(4,2),'c':(5,2)};days={'a':1,'b':0,'c':2};g=BoardGeometry(53);configure_sizes(g,cells,days)
  regions=surface_regions(g,cells,days)
  self.assertEqual([r['date'] for r in regions],['a','c'])
  self.assertTrue(all(math.isfinite(v) for r in regions for v in r['ellipse']))
  self.assertTrue(all(r['ellipse'][2]>0 and r['ellipse'][3]>0 for r in regions))
 def test_empty_and_dense_future_data(self):
  g=BoardGeometry(53);cells={str(i):(i//7,i%7) for i in range(371)}
  for level in [0,1,2,3,4]:
   days={d:level for d in cells};configure_sizes(g,cells,days);regions=surface_regions(g,cells,days)
   self.assertEqual(len(regions),371 if level else 0)
   for theme in ['dark','light']:
    definitions,shadows=surface_art(g,cells,days,theme)
    self.assertIn('pcbTraceQuietMask',definitions)
    self.assertNotIn('<filter',definitions+shadows)
 def test_rendered_surface_follows_public_active_dates(self):
  assets=Path(__file__).resolve().parents[1]/'assets';days=json.loads((assets/'public-profile.json').read_text())['days'];active={d for d,v in days.items() if v}
  for theme in ['dark','light']:
   root=E.parse(assets/f'contribution-{theme}.svg').getroot()
   self.assertEqual({e.get('data-trace-quiet') for e in root.iter() if e.get('data-trace-quiet')},active)
   self.assertEqual({e.get('data-contact-shadow') for e in root.iter() if e.get('data-contact-shadow')},active)
   traces=next(e for e in root.iter() if e.get('data-board-traces'))
   self.assertEqual(traces.get('mask'),'url(#pcbTraceQuietMask)')
if __name__=='__main__':unittest.main()
