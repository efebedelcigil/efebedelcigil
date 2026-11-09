from pathlib import Path
import json,html,re,xml.etree.ElementTree as E,datetime
from build_identity import lettering
from circuit_route import circuit_route
from design_parts import halo,centered,measure,strip_motion
R=Path(__file__).resolve().parents[1];A=R/'assets'
profile=json.loads((A/'profile.json').read_text(encoding='utf-8'));public=json.loads((A/'public-profile.json').read_text(encoding='utf-8'))
logos={'GitHub':'github','LinkedIn':'linkedin','C':'c','C++':'cplusplus','Python':'python','MATLAB / Simulink':'matlab','Linux':'linux','Git':'git','Gazebo':'gazebo','Verilog':'verilog','Fusion':'fusion','EAGLE':'autodesk','KiCad':'kicad','STM32':'stmicroelectronics','ESP32':'espressif','ROS 2':'ros','Raspberry Pi':'raspberrypi','LTspice':'ltspice','Proteus':'proteus','NanoEdge AI Studio':'stmicroelectronics'}
def logo(label,x,y,c,bg=None):
 path=A/'logos'/(logos.get(label,'_')+'.svg')
 if not path.exists():return f'<path d="M{x+3} {y+2}h12v12H{x+3}zM{x} {y+6}h3m12 0h3M{x+7} {y-1}v3m0 12v3" fill="none" stroke="{c}" stroke-width="1.3"/>'
 r=E.parse(path).getroot();vb=r.get('viewBox','0 0 24 24')
 for e in r.iter():
  for k in ['style','class']:e.attrib.pop(k,None)
  if e.get('fill')!='none':e.set('fill',bg if bg and e.get('fill','').lower() in ('#fff','#ffffff','white') else c)
  if e.get('stroke') and e.get('stroke')!='none':e.set('stroke',c)
  if e.tag.endswith('style'):e.text=''
 r.set('x',str(x));r.set('y',str(y));r.set('width','18');r.set('height','18');r.set('viewBox',vb)
 return E.tostring(r,encoding='unicode')
