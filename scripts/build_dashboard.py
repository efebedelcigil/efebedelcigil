from pathlib import Path
import json,html,re,xml.etree.ElementTree as E,datetime
from build_identity import lettering
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
  for name,title,area_key in [('learning','In progress','learning_areas'),('exploring','Interested in exploring','exploring_areas')]:
   groups=json.loads((A/(name+'.json')).read_text(encoding='utf-8'));p=[txt(title,8,35,31,blue,650),txt('Areas',8,78,19,copper),txt(' / '.join(profile[area_key]),8,110,21),txt('Tools',8,154,19,copper),traces(w,18)]
   x,y=8,173
   for label in [t for g in groups for t in g['tools']]:
    bw=len(label)*11+53
    if x+bw>w-8:x=8;y+=49
    p.append(f'<rect x="{x}" y="{y}" width="{bw}" height="36" rx="10" fill="{panel}" stroke="{line}"/>');p.append(logo(label,x+10,y+9,muted,panel));p.append(txt(label,x+36,y+25,20));x+=bw+9
   save(name+suffix,w,y+62,p)
  p=[txt('Explore the portfolio',26,49,33,blue,650),txt('Projects, publications, contact and more',26,87,21,muted),f'<path d="M{w-67} 45h29v29m-29 0 29-29" stroke="{copper}" stroke-width="3" fill="none"/>',f'<rect x="8" y="8" width="{w-16}" height="104" rx="15" fill="{panel}" stroke="{blue}" stroke-width="2"/><path d="M18 105h{w-36}" stroke="{copper}" opacity=".65"/>']
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
 p.append(f'<path d="M24 12h950v151H24Z" fill="none" stroke="{blue}" stroke-width="2" opacity=".18"/>')
 p.append(f'<path d="M24 12h950v151H24Z" fill="none" stroke="{copper}" stroke-width="3" stroke-dasharray="30 2192" stroke-linecap="round"><animate attributeName="stroke-dashoffset" from="0" to="-2222" dur="9s" repeatCount="indefinite"/></path>')
 for week in range(0,53,4):p.append(f'<circle cx="{24+week*18}" cy="12" r="3" fill="{blue}"><animate attributeName="opacity" values=".3;1;.3" dur="3s" begin="{week*.07}s" repeatCount="indefinite"/></circle>')
 p.append('</g>');p.append(txt('Each component represents an active public day.',8,359,19,muted));save('contribution',1120,382,p)
 save('contribution-still',1120,382,[re.sub(r'<animate\b[^>]*/>', '', part) for part in p])
 activity=public.get('activity',{})
 p=[txt('Public activity',8,25,21,muted)]
 for i,(label,count) in enumerate(activity.items()):p.append(txt(str(count)+' '+label,8+i*277,66,21,ink))
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
 save('still-link',340,30,[txt('Still version of landing page',8,23,21,muted)])
