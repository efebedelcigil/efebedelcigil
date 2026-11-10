from labels import display_label
from pathlib import Path
import json,html,hashlib,re
R=Path(__file__).resolve().parents[1]
A=R/'assets';profile=json.loads((A/'profile.json').read_text(encoding='utf-8'));data=json.loads((A/'public-profile.json').read_text(encoding='utf-8'))
def picture(name,alt,width=1120,mobile=True,hero=False,target=None):
 prefix='hero-' if hero else name+'-'
 sources=[]
 for theme in ['dark','light']:
  desktop=prefix+theme;small='hero-mobile-'+theme if hero else name+'-mobile-'+theme
  scheme=f'(prefers-color-scheme: {theme})'
  has_still=hero or name in ('toolkit','learning','exploring','focus','portfolio') or name.startswith('repo-')
  if has_still:
   if mobile:sources.append(f'<source media="{scheme} and (prefers-reduced-motion: reduce) and (max-width: 600px)" srcset="assets/{small}-still.svg">')
   sources.append(f'<source media="{scheme} and (prefers-reduced-motion: reduce)" srcset="assets/{desktop}-still.svg">')
  if name=='contribution':sources.append(f'<source media="{scheme} and (prefers-reduced-motion: reduce)" srcset="assets/contribution-still-{theme}.svg">')
  if mobile:sources.append(f'<source media="{scheme} and (max-width: 600px)" srcset="assets/{small}.svg">')
  sources.append(f'<source media="{scheme}" srcset="assets/{desktop}.svg">')
 content='<picture>'+''.join(sources)+f'<img src="assets/{prefix}light.svg" width="{width}" alt="{html.escape(display_label(alt),quote=True)}"></picture>'
 if name=='back-top':target='#top'
 return f'<a href="{target}">{content}</a>' if target else content

def linked(name,url,alt,width=138,mobile=False):return picture(name,alt,width,mobile,target=url)
def block(content):return '<p align="center">'+content+'</p>'
def heading(key,title):return block(picture('heading-'+key,title,1120,False))
parts=['<a name="top"></a>',block(picture('hero','Efe Varol Bedelcigil: control systems and robotics.',1280,True,True)),'<p align="left">'+linked('social-github','https://github.com/efebedelcigil','GitHub')+' '+linked('social-linkedin','https://www.linkedin.com/in/efevarolbedelcigil/','LinkedIn')+'</p>',block(linked('portfolio',profile['portfolio'],'Explore my portfolio: ALL projects, publications, contact info. and more',1120,True)),heading('working','Working areas'),block(picture('focus','Working areas: '+', '.join(profile['areas']))),heading('tools','Tools'),block(picture('toolkit','Engineering tools: '+', '.join(t for g in json.loads((A/'toolkit.json').read_text(encoding='utf-8')) for t in g['tools']))),heading('learning','In progress'),block(picture('learning','In progress. Areas: '+', '.join(profile['learning_areas'])+'. Tools and methods: '+', '.join(t for g in json.loads((A/'learning.json').read_text(encoding='utf-8')) for t in g['tools']))),heading('exploring','Interested in exploring'),block(picture('exploring','Interested in exploring. Areas: '+', '.join(profile['exploring_areas'])+'. Tools and methods: '+', '.join(t for g in json.loads((A/'exploring.json').read_text(encoding='utf-8')) for t in g['tools']))),heading('contribution','Contribution circuit'),block(picture('contribution','Public contribution circuit. Live data refreshed periodically.',mobile=False)),block(picture('activity','Public activity: '+', '.join(str(v)+' '+k for k,v in data['activity'].items()),mobile=False)),heading('languages','Project languages'),block(picture('profile-cards','Public project language distribution by source code bytes.',mobile=False)),heading('pinned','Pinned repositories')]
repos=data.get('pinned',[])
cards=[linked('repo-'+r['name'],r['html_url'],r['name']+' / '+(r['description'] or ''),'49%') for r in repos]
parts.append('<p align="center">'+' '.join(cards)+'</p>' if cards else 'No public repositories pinned yet.')
parts.append('<hr>\n\n<p align="center">'+linked('still-link','docs/STATIC.md','Still version of landing page',200)+' &nbsp; '+picture('back-top','Back to top',95,False)+'</p>')
for i in range(len(parts)-1):
 if 'assets/heading-' in parts[i] and parts[i+1].startswith('<p align="center">'):
  parts[i]=parts[i].removesuffix('</p>')+'<br>'+parts[i+1].removeprefix('<p align="center">');parts[i+1]=''
content='\n\n'.join(p for p in parts if p)+'\n'
def version(match):
 path=match.group(0);digest=hashlib.sha256((R/path).read_bytes()).hexdigest()[:12];return path+'?v='+digest
content=re.sub(r'assets/[^\"#?<>]+\.svg',version,content)
(R/'README.md').write_text(content,encoding='utf-8')
