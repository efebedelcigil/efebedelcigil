from pathlib import Path
import json,html
R=Path(__file__).resolve().parents[1]
A=R/'assets';profile=json.loads((A/'profile.json').read_text(encoding='utf-8'));data=json.loads((A/'public-profile.json').read_text(encoding='utf-8'))
def picture(name,alt,width=1120,mobile=True,hero=False,target=None):
 result=[]
 for theme in ['dark','light']:
  fragment=f'#gh-{theme}-mode-only';prefix='hero-' if hero else name+'-';desktop=prefix+theme
  if hero:mobile_name='hero-mobile-'+theme
  else:mobile_name=name+'-mobile-'+theme
  sources=''
  if name in ('toolkit','learning','exploring','focus','portfolio'):
   if mobile:sources+=f'<source media="(prefers-reduced-motion: reduce) and (max-width: 600px)" srcset="assets/{mobile_name}-still.svg">'
   sources+=f'<source media="(prefers-reduced-motion: reduce)" srcset="assets/{desktop}-still.svg">'
  if name=='contribution':sources+=f'<source media="(prefers-reduced-motion: reduce)" srcset="assets/contribution-still-{theme}.svg">'
  if hero:
   if mobile:sources+=f'<source media="(prefers-reduced-motion: reduce) and (max-width: 600px)" srcset="assets/{mobile_name}-still.svg">'
   sources+=f'<source media="(prefers-reduced-motion: reduce)" srcset="assets/{desktop}-still.svg">'
  if mobile:sources+=f'<source media="(max-width: 600px)" srcset="assets/{mobile_name}.svg">'
  destination=fragment if name=='back-top' else (target or ('assets/'+desktop+'.svg'))+fragment
  result.append(f'<a href="{destination}"><picture>{sources}<img src="assets/{desktop}.svg{fragment}" width="{width}" alt="{html.escape(alt,quote=True)}"></picture></a>')
 return ''.join(result)
def linked(name,url,alt,width=138,mobile=False):return picture(name,alt,width,mobile,target=url)
def block(content):return '<p align="center">'+content+'</p>'
def heading(key,title):return block(picture('heading-'+key,title,1120,False))
parts=['<a name="gh-dark-mode-only"></a><a name="gh-light-mode-only"></a>',block(picture('hero','Efe Varol Bedelcigil: control systems and robotics.',1280,True,True)),'<p align="left">'+linked('social-github','https://github.com/efebedelcigil','GitHub')+' '+linked('social-linkedin','https://www.linkedin.com/in/efevarolbedelcigil/','LinkedIn')+'</p>',block(linked('portfolio',profile['portfolio'],'Explore my portfolio: projects, publications, contact and more',1120,True)),heading('working','Working areas'),block(picture('focus','Working areas: '+', '.join(profile['areas']))),heading('tools','Tools'),block(picture('toolkit','Engineering tools: '+', '.join(t for g in json.loads((A/'toolkit.json').read_text(encoding='utf-8')) for t in g['tools']))),heading('learning','In progress'),block(picture('learning','In progress. Areas: '+', '.join(profile['learning_areas'])+'. Tools and methods: '+', '.join(t for g in json.loads((A/'learning.json').read_text(encoding='utf-8')) for t in g['tools']))),heading('exploring','Interested in exploring'),block(picture('exploring','Interested in exploring. Areas: '+', '.join(profile['exploring_areas'])+'. Tools and methods: '+', '.join(t for g in json.loads((A/'exploring.json').read_text(encoding='utf-8')) for t in g['tools']))),heading('contribution','Contribution circuit'),block(picture('contribution','Public contribution circuit. Live data refreshed periodically.',mobile=False)),block(picture('activity','Public activity: '+', '.join(str(v)+' '+k for k,v in data['activity'].items()),mobile=False)),heading('languages','Project languages'),block(picture('profile-cards','Public project language distribution by source code bytes.',mobile=False)),heading('pinned','Pinned repositories')]
repos=data.get('pinned',[])
cards=[linked('repo-'+r['name'],r['html_url'],r['name']+' / '+(r['description'] or ''),'49%') for r in repos]
parts.append('<p align="center">'+' '.join(cards)+'</p>' if cards else 'No public repositories pinned yet.')
def view_counter():
 result=[]
 for theme,color in [('dark','435f98'),('light','365dc1')]:
  fragment='#gh-'+theme+'-mode-only'
  url='https://komarev.com/ghpvc/?username=efebedelcigil&label=Profile+views&color='+color+'&style=flat'
  result.append(f'<a href="{html.escape(url,quote=True)}{fragment}"><img src="{html.escape(url,quote=True)}{fragment}" height="17" alt="Profile views"></a>')
 return ''.join(result)
parts.append('<hr>\n\n<p align="center">'+linked('still-link','docs/STATIC.md','Still version of landing page',190)+' &nbsp; '+view_counter()+' &nbsp; '+picture('back-top','Back to top',125,False)+'</p>')
(R/'README.md').write_text('\n\n'.join(parts)+'\n',encoding='utf-8')
