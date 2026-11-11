import unittest,math,xml.etree.ElementTree as E
from PIL import Image
from pcb_components import A,META,definitions,contacts
from contribution_geometry import BoardGeometry,ChipGeometry

class PhysicalPartsTests(unittest.TestCase):
 def test_transparent_assets_and_projection(self):
  self.assertEqual(set(META['parts']),{'1','2','3','4'})
  layout=BoardGeometry(53);a,b,c,d=layout.projection
  self.assertEqual([a,c,b,d],META['projection'])
  for level,p in META['parts'].items():
   with Image.open(A/f'part-{level}.png') as image:
    self.assertEqual(image.mode,'RGBA');self.assertEqual(image.getchannel('A').getextrema(),(0,255))
    self.assertLessEqual(max(image.size),384)
    self.assertAlmostEqual(image.width*META['units_per_pixel'],p['image'][2])
    self.assertAlmostEqual(image.height*META['units_per_pixel'],p['image'][3])
   self.assertTrue(all(math.isfinite(v) for point in p['polygon'] for v in point))
 def test_four_shared_embedded_images(self):
  root=E.fromstring(definitions());images=list(root.iter('image'));symbols=list(root.iter('symbol'))
  self.assertEqual(len(images),4);self.assertEqual(len(symbols),4)
  self.assertTrue(all(e.get('href').startswith('data:image/png;base64,') for e in images))
 def test_dense_calendar_all_types_and_contacts(self):
  for weeks in [26,53,54,80]:
   layout=BoardGeometry(weeks);chip=layout.chip
   for level in range(5):
    origin=layout.package_origin((weeks-1,6),level);box=chip.bounds(*origin,level)
    for x,y in contacts(chip,*origin,level):self.assertTrue(box[0]<=x<=box[2] and box[1]<=y<=box[3])
    self.assertGreater(layout.project_package_bounds(origin,level)[2]-layout.project_package_bounds(origin,level)[0],0)

if __name__=='__main__':unittest.main()
