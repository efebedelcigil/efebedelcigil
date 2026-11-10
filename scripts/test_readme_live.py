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
   self.assertTrue(any('contribution-' in r for r in refs))
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
  for theme in ['light','dark']:
   for name in ['hero','contribution','portfolio','toolkit','learning','exploring']:
    root=E.parse(ROOT/'assets'/f'{name}-{theme}.svg').getroot()
    self.assertTrue(any(e.tag.endswith('animate') for e in root.iter()),name)
    self.assertIn(f'assets/{name}-{theme}.svg?v=',text)
    self.assertRegex(text,r'prefers-reduced-motion: reduce')
 def test_exact_portfolio_copy(self):
  for theme in ['light','dark']:
   for mobile in ['', 'mobile-']:
    text=(ROOT/'assets'/f'portfolio-{mobile}{theme}.svg').read_text(encoding='utf-8')
    self.assertIn('aria-label="ALL projects, publications, contact info. and more"',text)

if __name__=='__main__':unittest.main()
