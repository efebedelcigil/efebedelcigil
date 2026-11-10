from labels import display_label
from pathlib import Path
import json,html,re,xml.etree.ElementTree as E,datetime
from build_identity import lettering
from circuit_route import circuit_route
from design_parts import halo,centered,measure,strip_motion,branch_groups
R=Path(__file__).resolve().parents[1];A=R/'assets'
profile=json.loads((A/'profile.json').read_text(encoding='utf-8'));public=json.loads((A/'public-profile.json').read_text(encoding='utf-8'))
from vector_logos import logo
for theme in ('dark','light'):
 ink,muted,blue,copper,panel,line=('#edf2f8','#a9b8cc','#78a4ff','#efa571','#142237','#31445e') if theme=='dark' else ('#192a40','#52647a','#214fc5','#a45d36','#edf3fa','#cbd8e8')
 def txt(t,x,y,s=22,c=None,w=550):return lettering(t,x,y,s,c or ink,w)
 def save(name,w,h,p):
  if name.startswith('heading-'):
   side=sum(map(ord,name))%2;length=48+(sum(map(ord,name))%4)*17
   x=12 if not side else w-length-24
   decoration=f'<g fill="none" stroke="{blue}" stroke-width=".8" opacity=".16"><path d="M{x} 7h{length*.6}l8 8h{length*.3}m{-length*.5} -11h{length*.3}l8 8"/><circle cx="{x}" cy="7" r="1.5"/></g>'
   p=[decoration]+p
  (A/f'{name}-{theme}.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><title>{html.escape(name)}</title>'+''.join(p)+'</svg>',encoding='utf-8')
  path=A/f'{name}-{theme}.svg'
  if '<animate' in path.read_text(encoding='utf-8'):
   (A/f'{name}-{theme}-still.svg').write_text(strip_motion(path.read_text(encoding='utf-8')),encoding='utf-8')
 def traces(w,y):return f'<path d="M{w-160} {y}h60l20 20h65m-125-9h43l20 20h62" stroke="{line}" fill="none"/><circle cx="{w-15}" cy="{y+20}" r="3" fill="{copper}"/>'
 for mobile in (False,True):
  w=600 if mobile else 1120;suffix='-mobile' if mobile else ''
  support=[[]];row_width=0
  for field in profile['areas'][2:]:
   needed=measure(field,21)+47
   if row_width+needed>w-(60 if mobile else 150):support.append([]);row_width=0
   support[-1].append(field);row_width+=needed
  height=113+(len(support)-1)*39
  p=[f'<rect x="8" y="8" width="{w-16}" height="{height}" rx="14" fill="{panel}" stroke="{line}"/>']
  for i in range(4):p.append(f'<path d="M{w-140+i*18} 19v12l16 16v{height-40}" stroke="{line}" fill="none" opacity=".5"/>')
  title=' & '.join(profile['areas'][:2]);tw=measure(title,32,650)
  p+=[centered(title,w,58,32,blue,650),logo('Control systems',(w-tw)/2-34,34,blue,size=23),logo('Robotics',(w+tw)/2+12,34,blue,size=23)]
  for j,row in enumerate(support):
   widths=[measure(label,21)+33 for label in row];x=(w-sum(widths)-14*(len(row)-1))/2;y=99+j*39
   for label,bw in zip(row,widths):p+=[logo(label,x,y-17,muted),txt(label,x+26,y,21,muted)];x+=bw+14
  p.append(f'<path d="M{w-121} 19v12l16 16v{height-40}" fill="none" stroke="{copper}" stroke-width="1" stroke-dasharray="9 160" opacity=".4"><animate attributeName="stroke-dashoffset" from="0" to="-169" dur="8s" repeatCount="indefinite"/></path>')
  save('focus'+suffix,w,height+12,p)
  for name,title,area_key in [('learning','In progress','learning_areas'),('exploring','Interested in exploring','exploring_areas')]:
   p=[];y=16;groups=json.loads((A/(name+'.json')).read_text(encoding='utf-8'))
   area_groups=profile['learning_area_groups' if name=='learning' else 'exploring_area_groups']
   parts,y2=branch_groups(area_groups,w,y,'Areas',ink,muted,copper,panel,line);p+=parts
   parts,end=branch_groups(groups,w,y2,'Tools & methods',ink,muted,blue,panel,line);p+=parts
   save(name+suffix,w,end,p)
  from fontTools.pens.boundsPen import BoundsPen
  from build_identity import font_at
  def extent(text,size,weight):
   text=display_label(text)
   f=font_at(weight);glyphs=f.getGlyphSet();cmap=f.getBestCmap();bounds=[]
   for char in text:
    pen=BoundsPen(glyphs);glyphs[cmap.get(ord(char),'.notdef')].draw(pen)
    if pen.bounds:bounds.append(pen.bounds)
   scale=size/f['head'].unitsPerEm
   return min(b[1] for b in bounds)*scale,max(b[3] for b in bounds)*scale
  title='Explore my portfolio';subtitle='Projects, publications, contact and more'
  low,high=extent(title,33,650);sub_low,sub_high=extent(subtitle,21,550)
  shift=98-((60-high)+(100-sub_low))/2
  p=[f'<rect x="8" y="8" width="{w-16}" height="180" rx="10" fill="{panel}" stroke="{blue}" stroke-width="2"/>',txt(title,26,60+shift,33,blue,650),txt(subtitle,26,100+shift,21,muted),logo('Open link',w-68,83,copper,size=30)]
  p.append(halo(8,8,w-16,180,blue).replace('stroke-width="1"','stroke-width="1.3"').replace('opacity=".55"','opacity=".75"'))
  save('portfolio'+suffix,w,196,p)
 for key,title in [('working','Working areas'),('tools','Tools'),('learning','In progress'),('exploring','Interested in exploring'),('contribution','Contribution circuit'),('languages','Project languages'),('pinned','Pinned repositories')]:
  tw=measure(title,32,650);left=(1120-tw)/2
  p=[centered(title,1120,41,32,blue,650),f'<path d="M40 31H{left-28}m{tw+56} 0H1080" stroke="{line}"/><circle cx="{left-16}" cy="31" r="3" fill="{copper}"/>']
  p.append(f'<circle cx="{1120-left+16}" cy="31" r="3" fill="{copper}"/>')
  save('heading-'+key,1120,49,p)
 for name,label in [('github','GitHub'),('linkedin','LinkedIn')]:
  icon=logo(label,12,17,ink,panel)
  save('social-'+name,180,52,[f'<rect x="1" y="1" width="178" height="50" rx="13" fill="{panel}" stroke="{line}"/>',icon,txt(label,41,34,23),logo('Open link',148,18,muted,size=16)])
 # Pseudo-isometric contribution board: date-to-cell mapping stays identical across themes.
 dates=sorted(public['days']);start=datetime.date.fromisoformat(dates[0]);palette=[panel,'#31546b','#3e7a89','#5aa3ad','#88c8c3'] if theme=='dark' else ['#dce7eb','#9dbac3','#6b9ba8','#427e91','#23647b']
 period=datetime.date.fromisoformat(dates[0]).strftime('%b %Y')+' / '+datetime.date.fromisoformat(dates[-1]).strftime('%b %Y')
 p=[centered(period,1120,28,19,muted)]
 p.append(f'<g transform="translate(70 60) matrix(1 .08 -.32 .82 0 0)"><rect x="0" y="10" width="1010" height="183" rx="18" fill="{line}"/><rect width="1010" height="183" rx="18" fill="{panel}" stroke="{muted}"/>')
 p.append(halo(0,0,1010,183,copper,radius=18))
 for week in range(53):p.append(f'<path d="M{24+week*18} 17v144" stroke="{line}" stroke-width="1"/>')
 chip_start=len(p)
 for d in dates:
  day=datetime.date.fromisoformat(d);offset=(day-start).days;week=offset//7;row=offset%7;level=public['days'][d];x=20+week*18;y=20+row*21
  if not level:
   p.append(f'<path d="M{x+4} {y+6}h4" stroke="{line}" stroke-width="1" opacity=".3"/>');continue
  lift=3+level*.65
  p.append(f'<rect x="{x+1}" y="{y+2}" width="13" height="14" rx="2" fill="{line}" opacity=".7"/>')
  p.append(f'<path d="M{x-2} {y+4}h3m10 0h4M{x-2} {y+9}h3m10 0h4" stroke="{copper}" stroke-width="1.3"/>')
  p.append(f'<path d="M{x} {y+13-lift}h12v{lift}h-12z" fill="{line}"/><path d="M{x+12} {y-lift}v13l2 2V{y+2}z" fill="{muted}" opacity=".6"/>')
  p.append(f'<rect x="{x}" y="{y-lift}" width="12" height="13" rx="1.5" fill="{palette[level]}" stroke="{muted}" stroke-width=".5"><title>{d}: activity level {level}</title></rect>')
  p.append(f'<path d="M{x+1} {y+2-lift}h10" stroke="{ink}" stroke-width=".7" opacity=".45"/>')
 packages=p[chip_start:];p=p[:chip_start]
 active={(i//7,i%7) for i,d in enumerate(dates) if public['days'][d]}
 route=circuit_route(active)
 levels={(i//7,i%7):public['days'][d] for i,d in enumerate(dates)}
 points=[(26+x*18,26.5+y*21) for x,y in route]
 wire='M'+' L'.join(f'{x},{y}' for x,y in points)
 p.append(f'<path d="{wire}" fill="none" stroke="{copper}" stroke-width="1" opacity=".18"/>')
 p.append(f'<defs><filter id="currentGlow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="2"/></filter></defs>')
 for color,weight,blur in [(copper,6,' filter="url(#currentGlow)"'),(copper,2.5,''),('#ffe1bd',.75,'')]:
  p.append(f'<path d="{wire}" pathLength="1000" fill="none" stroke="{color}" stroke-width="{weight}" stroke-dasharray="18 982" stroke-linecap="round"{blur}><animate attributeName="stroke-dashoffset" from="0" to="-1000" dur="14s" repeatCount="indefinite"/></path>')
 p+=packages
 from math import hypot
 distances=[0.0]
 for a,b in zip(points,points[1:]):distances.append(distances[-1]+hypot(b[0]-a[0],b[1]-a[1]))
 total_length=distances[-1] or 1
 for cell in sorted(active):
  x,y=20+cell[0]*18,20+cell[1]*21;lift=3+levels[cell]*.65
  phase=max(0,distances[route.index(cell)]/total_length*14-.25)
  p.append(f'<path d="M{x+4} {y-2}v3m5-3v3M{x+4} {y+12}v3m5-3v3" stroke="{copper}" stroke-width="1"/>')
  p.append(f'<rect x="{x+3}" y="{y+4-lift}" width="6" height="4" rx="1" fill="{copper}" opacity=".12"><animate attributeName="opacity" values=".12;.7;.12;.12" keyTimes="0;.025;.065;1" begin="{phase:.3f}s" dur="14s" repeatCount="indefinite"/></rect>')
 p.append('</g>');save('contribution',1120,301,p)
 save('contribution-still',1120,301,[re.sub(r'<animate\b[^>]*/>', '', part) for part in p])
 activity=public.get('activity',{})
 p=[centered('Public activity',1120,25,21,copper,600)]
 for i,(label,count) in enumerate(activity.items()):
  text=str(count)+' '+label;tw=measure(text,21)+30;cx=(i+.5)*280;x=cx-tw/2
  p.append(logo(label,x,54,blue,size=20));p.append(txt(text,x+30,73,21,ink))
 save('activity',1120,96,p)
 # Language distribution uses public repository language bytes, excluding forks and the profile repository.
 repos=public['repos'];projects=public.get('pinned',[])
 languages=public.get('languages',{});total=sum(languages.values()) or 1
 colors=[blue,copper,'#65b8ae','#a995d0','#aab8c8']
 p=[centered('Public source code / language bytes',1120,25,19,muted)]
 ordered=sorted(languages.items(),key=lambda item:-item[1])
 labels=[language+' '+str(round(value/total*100,1))+'%' for language,value in ordered]
 col_widths=[max([measure(labels[i],20)+19 for i in range(col,len(labels),3)] or [0]) for col in range(3)]
 legend_left=(1120-sum(col_widths)-144)/2
 cursor=8
 for i,(language,value) in enumerate(sorted(languages.items(),key=lambda x:-x[1])):
  span=1104*value/total;c=colors[i%len(colors)]
  p.append(f'<rect x="{cursor}" y="46" width="{span}" height="22" fill="{c}"/>')
  p.append(f'<path d="M{cursor} 41v32" stroke="{line}"/>');cursor+=span
  x=legend_left+sum(col_widths[:i%3])+(i%3)*72;y=108+(i//3)*35
  p.append(f'<circle cx="{x+5}" cy="{y-7}" r="4" fill="{c}"/>');p.append(txt(language+' '+str(round(value/total*100,1))+'%',x+19,y,20))
 save('profile-cards',1120,136+((len(languages)-1)//3)*35,p)
 def shorten(t,n):return t if len(t)<=n else t[:n-3].rstrip()+'...'
 for repo in projects:
  title=repo['name'];desc=shorten(repo['description'] or 'Public repository',48)
  names=[key for key,_ in sorted(repo.get('languages',{}).items(),key=lambda x:-x[1])]
  language_text=' / '.join(names) or repo.get('language') or 'Public repository'
  while measure(language_text,17)>490:language_text=language_text[:-4].rstrip(' .')+'...'
  p=[f'<rect x="1" y="1" width="538" height="166" rx="13" stroke="{line}" fill="{panel}"/>',txt(shorten(title,31),22,43,24,ink,650),txt(desc,22,76,20,muted),txt(language_text,22,110,17,muted),txt('View repository',22,146,18,blue),logo('View repository',496,128,blue,size=22)]
  p.append(halo(1,1,538,166,blue,radius=13).replace('stroke-width="1"','stroke-width="1.5"').replace('opacity=".55"','opacity=".75"'))
  save('repo-'+title,540,168,p)
 save('still-link',400,40,[f'<rect x="1" y="1" width="398" height="38" rx="10" fill="{panel}" stroke="{line}"/>',logo('Pause',12,12,blue,size=18),txt('Still version of landing page',36,29,22,ink)])

 save('back-top',190,40,[f'<rect x="1" y="1" width="188" height="36" rx="9" fill="{panel}" stroke="{line}"/>',logo('Back to top',12,9,blue,size=18),txt('Back to top',38,26,20,ink)])
