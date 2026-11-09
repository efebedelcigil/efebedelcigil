from pathlib import Path
import json,re,urllib.request,datetime,subprocess
ROOT=Path(__file__).resolve().parents[1]
user='efebedelcigil'
def read(url):
 req=urllib.request.Request(url,headers={'User-Agent':'public-profile-artwork'})
 return urllib.request.urlopen(req,timeout=30).read().decode()
page=read(f'https://github.com/users/{user}/contributions');days={}
for tag in re.findall(r'<td\b[^>]*>',page):
 d=re.search(r'data-date="([^"]+)"',tag);l=re.search(r'data-level="(\d)"',tag)
 if d and l:days[d[1]]=int(l[1])
if len(days)<350:raise ValueError('Incomplete public calendar; preserving previous snapshot')
repos=[]
for page_num in range(1,20):
 batch=json.loads(read(f'https://api.github.com/users/{user}/repos?per_page=100&page={page_num}&type=owner'))
 for r in batch:
  if not r.get('private',True):repos.append({k:r[k] for k in ['name','description','html_url','language','stargazers_count','fork']})
 if len(batch)<100:break
profile_html=read(f'https://github.com/{user}')
pinned=[]
for block in profile_html.split('pinned-item-list-item-content')[1:]:
 m=re.search(r'href="/([^"?]+/[^"?]+)"[^>]*class="Link',block)
 if m:
  owner,name=m[1].split('/',1)
  detail=json.loads(read(f'https://api.github.com/repos/{owner}/{name}'))
  if not detail.get('private',True):pinned.append({k:detail[k] for k in ['name','full_name','description','html_url','language','stargazers_count','fork']})
languages={}
for repo in repos:
 if repo['fork'] or repo['name']==user:continue
 for language,count in json.loads(read(f'https://api.github.com/repos/{user}/{repo["name"]}/languages')).items():languages[language]=languages.get(language,0)+count
previous=json.loads((ROOT/'assets/public-profile.json').read_text(encoding='utf-8'))
activity=previous.get('activity',{})
try:
 query=(ROOT/'scripts/public-profile.graphql').read_text()
 raw=json.loads(subprocess.check_output(['gh','api','graphql','-f','query='+query],text=True))['data']['user']['contributionsCollection']
 activity={label:sum(r['contributions']['totalCount'] for r in raw[key] if not r['repository']['isPrivate']) for label,key in [('Commits','commitContributionsByRepository'),('Issues','issueContributionsByRepository'),('Pull requests','pullRequestContributionsByRepository'),('Reviews','pullRequestReviewContributionsByRepository')]}
except (subprocess.CalledProcessError,KeyError,FileNotFoundError):
 raise RuntimeError('Public activity refresh failed; retaining previous snapshot and artwork')
snapshot={'fetched':datetime.date.today().isoformat(),'source':'Public calendar, public repository metadata and languages; contribution types filtered by public repository.','days':days,'repos':repos,'pinned':pinned,'languages':languages,'activity':activity}
(ROOT/'assets/public-profile.json').write_text(json.dumps(snapshot,indent=2)+'\n',encoding='utf-8')
