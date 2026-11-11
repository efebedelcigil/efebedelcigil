import json,subprocess,tempfile,unittest
from pathlib import Path
from publish_public_assets import publish

class PublishTests(unittest.TestCase):
 def test_generated_publication_and_checkout_isolation(self):
  with tempfile.TemporaryDirectory(prefix='public-assets-test-') as folder:
   base=Path(folder).resolve();self.assertTrue(base.is_relative_to(Path(tempfile.gettempdir()).resolve()))
   root=base/'source';root.mkdir();remote=base/'remote.git'
   def git(*args):return subprocess.check_output(['git',*args],cwd=root,stderr=subprocess.DEVNULL).decode().strip()
   subprocess.run(['git','init','--bare',str(remote)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
   git('init','--initial-branch=main');git('remote','add','origin',str(remote))
   (root/'private.txt').write_text('excluded fixture');git('add','private.txt')
   git('-c','user.name=Test','-c','user.email=test@example.invalid','commit','-m','Source')
   git('push','origin','main')
   head=git('rev-parse','HEAD');(root/'staged.txt').write_text('keep staged');git('add','staged.txt')
   a=root/'assets';a.mkdir();(a/'contribution-dark.svg').write_text('<svg/>')
   (a/'repo-removed-dark.svg').write_text('<svg/>');(a/'hero-dark.svg').write_text('<svg/>');(a/'unrelated.svg').write_text('<svg/>')
   (a/'public-profile.json').write_text(json.dumps({'days':{'2026-11-10':1},'day_counts':{'2026-11-10':2}}))
   (root/'README.md').write_text('Generated profile');(root/'docs').mkdir();(root/'docs/STATIC.md').write_text('Still profile')
   self.assertTrue(publish(root));self.assertFalse(publish(root))
   self.assertEqual(git('rev-parse','HEAD'),head);self.assertEqual(git('branch','--show-current'),'main')
   self.assertEqual(git('diff','--cached','--name-only'),'staged.txt')
   names=git('ls-tree','-r','--name-only','FETCH_HEAD').splitlines()
   self.assertEqual(names,['README.md','assets/contribution-dark.svg','assets/hero-dark.svg','assets/public-profile.json','docs/STATIC.md','private.txt'])
   self.assertEqual(git('show','FETCH_HEAD:private.txt'),'excluded fixture')
   clone=base/'next'
   subprocess.run(['git','clone','--branch','main',str(remote),str(clone)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
   self.assertFalse(publish(clone))
   (clone/'assets/contribution-dark.svg').write_text('<svg><title>updated</title></svg>')
   self.assertTrue(publish(clone))
   git('fetch','origin','main')
   self.assertIn('updated',git('show','FETCH_HEAD:assets/contribution-dark.svg'))

if __name__=='__main__':unittest.main()
