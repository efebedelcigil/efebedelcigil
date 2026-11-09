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
  if name=='contribution':sources+=f'<source media="(prefers-reduced-motion: reduce)" srcset="assets/contribution-still-{theme}.svg">'
  if hero:
   if mobile:sources+=f'<source media="(prefers-reduced-motion: reduce) and (max-width: 600px)" srcset="assets/{mobile_name}-still.svg">'
   sources+=f'<source media="(prefers-reduced-motion: reduce)" srcset="assets/{desktop}-still.svg">'
  if mobile:sources+=f'<source media="(max-width: 600px)" srcset="assets/{mobile_name}.svg">'
  result.append(f'<a href="{target or ("assets/"+desktop+".svg")}{fragment}"><picture>{sources}<img src="assets/{desktop}.svg{fragment}" width="{width}" alt="{html.escape(alt,quote=True)}"></picture></a>')
 return ''.join(result)
def linked(name,url,alt,width=138,mobile=False):return picture(name,alt,width,mobile,target=url)
parts=[picture('hero','Efe Varol Bedelcigil: control systems and robotics.',1280,True,True),linked('social-github','https://github.com/efebedelcigil','GitHub')+' '+linked('social-linkedin','https://www.linkedin.com/in/efevarolbedelcigil/','LinkedIn'),linked('portfolio',profile['portfolio'],'Projects, publications, contact and more',1120,True),'**'+profile['discipline']+'**  \n'+profile['institution']+' / '+profile['status'], '### Working areas', '**Control systems & robotics**  \n'+ ' / '.join(profile['areas'][2:]), picture('control-loop','A closed-loop control diagram'), '### Tools',picture('toolkit','Engineering tools: '+', '.join(t for g in json.loads((A/'toolkit.json').read_text(encoding='utf-8')) for t in g['tools'])),'### In progress','**Areas** / '+' / '.join(profile['learning_areas'])+'  \n**Tools**',picture('learning','In progress: '+', '.join(profile['learning_areas'])),'### Interested in exploring','**Areas** / '+' / '.join(profile['exploring_areas'])+'  \n**Tools**',picture('exploring','Interested in exploring: '+', '.join(profile['exploring_areas'])),picture('contribution','Public contribution circuit. Live data refreshed periodically.',mobile=False),picture('activity','Public activity: '+', '.join(str(v)+' '+k for k,v in data['activity'].items()),mobile=False),picture('profile-cards','Public project language distribution by source code bytes.',mobile=False),'### Pinned repositories']
repos=data.get('pinned',[])
cards=[linked('repo-'+r['name'],r['html_url'],r['name']+' / '+(r['description'] or ''),'49%') for r in repos]
parts.append('<p>'+' '.join(cards)+'</p>' if cards else 'No public repositories pinned yet.')
parts.append('---\n\n'+linked('still-link','docs/STATIC.md','Still version of landing page',220)+' &nbsp; <img src="https://komarev.com/ghpvc/?username=efebedelcigil&amp;label=Views&amp;color=526f94&amp;style=flat" height="20" alt="Total profile views">')
(R/'README.md').write_text('\n\n'.join(parts)+'\n',encoding='utf-8')
