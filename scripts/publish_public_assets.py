"""Publish generated profile files atomically without changing source files."""
import json,os,subprocess,tempfile
from pathlib import Path

BRANCH='main'
ROOT=Path(__file__).resolve().parents[1]

def publish(root=ROOT):
 root=Path(root);assets=root/'assets'
 prefixes=('hero-','toolkit-','learning-','exploring-','focus-','portfolio-','heading-','social-','still-link-','back-top-','contribution-','activity-','profile-cards-','repo-')
 files=sorted(p for p in assets.glob('*.svg') if p.name.startswith(prefixes))
 files += [assets/'public-profile.json',root/'README.md',root/'docs/STATIC.md']
 if not (assets/'public-profile.json').is_file() or not any(p.name=='contribution-dark.svg' for p in files):
  raise ValueError('Missing public snapshot or contribution artwork')
 snapshot=json.loads((assets/'public-profile.json').read_text(encoding='utf-8'))
 current_pins={r['name'] for r in snapshot.get('pinned',[])}
 files=[p for p in files if not p.name.startswith('repo-') or any(p.name in {f'repo-{name}-{theme}{suffix}.svg' for theme in ['dark','light'] for suffix in ['', '-still']} for name in current_pins)]
 if not snapshot.get('days') or set(snapshot['days'])!=set(snapshot.get('day_counts',{})):
  raise ValueError('Incomplete public calendar')
 fd,index=tempfile.mkstemp(prefix='profile-data-index-');os.close(fd);Path(index).unlink()
 env={**os.environ,'GIT_INDEX_FILE':index,'GIT_AUTHOR_NAME':'github-actions[bot]','GIT_AUTHOR_EMAIL':'41898282+github-actions[bot]@users.noreply.github.com','GIT_COMMITTER_NAME':'github-actions[bot]','GIT_COMMITTER_EMAIL':'41898282+github-actions[bot]@users.noreply.github.com'}
 def git(*args,input=None,check=True):
  return subprocess.run(['git',*args],cwd=root,env=env,input=input,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=check)
 try:
  ref='refs/heads/'+BRANCH
  remote=git('ls-remote','--exit-code','--heads','origin',ref,check=False)
  if remote.returncode or not remote.stdout.strip():raise RuntimeError('Cannot resolve publication branch: '+remote.stderr.decode())
  git('fetch','--no-tags','--depth=1','origin',ref)
  parent=git('rev-parse','FETCH_HEAD').stdout.decode().strip()
  if parent!=git('rev-parse','HEAD').stdout.decode().strip():
   print('Main advanced during generation; skipping stale output');return False
  git('read-tree',parent);entries=[]
  previous=git('ls-tree','-r','--name-only',parent,'assets/').stdout.decode().splitlines()
  current={str(p.relative_to(root)).replace('\\','/') for p in files}
  for name in previous:
   if name.startswith('assets/repo-') and name.endswith('.svg') and name not in current:
    git('update-index','--force-remove',name)
  for p in files:
   oid=git('hash-object','-w','--stdin',input=p.read_bytes()).stdout.decode().strip()
   entries.append(f'100644 {oid}\t{p.relative_to(root).as_posix()}\n')
  git('update-index','--index-info',input=''.join(entries).encode())
  tree=git('write-tree').stdout.decode().strip()
  if tree==git('rev-parse',parent+'^{tree}').stdout.decode().strip():
   print('Public assets unchanged');return False
  args=['commit-tree',tree,'-p',parent]
  commit=git(*args,input=b'Refresh public profile data assets\n').stdout.decode().strip()
  git('push','origin',commit+':'+ref)
  print('Published public assets to '+BRANCH);return True
 finally:
  Path(index).unlink(missing_ok=True);Path(index+'.lock').unlink(missing_ok=True)

if __name__=='__main__':publish()
