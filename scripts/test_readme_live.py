import re,unittest,hashlib,xml.etree.ElementTree as E
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


class ReadmeLiveTests(unittest.TestCase):
 def test_live_sources_and_static_paths(self):
  for file in [ROOT/'README.md',ROOT/'docs/STATIC.md']:
   text=file.read_text(encoding='utf-8')
   self.assertNotIn('profile-data',text)
   self.assertNotIn('#gh-dark-mode-only',text)
   refs=re.findall(r'(?:src|srcset)="([^"]+)"',text)
   self.assertTrue(any('#contribution' in r for r in refs))
   self.assertEqual(text.count('<picture>'),text.count('<img '))
   self.assertNotRegex(text,r'<a href="[^"]*assets/')
   for ref in refs:
    self.assertIn('?v=',ref)
    path=ref.split('#')[0].split('?')[0]
    self.assertTrue((file.parent/path).is_file(),ref)
    base=Path(path).name
    if file.name=='STATIC.md' and base.startswith(('contribution-','repo-')):self.assertIn('still',path)
    digest=hashlib.sha256((file.parent/path).read_bytes()).hexdigest()[:12]
    self.assertIn('?v='+digest,ref)
 def test_motion_sources(self):
  text=(ROOT/'README.md').read_text(encoding='utf-8')
  for name in ['hero','contribution','portfolio','toolkit','learning','exploring']:
   root=E.parse(ROOT/'assets'/f'{name}.svg').getroot()
   self.assertTrue(any(e.tag.endswith('animate') for e in root.iter()),name)
   self.assertIn(f'assets/{name}.svg?v=' if name=='hero' else '#'+name+'"',text)
   self.assertIn('@media(prefers-color-scheme:dark)',root.find('{http://www.w3.org/2000/svg}style').text)
  self.assertIn('prefers-reduced-motion: reduce',text)
 def test_shared_clock_views_and_references(self):
  from build_halo_atlas import names
  views=[]
  for suffix in ['', '-still']:
   root=E.parse(ROOT/'assets'/f'card-halos{suffix}.svg').getroot()
   self.assertNotIn('width',root.attrib);self.assertNotIn('height',root.attrib)
   found=[(e.get('id'),e.get('viewBox')) for e in root if e.tag.endswith('view')];views.append(found)
   self.assertEqual([n for n,v in found],names())
   ids=[e.get('id') for e in root.iter() if e.get('id')];self.assertEqual(len(ids),len(set(ids)))
   for e in root.iter():
    for value in e.attrib.values():
     for ref in re.findall(r'url\(#([^)]*)\)',value):self.assertIn(ref,ids)
   if suffix:self.assertFalse(any('animate' in e.tag for e in root.iter()))
   else:
    for e in root.iter():
     if e.get('data-halo')=='true':
      animation=next(iter(e));self.assertEqual(animation.get('dur'),'8s');self.assertEqual(animation.get('begin'),'0s')
  self.assertEqual(views[0],views[1])
 def test_adaptive_geometry_and_timing_unchanged(self):
  for name in ['hero','hero-mobile','contribution','portfolio','toolkit','learning','exploring']:
   left=E.parse(ROOT/'assets'/f'{name}-light.svg').getroot()
   adaptive=E.parse(ROOT/'assets'/f'{name}.svg').getroot()
   source=list(left.iter());result=[e for e in adaptive.iter() if not e.tag.endswith('style')]
   self.assertEqual(len(source),len(result))
   for a,b in zip(source,result):
    self.assertEqual(a.tag,b.tag)
    attrs={k:v for k,v in b.attrib.items() if k!='class'}
    expected={k:v for k,v in a.attrib.items() if k!='class'}
    self.assertEqual(hashlib.sha256(repr(expected).encode()).hexdigest(),hashlib.sha256(repr(attrs).encode()).hexdigest(),(name,a.tag))
 def test_exact_portfolio_copy(self):
  for theme in ['light','dark']:
   for mobile in ['', 'mobile-']:
    text=(ROOT/'assets'/f'portfolio-{mobile}{theme}.svg').read_text(encoding='utf-8')
    self.assertIn('aria-label="ALL projects, publications, contact info. and more"',text)

if __name__=='__main__':unittest.main()
