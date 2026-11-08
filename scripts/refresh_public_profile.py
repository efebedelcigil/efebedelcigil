from pathlib import Path
import json,re,urllib.request,datetime
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
snapshot={'fetched':datetime.date.today().isoformat(),'source':'Anonymous public GitHub endpoints. No credentials, private repositories or private contribution aggregates.','days':days,'repos':repos}
(ROOT/'assets/public-profile.json').write_text(json.dumps(snapshot,indent=2)+'\n',encoding='utf-8')