for theme in ('dark','light'):
 ink,muted,blue,copper,panel,line=('#edf2f8','#a9b8cc','#78a4ff','#efa571','#142237','#31445e') if theme=='dark' else ('#192a40','#52647a','#214fc5','#a45d36','#edf3fa','#cbd8e8')
 def txt(t,x,y,s=22,c=None,w=550):return lettering(t,x,y,s,c or ink,w)
 def save(name,w,h,p):
  (A/f'{name}-{theme}.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><title>{html.escape(name)}</title>'+''.join(p)+'</svg>',encoding='utf-8')
  path=A/f'{name}-{theme}.svg'
  if '<animate' in path.read_text(encoding='utf-8'):
   (A/f'{name}-{theme}-still.svg').write_text(strip_motion(path.read_text(encoding='utf-8')),encoding='utf-8')
 def traces(w,y):return f'<path d="M{w-160} {y}h60l20 20h65m-125-9h43l20 20h62" stroke="{line}" fill="none"/><circle cx="{w-15}" cy="{y+20}" r="3" fill="{copper}"/>'
 for mobile in (False,True):
  w=600 if mobile else 1120;suffix='-mobile' if mobile else ''
  p=[f'<rect x="8" y="8" width="{w-16}" height="174" rx="14" fill="{panel}" stroke="{line}"/>']
  for i in range(4):p.append(f'<path d="M{w-140+i*18} 19v12l16 16v111" stroke="{line}" fill="none" opacity=".65"/>')
  p.append(centered('Control systems & robotics',w,58,32,blue,650))
  rows=['Embedded systems / Power electronics','Mechatronics / IoT / Circuit design / 3D printing'] if mobile else ['Embedded systems / Power electronics / Mechatronics / IoT','Circuit design / 3D printing']
  for j,row in enumerate(rows):p.append(centered(row,w,103+j*34,22,muted))
  save('focus'+suffix,w,194,p)
  for name,title,area_key in [('learning','In progress','learning_areas'),('exploring','Interested in exploring','exploring_areas')]:
   groups=json.loads((A/(name+'.json')).read_text(encoding='utf-8'));p=[]
   y=16
   for branch,labels in [('Areas',profile[area_key]),('Tools & methods',[t for g in groups for t in g['tools']])]:
    p.append(f'<path d="M18 {y-10}v40h25" stroke="{line}" fill="none"/>');p.append(txt(branch,50,y+15,21,copper,600))
    rows=[[]];used=0
    for label in labels:
     bw=measure(label,20)+55
     if used+bw>w-68:rows.append([]);used=0
     rows[-1].append((label,bw));used+=bw+9
    layout=[]
    for row_index,row in enumerate(rows):
     x=50+(w-68-sum(bw for _,bw in row)-9*(len(row)-1))/2
     for label,bw in row:layout.append((label,x,y+34+49*row_index,bw));x+=bw+9
    for j,(label,x,by,bw) in enumerate(layout):
     p.append(f'<rect x="{x}" y="{by}" width="{bw}" height="36" rx="10" fill="{panel}" stroke="{line}"/>');p.append(halo(x,by,bw,36,copper if branch=='Areas' else blue,j*17))
     marks={'Machine learning':'M1 1h15v15H1zM4 4l9 9M4 13l9-9','TinyML':'M2 2h14v14H2zM6 6h6v6H6z','Motor control':'M9 1a8 8 0 1 0 0 16 8 8 0 1 0 0-16M4 12V6l5 5 5-5v6','Sensor fusion':'M1 3l8 6 8-6M1 15l8-6 8 6M9 1v16'}
     if label in marks:p.append(f'<path d="{marks[label]}" transform="translate({x+10} {by+9})" stroke="{muted}" stroke-width="1.4" fill="none"/>')
     else:p.append(logo(label,x+10,by+9,muted,panel))
     p.append(txt(label,x+36,by+25,20))
    p.append(f'<path d="M18 {y+30}v{by-y+8}" stroke="{line}" fill="none"/>');y=by+66
   save(name+suffix,w,y,p)
  p=[txt('Explore my portfolio',26,49,33,blue,650),txt('Projects, publications, contact and more',26,87,21,muted),f'<path d="M{w-67} 45h29v29m-29 0 29-29" stroke="{copper}" stroke-width="3" fill="none"/>',f'<rect x="8" y="8" width="{w-16}" height="104" rx="15" fill="{panel}" stroke="{blue}" stroke-width="2"/><path d="M18 105h{w-36}" stroke="{copper}" opacity=".65"/>']
  p=p[-1:]+p[:-1]
  save('portfolio'+suffix,w,122,p)
 for key,title in [('working','Working areas'),('tools','Tools'),('learning','In progress'),('exploring','Interested in exploring'),('contribution','Contribution circuit'),('languages','Project languages'),('pinned','Pinned repositories')]:
  tw=measure(title,32,650);left=(1120-tw)/2
  p=[centered(title,1120,41,32,blue,650),f'<path d="M40 31H{left-28}m{tw+56} 0H1080" stroke="{line}"/><circle cx="{left-16}" cy="31" r="3" fill="{copper}"/>']
  save('heading-'+key,1120,65,p)
 for name,label in [('github','GitHub'),('linkedin','LinkedIn')]:
  icon=logo(label,12,17,ink,panel)
  save('social-'+name,180,52,[f'<rect x="1" y="1" width="178" height="50" rx="13" fill="{panel}" stroke="{line}"/>',icon,txt(label,41,34,23),f'<path d="M151 30l8-8m-7 0h7v7" fill="none" stroke="{muted}" stroke-width="2"/>'])
 # Pseudo-isometric contribution board: date-to-cell mapping stays identical across themes.
 dates=sorted(public['days']);start=datetime.date.fromisoformat(dates[0]);palette=[panel,'#31546b','#3e7a89','#5aa3ad','#88c8c3'] if theme=='dark' else ['#dce7eb','#9dbac3','#6b9ba8','#427e91','#23647b']
 p=[centered('Public activity / past year',1120,28,19,muted)]
 p.append(f'<g transform="translate(70 60) matrix(1 .08 -.32 .82 0 0)"><rect x="0" y="10" width="1010" height="183" rx="18" fill="{line}"/><rect width="1010" height="183" rx="18" fill="{panel}" stroke="{muted}"/>')
 for week in range(53):p.append(f'<path d="M{24+week*18} 17v144" stroke="{line}" stroke-width="1"/>')
 for d in dates:
  day=datetime.date.fromisoformat(d);offset=(day-start).days;week=offset//7;row=offset%7;level=public['days'][d];x=20+week*18;y=20+row*21
  if not level:
   p.append(f'<rect x="{x}" y="{y}" width="12" height="13" rx="2" fill="{palette[0]}"/>');continue
  lift=3+level*.65
  p.append(f'<rect x="{x+1}" y="{y+2}" width="13" height="14" rx="2" fill="{line}" opacity=".7"/>')
  p.append(f'<path d="M{x-2} {y+4}h3m10 0h4M{x-2} {y+9}h3m10 0h4" stroke="{copper}" stroke-width="1.3"/>')
  p.append(f'<path d="M{x} {y+13-lift}h12v{lift}h-12z" fill="{line}"/><path d="M{x+12} {y-lift}v13l2 2V{y+2}z" fill="{muted}" opacity=".6"/>')
  p.append(f'<rect x="{x}" y="{y-lift}" width="12" height="13" rx="1.5" fill="{palette[level]}" stroke="{muted}" stroke-width=".5"><title>{d}: activity level {level}</title></rect>')
  p.append(f'<path d="M{x+1} {y+2-lift}h10" stroke="{ink}" stroke-width=".7" opacity=".45"/>')
 active={(i//7,i%7) for i,d in enumerate(dates) if public['days'][d]}
 route=circuit_route(active)
 levels={(i//7,i%7):public['days'][d] for i,d in enumerate(dates)}
 points=[(26+x*18,26.5+y*21-(3+levels[(x,y)]*.65 if levels.get((x,y)) else 0)) for x,y in route]
 wire='M'+' L'.join(f'{x},{y}' for x,y in points)
 p.append(f'<path d="{wire}" fill="none" stroke="{copper}" stroke-width="1" opacity=".18"/>')
 p.append(f'<defs><filter id="currentGlow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="2"/></filter></defs>')
 for color,weight,blur in [(copper,6,' filter="url(#currentGlow)"'),(copper,2.5,''),('#ffe1bd',.75,'')]:
  p.append(f'<path d="{wire}" pathLength="1000" fill="none" stroke="{color}" stroke-width="{weight}" stroke-dasharray="18 982" stroke-linecap="round"{blur}><animate attributeName="stroke-dashoffset" from="0" to="-1000" dur="14s" repeatCount="indefinite"/></path>')
 p.append('</g>');save('contribution',1120,301,p)
 save('contribution-still',1120,301,[re.sub(r'<animate\b[^>]*/>', '', part) for part in p])
 activity=public.get('activity',{})
 p=[centered('Public activity',1120,25,21,muted)]
 marks={'Commits':'M1 9h4m8 0h4M9 5a4 4 0 1 0 0 8 4 4 0 1 0 0-8','Issues':'M9 1a8 8 0 1 0 0 16 8 8 0 1 0 0-16M9 5v5m0 3v.1','Pull requests':'M4 3v11M1 2a3 3 0 1 0 6 0M1 16a3 3 0 1 0 6 0M11 3h3v10m-6-10 3-3m-3 3 3 3M11 16a3 3 0 1 0 6 0','Reviews':'M1 1h16v12H7l-5 4v-4H1zM5 7l3 3 5-6'}
 for i,(label,count) in enumerate(activity.items()):
  x=8+i*277
  p.append(f'<path d="{marks[label]}" transform="translate({x} 49)" stroke="{blue}" stroke-width="1.5" fill="none" stroke-linecap="round"/>')
  p.append(txt(str(count)+' '+label,x+28,66,21,ink))
 save('activity',1120,89,p)
 # Language distribution uses public repository language bytes, excluding forks and the profile repository.
 repos=public['repos'];projects=public.get('pinned',[])
 languages=public.get('languages',{});total=sum(languages.values()) or 1
 colors=[blue,copper,'#65b8ae','#a995d0','#aab8c8']
 p=[centered('Public source code / language bytes',1120,64,19,muted)]
 cursor=8
 for i,(language,value) in enumerate(sorted(languages.items(),key=lambda x:-x[1])):
  span=1104*value/total;c=colors[i%len(colors)]
  p.append(f'<rect x="{cursor}" y="87" width="{span}" height="22" fill="{c}"/>')
  p.append(f'<path d="M{cursor} 82v32" stroke="{line}"/>');cursor+=span
  x=8+(i%3)*365;y=149+(i//3)*35
  p.append(f'<circle cx="{x+5}" cy="{y-7}" r="4" fill="{c}"/>');p.append(txt(language+' '+str(round(value/total*100,1))+'%',x+19,y,20))
 save('profile-cards',1120,177+((len(languages)-1)//3)*35,p)
 def shorten(t,n):return t if len(t)<=n else t[:n-3].rstrip()+'...'
 for repo in projects:
  title=repo['name'];desc=shorten(repo['description'] or 'Public repository',48)
  p=[f'<rect x="1" y="1" width="538" height="140" rx="13" stroke="{line}" fill="{panel}"/>',txt(shorten(title,31),22,45,24,ink,650),txt(desc,22,80,20,muted),txt(repo.get('language') or 'Repository',22,117,18,blue)]
  save('repo-'+title,540,142,p)
 save('still-link',400,42,[f'<rect x="1" y="1" width="398" height="40" rx="10" fill="{panel}" stroke="{line}"/>',f'<path d="M16 15v12m5-12v12" stroke="{blue}" stroke-width="2"/>',txt('Still version of landing page',36,29,22,ink)])
