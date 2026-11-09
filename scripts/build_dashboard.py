from pathlib import Path
import json,html,re,xml.etree.ElementTree as E,datetime
from build_identity import lettering
from circuit_route import circuit_route
R=Path(__file__).resolve().parents[1];A=R/'assets'
profile=json.loads((A/'profile.json').read_text(encoding='utf-8'));public=json.loads((A/'public-profile.json').read_text(encoding='utf-8'))
logos={'C':'c','C++':'cplusplus','Python':'python','MATLAB / Simulink':'matlab','Linux':'linux','Git':'git','Gazebo':'gazebo','Verilog':'verilog','Fusion':'fusion','EAGLE':'autodesk','KiCad':'kicad','STM32':'stmicroelectronics','ESP32':'espressif','ROS 2':'ros','Raspberry Pi':'raspberrypi','LTspice':'ltspice','Proteus':'proteus','NanoEdge AI Studio':'stmicroelectronics'}
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
 def traces(w,y):return f'<path d="M{w-160} {y}h60l20 20h65m-125-9h43l20 20h62" stroke="{line}" fill="none"/><circle cx="{w-15}" cy="{y+20}" r="3" fill="{copper}"/>'
 for mobile in (False,True):
  w=600 if mobile else 1120;suffix='-mobile' if mobile else ''
  p=[txt(profile['discipline'],8,33,28),txt(profile['institution']+' / '+profile['status'],8,66,20,muted),txt('Working areas',8,128,30,blue,650),traces(w,104)]
  # One connected circuit, with both main fields and supporting fields inside it.
  p.append(f'<rect x="8" y="146" width="{w-16}" height="150" rx="14" fill="{panel}" stroke="{line}"/>')
  for i in range(5):p.append(f'<path d="M{w-170+i*20} 155v12l20 20v88" stroke="{line}" fill="none" opacity=".65"/>')
  p.extend([txt('Control systems & robotics',32,190,30,blue,650)])
  rows=['Embedded systems / Power electronics','Mechatronics / IoT / Circuit design / 3D printing'] if mobile else ['Embedded systems / Power electronics / Mechatronics / IoT / Circuit design / 3D printing']
  for i,row in enumerate(rows):p.append(txt(row,32,231+i*33,21,muted))
  save('focus'+suffix,w,322,p)
  control=[f'<path d="M15 40h110m40 0h115m140 0h120m140 0h{1120-710}" stroke="{blue}" stroke-width="2" fill="none"/>',f'<circle cx="145" cy="40" r="20" stroke="{copper}" fill="none"/>',f'<path d="M137 40h16m-8-8v16M{1120-35} 40v58H145V60" stroke="{line}" fill="none" stroke-width="2"/>']
  for x,label in [(280,'Control'),(540,'System')]:
   if x+140>1120-15:continue
   control.extend([f'<rect x="{x}" y="15" width="140" height="50" rx="9" fill="{panel}" stroke="{blue}"/>',txt(label,x+19,48,24,ink)])
  save('control-loop'+suffix,w,112*w/1120,[f'<g transform="scale({w/1120})">']+control+['</g>'])
  for name,title,area_key in [('learning','In progress','learning_areas'),('exploring','Interested in exploring','exploring_areas')]:
   groups=json.loads((A/(name+'.json')).read_text(encoding='utf-8'));p=[]
   x,y=8,8
   for label in [t for g in groups for t in g['tools']]:
    bw=len(label)*11+53
    if x+bw>w-8:x=8;y+=49
    p.append(f'<rect x="{x}" y="{y}" width="{bw}" height="36" rx="10" fill="{panel}" stroke="{line}"/>');p.append(logo(label,x+10,y+9,muted,panel));p.append(txt(label,x+36,y+25,20));x+=bw+9
   save(name+suffix,w,y+62,p)
  p=[txt('Explore my portfolio',26,49,33,blue,650),txt('Projects, publications, contact and more',26,87,21,muted),f'<path d="M{w-67} 45h29v29m-29 0 29-29" stroke="{copper}" stroke-width="3" fill="none"/>',f'<rect x="8" y="8" width="{w-16}" height="104" rx="15" fill="{panel}" stroke="{blue}" stroke-width="2"/><path d="M18 105h{w-36}" stroke="{copper}" opacity=".65"/>']
  p=p[-1:]+p[:-1]
  save('portfolio'+suffix,w,122,p)
 # Pseudo-isometric contribution board: date-to-cell mapping stays identical across themes.
 dates=sorted(public['days']);start=datetime.date.fromisoformat(dates[0]);palette=[panel,'#31546b','#3e7a89','#5aa3ad','#88c8c3'] if theme=='dark' else ['#dce7eb','#9dbac3','#6b9ba8','#427e91','#23647b']
 p=[txt('Contribution circuit',8,34,30,blue,650),txt('Public activity / past year',8,66,19,muted)]
 p.append(f'<g transform="translate(70 108) matrix(1 .08 -.32 .82 0 0)"><rect x="0" y="10" width="1010" height="183" rx="18" fill="{line}"/><rect width="1010" height="183" rx="18" fill="{panel}" stroke="{muted}"/>')
 for week in range(53):p.append(f'<path d="M{24+week*18} 17v144" stroke="{line}" stroke-width="1"/>')
 for d in dates:
  day=datetime.date.fromisoformat(d);offset=(day-start).days;week=offset//7;row=offset%7;level=public['days'][d];x=20+week*18;y=20+row*21
  p.append(f'<rect x="{x}" y="{y}" width="12" height="13" rx="2" fill="{palette[level]}"><title>{d}: activity level {level}</title></rect>')
  if level:p.append(f'<path d="M{x-2} {y+4}h2m12 0h3M{x-2} {y+9}h2m12 0h3" stroke="{copper}" stroke-width="1"/>')
 active={(i//7,i%7) for i,d in enumerate(dates) if public['days'][d]}
 route=circuit_route(active)
 points=[(26+x*18,26.5+y*21) for x,y in route]
 wire='M'+' L'.join(f'{x},{y}' for x,y in points)
 p.append(f'<path d="{wire}" fill="none" stroke="{blue}" stroke-width="1" opacity=".25"/>')
 p.append(f'<defs><filter id="currentGlow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="2"/></filter></defs>')
 for color,weight,blur in [(blue,7,' filter="url(#currentGlow)"'),(copper,2.4,''),(ink,.8,'')]:
  p.append(f'<path d="{wire}" pathLength="1000" fill="none" stroke="{color}" stroke-width="{weight}" stroke-dasharray="18 982" stroke-linecap="round"{blur}><animate attributeName="stroke-dashoffset" from="0" to="-1000" dur="14s" repeatCount="indefinite"/></path>')
 p.append('</g>');save('contribution',1120,349,p)
 save('contribution-still',1120,349,[re.sub(r'<animate\b[^>]*/>', '', part) for part in p])
 activity=public.get('activity',{})
 p=[txt('Public activity',8,25,21,muted)]
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
 p=[txt('Project languages',8,32,30,blue,650),txt('Public source code / language bytes',8,64,19,muted)]
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
